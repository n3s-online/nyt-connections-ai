"""Class for representing the state of a game of Connections."""

from typing import List, Set
from game_types.game_types import AttemptResult, AttemptResultStatus, GameStatus
from utils.attempt_utils import get_number_of_correct_groups

ALLOWED_MISTAKES = 3


class GameState:
    """Class for representing the state of a game of Connections."""

    def __init__(self, game_id: int, initial_words: Set[str]):
        self.game_id = game_id
        self.remaining_words: Set[str] = initial_words
        self.group_attempt_history: List[AttemptResult] = []
        self.player_quit: bool = False

    def record_attempt(
        self, attempt_words: Set[str], result: AttemptResultStatus
    ) -> AttemptResult:
        """Record an attempt to group the given words."""
        attempt = AttemptResult(attempt_words, result)
        self.group_attempt_history.append(attempt)
        return attempt

    def quit(self):
        print("Quitting game")
        self.player_quit = True

    def get_game_status(self) -> GameStatus:
        """Return the status of the game."""
        correct_groups = get_number_of_correct_groups(self.group_attempt_history)
        number_of_attempts = len(self.group_attempt_history)
        mistakes = number_of_attempts - correct_groups
        if mistakes > ALLOWED_MISTAKES or self.player_quit:
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

    def get_turn_number(self) -> int:
        """Return the number of the current turn."""
        return len(self.group_attempt_history) + 1

    def get_attempts(self) -> List[AttemptResult]:
        """Return the list of attempts."""
        return self.group_attempt_history

    def get_game_id(self) -> int:
        """Return the game id."""
        return self.game_id

    def __str__(self) -> str:
        attempt_history_string = (
            "\nAttempts:" if len(self.group_attempt_history) > 0 else ""
        )
        for i, attempt in enumerate(self.group_attempt_history):
            attempt_history_string += f"\n\t{i+1}. {attempt.pretty_str()}"
        return f"==Game State==\nStatus: {self.get_game_status()}\nRemaining Words: {self.remaining_words}{attempt_history_string}"
