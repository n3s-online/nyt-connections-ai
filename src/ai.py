from game_state import AttemptResult, AttemptResultStatus
import openai
import json
from typing import List

# MODEL_TO_USE = "gpt-3.5-turbo"
MODEL_TO_USE = "gpt-4"


def getSystemMessage(message: str) -> dict:
    return {"role": "system", "content": f"{message}"}


def getAssistantMessage(message: str) -> dict:
    return {"role": "assistant", "content": f"{message}"}


def getUserMessage(message: str) -> dict:
    return {"role": "user", "content": f"{message}"}


SYSTEM_MESSAGE_BASE = """
You are playing a game. You will be provided with a group of words. There are several groups of 4 words each that share a common theme / category. List each group of 4 words with their associated theme in order of confidence.

Examples of groupings:
- Fish: Bass, Flounder, Salmon, Trout
- Fire _: Ant, Drill, Island, Opal
- Fruit Homophones: Lyme, Mellon, Pair, Plumb
- Publications: Journal, Globe, Post, Asteroid

Each word can only be in one grouping, and each grouping must have 4 words exactly. The grouping cannot have a theme like "Random words", "General terms" or "Unrelated words", they must be connected in some way. 
The user may also give information about previous attempted groups.
"""
STARTING_MESSAGE = getSystemMessage(SYSTEM_MESSAGE_BASE)

CONVERT_TO_JSON_MESSAGE_BASE = """
Convert your response to a JSON string which is an array where each element in the array has a words array, and a theme array. Every group must have 4 words.
If I were to type this in typescript it'd be `{words: string[]; theme: string;}[]`.
"""
CONVERT_TO_JSON_MESSAGE = getSystemMessage(CONVERT_TO_JSON_MESSAGE_BASE)


def getUserWordMessage(words: List[str]) -> dict:
    words_as_json_string = json.dumps(words)
    return getUserMessage(words_as_json_string)


def getCorrectionAttemptMessage(attempt: AttemptResult) -> dict:
    words = attempt.words
    message = ""
    if attempt.result == AttemptResultStatus.SUCCESS:
        raise Exception("Attempt was successful, no need to correct")
    elif attempt.result == AttemptResultStatus.FAILURE:
        message = f"Correction: {str(words)} is not a valid grouping."
    elif attempt.result == AttemptResultStatus.ONE_AWAY:
        message = f"Correction: {str(words)} is not a valid grouping. 3 of these 4 words were in in the same group, but 1 did not belong."
    return getUserMessage(message)


def getResponse(messages: List[dict]) -> str:
    response = openai.ChatCompletion.create(
        model=MODEL_TO_USE,
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    response_content = response["choices"][0]["message"]["content"]
    return response_content


class AIResponse:
    def __init__(self, obj):
        self.words: List[str] = [word.upper() for word in obj["words"]]
        self.theme: str = obj["theme"]

    def __str__(self):
        return f"{self.theme}: {self.words}"

    def get_words(self) -> List[str]:
        return self.words


class AI:
    def __init__(self, open_api_key):
        self.open_api_key = open_api_key
        openai.api_key = open_api_key

    # messages:
    # 1. [System, Words]
    # 2. [System, Words, Assistant, ConvertToJson]
    # returns the 4 ai responses
    def get_initial_guesses(self, words: List[str]) -> List[AIResponse]:
        words_as_message = getUserWordMessage(words)
        self.messages = [STARTING_MESSAGE, words_as_message]
        assistant_response = getResponse(self.messages)
        self.messages.append(getAssistantMessage(assistant_response))
        messages_with_json = self.messages + [CONVERT_TO_JSON_MESSAGE]
        assistant_json_response = getResponse(messages_with_json)
        json_response = json.loads(assistant_json_response)
        return [AIResponse(obj) for obj in json_response]

    # messages:
    # 1. [System, Words, Assistant, Correction]
    # 2. [System, Words, Assistant, Correction, Assistant, ConvertToJson]
    def get_modified_guess(
        self, words: List[str], relevant_attempt: AttemptResult
    ) -> List[AIResponse]:
        correction_message = getCorrectionAttemptMessage(relevant_attempt)
        self.messages.append(correction_message)
        assistant_response = getResponse(self.messages)
        self.messages.append(getAssistantMessage(assistant_response))
        messages_with_json = self.messages + [CONVERT_TO_JSON_MESSAGE]
        assistant_json_response = getResponse(messages_with_json)
        json_response = json.loads(assistant_json_response)
        return [AIResponse(obj) for obj in json_response]
