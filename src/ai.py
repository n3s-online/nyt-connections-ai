"""This module contains the AI class which is responsible for 
communicating with the OpenAI API and parsing the response."""

import json
from typing import List, Set
from prompts.prompts import SYSTEM_MESSAGE_BASE_V1
from utils.openai_wrapper import (
    OpenAIMessageFactory,
    OpenAIMessage,
    OpenAIChat,
    OpenAIChatBuilder,
)
from game_state import GameState


def get_system_message_content(remaining_words: Set[str]) -> str:
    """Get the content of the system message."""
    number_of_groups_to_provide = len(remaining_words) // 4
    message = SYSTEM_MESSAGE_BASE_V1
    message += f"\nProvide {number_of_groups_to_provide} groups of 4 words each."
    return message


def get_system_message(game_state: GameState) -> OpenAIMessage:
    """Get the system message."""
    message = get_system_message_content(game_state.get_remaining_words())
    return OpenAIMessageFactory.get_system_message(message)


def get_initial_user_message_content(remaining_words: Set[str]) -> str:
    """Get the content of the initial user message."""
    message = json.dumps(list(remaining_words))
    return message


def get_initial_user_message(game_state: GameState) -> OpenAIMessage:
    """Get the initial user message."""
    message = get_initial_user_message_content(game_state.get_remaining_words())
    return OpenAIMessageFactory.get_user_message(message)


CONVERT_TO_JSON_MESSAGE_CONTENT = """
Convert your response to JSON where the response has an array of objects, each of which have a words string array, and a theme string. Every group must have 4 words.
If I were to type the JSON in typescript it'd be `{groups: {words: string[]; theme: string;}[];}`.
"""
CONVERT_TO_JSON_MESSAGE = OpenAIMessageFactory.get_system_message(
    CONVERT_TO_JSON_MESSAGE_CONTENT
)


class AIGuess:
    """Class for representing a guess from the AI."""

    def __init__(self, words: Set[str], theme: str):
        self.words = {word.upper() for word in words}
        self.theme = theme

    def __str__(self):
        return f"{self.theme}: {str(list(self.words))}"

    def get_words(self) -> Set[str]:
        """Return the words in the guess."""
        return self.words


class AI:
    """Class for representing the AI."""

    def __init__(self, game_state: GameState, model: str):
        self.game_state = game_state
        self.model = model

    def __convert_to_json_and_parse(
        self, chat_builder_input: OpenAIChatBuilder
    ) -> List[AIGuess]:
        """Add on the JSON system message, get assistant response, and parse it."""
        chat_builder = OpenAIChatBuilder(chat_builder_input).with_message(
            CONVERT_TO_JSON_MESSAGE
        )
        chat = OpenAIChat(chat_builder)
        assistant_response = chat.get_json_response()
        json_string = assistant_response.get_content()
        json_object = json.loads(json_string)
        guesses: List[AIGuess] = []
        for group in json_object["groups"]:
            words = set(group["words"])
            theme = group["theme"]
            guesses.append(AIGuess(words, theme))
        return guesses

    def get_initial_guesses(self) -> List[AIGuess]:
        """Get the initial guesses from the AI."""
        system_message = get_system_message(self.game_state)
        user_message = get_initial_user_message(self.game_state)
        chat_builder = OpenAIChatBuilder()
        chat_builder = chat_builder.with_message(system_message)
        chat_builder = chat_builder.with_message(user_message)
        chat = OpenAIChat(chat_builder)
        assistant_response = chat.get_response(self.model)
        chat_builder = chat_builder.with_message(assistant_response)
        return self.__convert_to_json_and_parse(chat_builder)
