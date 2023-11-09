"""Helper classes and types for interacting with OpenAI's API."""

from enum import Enum
from typing import List, Union
import openai


class OpenAIMessageType(Enum):
    """Enum for representing the type of a message."""

    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"


class OpenAIMessage:
    """Class for representing a message."""

    def __init__(self, role: OpenAIMessageType, content: str):
        self.role = role
        self.content = content

    def get_as_dict(self) -> dict:
        """Return the message as a dictionary."""
        return {"role": self.role.value, "content": self.content}

    def __str__(self):
        return f"{self.role.value}: {self.content}"

    def get_role(self) -> OpenAIMessageType:
        """Return the role of the message."""
        return self.role

    def get_content(self) -> str:
        """Return the content of the message."""
        return self.content


class OpenAIMessageFactory:
    """Factory class for creating OpenAIMessage objects."""

    @staticmethod
    def get_system_message(content: str) -> OpenAIMessage:
        """Create a system message with the given content."""
        return OpenAIMessage(OpenAIMessageType.SYSTEM, content)

    @staticmethod
    def get_user_message(content: str) -> OpenAIMessage:
        """Create a user message with the given content."""
        return OpenAIMessage(OpenAIMessageType.USER, content)

    @staticmethod
    def get_assistant_message(content: str) -> OpenAIMessage:
        """Create an assistant message with the given content."""
        return OpenAIMessage(OpenAIMessageType.ASSISTANT, content)


class OpenAIChatBuilder:
    """Class for building a chat with OpenAI's API."""

    def __init__(
        self, messages: Union[List[OpenAIMessage], "OpenAIChatBuilder", None] = None
    ):
        if isinstance(messages, OpenAIChatBuilder):
            self.messages = messages.get_messages()
        else:
            self.messages = messages or []

    def with_message(self, message: OpenAIMessage) -> "OpenAIChatBuilder":
        """Add the given message to the chat."""
        new_messages = self.messages + [message]
        return OpenAIChatBuilder(new_messages)

    def get_messages(self) -> List[OpenAIMessage]:
        """Return the messages in the chat."""
        return self.messages


class ResponseFormat(Enum):
    """Enum for representing the format of the response."""

    JSON = "json_object"
    TEXT = "text"


MODEL_TO_USE = "gpt-4-1106-preview"


def getOpenAiResponse(
    messages: List[OpenAIMessage], response_format: ResponseFormat
) -> OpenAIMessage:
    """Get a response from OpenAI's API."""
    response = openai.ChatCompletion.create(
        model=MODEL_TO_USE,
        messages=[message.get_as_dict() for message in messages],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": response_format.value},
    )
    response_content: str = response["choices"][0]["message"]["content"]  # type: ignore
    return OpenAIMessageFactory.get_assistant_message(response_content)


class OpenAIChat:
    """Class for interacting with OpenAI's API."""

    def __init__(
        self, messages_or_builder: Union[List[OpenAIMessage], OpenAIChatBuilder]
    ):
        if isinstance(messages_or_builder, OpenAIChatBuilder):
            self.messages = messages_or_builder.get_messages()
        else:
            self.messages = messages_or_builder

    def get_response(self) -> OpenAIMessage:
        """Get a response from OpenAI's API."""
        return getOpenAiResponse(self.messages, ResponseFormat.TEXT)

    def get_json_response(self) -> OpenAIMessage:
        """Get a JSON response from OpenAI's API."""
        return getOpenAiResponse(self.messages, ResponseFormat.JSON)
