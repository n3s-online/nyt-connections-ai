from enum import Enum
from typing import Set


class GameStatus(Enum):
    """Enum for representing the status of a game."""

    IN_PROGRESS = 1
    WON = 2
    LOST = 3


class AttemptResultStatus(Enum):
    """Enum for representing the status of a group attempt."""

    SUCCESS = 1
    FAILURE = 2
    ONE_AWAY = 3


class AttemptResult:
    """Class for representing the result of a group attempt."""

    def __init__(self, words: Set[str], result: AttemptResultStatus):
        self.words = words
        self.result = result

    def __str__(self):
        return f"GroupAttempt(words={self.words}, result={self.result})"

    def pretty_str(self):
        """Return a pretty string representation of the attempt."""
        return f"{self.result}: {str(self.words)}"
