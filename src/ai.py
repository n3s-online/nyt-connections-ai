import datetime
from game_state import AttemptResult, AttemptResultStatus
import openai
import json
from typing import List

# MODEL_TO_USE = "gpt-3.5-turbo"
MODEL_TO_USE = "gpt-4"


def getLogFileName() -> str:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"logs/{timestamp}.txt"


def logMessages(messages: List[dict]):
    log_file_name = getLogFileName()
    with open(log_file_name, "w") as log_file:
        for message in messages:
            # replace every "\n" with "\n\t" in the message content
            content = message["content"].replace("\n", "\n\t")
            log_file.write(f"{message['role']}:\n\t{content}\n")
        log_file.write("\n")


def getSystemMessage(message: str) -> dict:
    return {"role": "system", "content": f"{message}"}


def getAssistantMessage(message: str) -> dict:
    return {"role": "assistant", "content": f"{message}"}


def getUserMessage(message: str) -> dict:
    return {"role": "user", "content": f"{message}"}


SYSTEM_MESSAGE_BASE = """You are playing a game. You will be provided with a group of words. There are several groups of 4 words each that share a common theme / category. List each group of 4 words with their associated theme in order of confidence.

Examples of groupings:
- Fish: Bass, Flounder, Salmon, Trout
- Fire _: Ant, Drill, Island, Opal
- Fruit Homophones: Lyme, Mellon, Pair, Plumb
- Publications: Journal, Globe, Post, Asteroid

Each word can only be in one grouping, and each grouping must have 4 words exactly. The grouping cannot have a theme like "Random words", "General terms" or "Unrelated words", they must be connected in some way. 
The user may also give information about previous attempted groups.
Order does not matter, for example, if the user has already attempted the group "A, B, C, D", Do not provide a guess of "D, C, B, A" or any other combination of the same 4 words.
"""
STARTING_MESSAGE = getSystemMessage(SYSTEM_MESSAGE_BASE)

CONVERT_TO_JSON_MESSAGE_BASE = """
Convert your response to a JSON string which is an array where each element in the array has a words array, and a theme array. Every group must have 4 words.
If I were to type this in typescript it'd be `{words: string[]; theme: string;}[]`.
"""
CONVERT_TO_JSON_MESSAGE = getSystemMessage(CONVERT_TO_JSON_MESSAGE_BASE)


def getUserWordMessage(words: List[str], relevant_attempt: AttemptResult) -> dict:
    message = json.dumps(words)
    number_of_groups_to_provide = len(words) // 4
    message += f"\nProvide {number_of_groups_to_provide} groups of 4 words each."
    if relevant_attempt != None:
        message += f"\n{summarizeAttempt(relevant_attempt)}"
    return getUserMessage(message)


def getCorrectionAttemptMessage(attempt: AttemptResult) -> dict:
    message = f"Correction: {summarizeAttempt(attempt)})"
    return getUserMessage(message)


def summarizeAttempt(attempt: AttemptResult) -> str:
    words = attempt.words
    message = ""
    if attempt.result == AttemptResultStatus.FAILURE:
        message = f"You know that {str(words)} is not a valid grouping. Try to find a different category."
    elif attempt.result == AttemptResultStatus.ONE_AWAY:
        message = f"You know that {str(words)} is not a valid grouping, 3 of the 4 words are in the same category. Identify which other word from the input belongs in this category. Identify which word does not belong in this category. Swap the word that does not belong with the new word."
    else:
        raise Exception("Attempt was successful, no need to correct")
    return (
        message
        + " As a reminder, the output must be groups of 4 words each, every word being unique and from the original input."
    )


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
    def get_initial_guesses(
        self, words: List[str], relevant_attempt: AttemptResult
    ) -> List[AIResponse]:
        initial_message = getUserWordMessage(words, relevant_attempt)
        self.messages = [STARTING_MESSAGE, initial_message]
        assistant_response = getResponse(self.messages)
        self.messages.append(getAssistantMessage(assistant_response))
        messages_with_json = self.messages + [CONVERT_TO_JSON_MESSAGE]
        assistant_json_response = getResponse(messages_with_json)
        logMessages(
            self.messages
            + [CONVERT_TO_JSON_MESSAGE, getAssistantMessage(assistant_json_response)]
        )
        return parseJson(assistant_json_response)

    # messages:
    # 1. [System, Words (? 3away), Assistant, Correction]
    # 2. [System, Words (? 3away), Assistant, Correction, Assistant, ConvertToJson]
    def get_modified_guess(
        self, words: List[str], relevant_attempt: AttemptResult
    ) -> List[AIResponse]:
        correction_message = getCorrectionAttemptMessage(relevant_attempt)
        self.messages.append(correction_message)
        assistant_response = getResponse(self.messages)
        self.messages.append(getAssistantMessage(assistant_response))
        messages_with_json = self.messages + [CONVERT_TO_JSON_MESSAGE]
        assistant_json_response = getResponse(messages_with_json)
        logMessages(
            self.messages
            + [CONVERT_TO_JSON_MESSAGE, getAssistantMessage(assistant_json_response)]
        )
        return parseJson(assistant_json_response)


def parseJson(assistant_json_response: str) -> List[AIResponse]:
    # try to json.loads, but catch error and print assistant_json-response if JSONDecodeError happens
    try:
        json_response = json.loads(assistant_json_response)
        return [AIResponse(obj) for obj in json_response]
    except json.decoder.JSONDecodeError:
        print("Error parsing JSON")
        print(assistant_json_response)
        raise json.decoder.JSONDecodeError
