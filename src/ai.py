from game_state import GameState, Attempt, AttemptResult
import openai
import json
from typing import List

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
Convert your response to a JSON string which is an array where each element in the array has a words array, and a theme array.
If I were to type this in typescript it'd be `{words: string[]; theme: string;}[]`.
"""
CONVERT_TO_JSON_MESSAGE = getSystemMessage(CONVERT_TO_JSON_MESSAGE_BASE)

ATTEMPT_RESULTS_TO_ADD_TO_MESSAGE = [AttemptResult.ONE_AWAY, AttemptResult.FAILURE]


def isAttemptRelevant(words: List[str], attempt: Attempt) -> bool:
    if attempt.result not in ATTEMPT_RESULTS_TO_ADD_TO_MESSAGE:
        return False
    all_attempt_words_are_in_words = all(
        [attempt_word in words for attempt_word in attempt.words]
    )
    return all_attempt_words_are_in_words


def convertAttemptToMessage(attempt: Attempt) -> str:
    attempt_as_json_string = json.dumps(attempt.words)
    if attempt.result == AttemptResult.ONE_AWAY:
        return f"In a previous attempt of {attempt_as_json_string}, 3 of these words belong to the same group but one of them does not."
    elif attempt.result == AttemptResult.FAILURE:
        return f"In a previous attempt of {attempt_as_json_string}, these 4 words do not belong to the same group."
    raise Exception(f"Unexpected attempt result: {attempt.result}")


def getUserWordMessage(words: List[str], attempts: List[Attempt]) -> dict:
    words_as_json_string = json.dumps(words)
    attempts_for_message = list(
        filter(
            lambda attempt: isAttemptRelevant(words, attempt),
            attempts,
        )
    )
    attempts_as_messages = list(map(convertAttemptToMessage, attempts_for_message))
    message_string = "\n".join([words_as_json_string] + attempts_as_messages)
    return getUserMessage(message_string)


def getResponse(messages: List[dict]) -> str:
    print("Sending messages: ", messages)
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
        self.words: List[str] = obj["words"]
        self.theme: str = obj["theme"]

    def __str__(self):
        return f"{self.theme}: {self.words}"


class AI:
    def __init__(self, open_api_key):
        self.open_api_key = open_api_key
        openai.api_key = open_api_key

    def getWords(self, state: GameState) -> List[AIResponse]:
        words_as_message = getUserWordMessage(
            state.getRemainingWords(), state.getAttemptHistory()
        )
        messages = [STARTING_MESSAGE, words_as_message]
        initial_response = getResponse(messages)
        print("Got initial response: ", initial_response)
        messages.append(getAssistantMessage(initial_response))
        messages.append(CONVERT_TO_JSON_MESSAGE)
        response = getResponse(messages)
        print("Got response: ", response)
        json_response = json.loads(response)
        return [AIResponse(obj) for obj in json_response]
