"""Class for representing the state of a game of Connections."""

from enum import Enum
from typing import List, Set, Union

ALLOWED_MISTAKES = 3


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


class GameState:
    """Class for representing the state of a game of Connections."""

    def __init__(self, game_id: int, initial_words: Set[str]):
        self.game_id = game_id
        self.remaining_words: Set[str] = initial_words
        self.group_attempt_history: List[AttemptResult] = []

    def record_attempt(
        self, attempt_words: Set[str], result: AttemptResultStatus
    ) -> AttemptResult:
        """Record an attempt to group the given words."""
        attempt = AttemptResult(attempt_words, result)
        self.group_attempt_history.append(attempt)
        return attempt

    def get_game_status(self) -> GameStatus:
        """Return the status of the game."""
        correct_groups = self.__get_number_of_correct_groups()
        number_of_attempts = self.__get_number_of_attempts()
        mistakes = number_of_attempts - correct_groups
        if mistakes > ALLOWED_MISTAKES:
            return GameStatus.LOST
        elif correct_groups == 4:
            return GameStatus.WON
        return GameStatus.IN_PROGRESS

    def get_remaining_words(self) -> Set[str]:
        """Return the remaining words in the game."""
        return self.remaining_words

    def update_remaining_words(self, words: Set[str]):
        """Update the remaining words in the game."""
        self.remaining_words = words

    def is_game_over(self) -> bool:
        """Returns if the game is over."""
        return self.get_game_status() != GameStatus.IN_PROGRESS

    # TODO I keep too many helper functions in this class. they should be moved to a utilty file

    def get_game_over_message(self) -> str:
        """Return a summary message for the game being over."""
        game_status = self.get_game_status()
        number_of_attempts = self.__get_number_of_attempts()
        mistakes = self.__number_of_mistakes()
        correct_groups = self.__get_number_of_correct_groups()
        game_summary = f"Game {self.game_id} over! {game_status.name} in {number_of_attempts} attempts with {mistakes} mistakes and {correct_groups} correct groups."
        for i, attempt in enumerate(self.group_attempt_history):
            game_summary += f"\n\t{i+1}. {attempt.pretty_str()}"
        return game_summary

    def get_turn_number(self) -> int:
        """Return the number of the current turn."""
        return len(self.group_attempt_history) + 1

    def was_previous_attempt_failure(self) -> int:
        """Return if the previous attempt was a failure."""
        if len(self.group_attempt_history) == 0:
            return False
        return self.group_attempt_history[-1].result == AttemptResultStatus.FAILURE

    def __str__(self) -> str:
        attempt_history_string = (
            "\nAttempts:" if len(self.group_attempt_history) > 0 else ""
        )
        for i, attempt in enumerate(self.group_attempt_history):
            attempt_history_string += f"\n\t{i+1}. {attempt.pretty_str()}"
        return f"==Game State==\nStatus: {self.get_game_status()}\nRemaining Words: {self.remaining_words}{attempt_history_string}"

    def __get_number_of_correct_groups(self) -> int:
        correct_attempt_results = filter(
            lambda attempt: attempt.result == AttemptResultStatus.SUCCESS,
            self.group_attempt_history,
        )
        return len(list(correct_attempt_results))

    def __get_number_of_attempts(self) -> int:
        return len(self.group_attempt_history)

    def __number_of_mistakes(self) -> int:
        return self.__get_number_of_attempts() - self.__get_number_of_correct_groups()
