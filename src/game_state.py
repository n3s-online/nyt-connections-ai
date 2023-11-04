from typing import List
from enum import Enum

ALLOWED_MISTAKES = 3


class GameStatus(Enum):
    IN_PROGRESS = 1
    WON = 2
    LOST = 3


class AttemptResultStatus(Enum):
    SUCCESS = 1
    FAILURE = 2
    ONE_AWAY = 3


class AttemptResult:
    def __init__(self, words: List[str], result: AttemptResultStatus):
        self.words = words
        self.result = result

    def __str__(self):
        return f"GroupAttempt(words={self.words}, result={self.result})"

    def pretty_str(self):
        return f"{self.result}: {str(self.words)}"


class GameState:
    def __init__(self, initial_words: List[str]):
        self.remaining_words: List[str] = initial_words
        self.group_attempt_history: List[AttemptResult] = []

    def record_attempt(
        self, attempt_words: List[str], result: AttemptResultStatus
    ) -> AttemptResult:
        attempt = AttemptResult(attempt_words, result)
        self.group_attempt_history.append(attempt)
        return attempt

    def get_game_status(self) -> GameStatus:
        correct_groups = self.__get_number_of_correct_groups()
        number_of_attempts = self.__get_number_of_attempts()
        mistakes = number_of_attempts - correct_groups
        if mistakes > ALLOWED_MISTAKES:
            return GameStatus.LOST
        elif correct_groups == 4:
            return GameStatus.WON
        return GameStatus.IN_PROGRESS

    def get_remaining_words(self) -> List[str]:
        return self.remaining_words

    def update_remaining_words(self, words: List[str]):
        self.remaining_words = words

    def is_game_over(self) -> bool:
        return self.get_game_status() != GameStatus.IN_PROGRESS

    def get_game_over_message(self) -> str:
        game_status = self.get_game_status()
        number_of_attempts = self.__get_number_of_attempts()
        mistakes = self.__number_of_mistakes()
        correct_groups = self.__get_number_of_correct_groups()
        return f"Game over! {game_status.name} in {number_of_attempts} attempts with {mistakes} mistakes and {correct_groups} correct groups."

    def get_turn_number(self) -> int:
        return len(self.group_attempt_history) + 1

    def get_previous_attempt_for_words(self, words: List[str]) -> AttemptResult:
        for attempt in self.group_attempt_history:
            if self.__does_guess_match_attempt(words, attempt):
                return attempt
        return None

    # TODO - change to helper function instead of inside of class (doesnt need access to state)
    def __does_guess_match_attempt(
        self, group: List[str], attempt: AttemptResult
    ) -> bool:
        if all(word in attempt.words for word in group):
            return True
        return False

    def __str__(self) -> str:
        attempt_history_string = (
            "\nAttempts:" if len(self.group_attempt_history) > 0 else ""
        )
        for i, attempt in enumerate(self.group_attempt_history):
            attempt_history_string += f"\n\t{i+1}. {attempt.pretty_str()}"
        return f"== Game State ==\nStatus: {self.get_game_status()}\nRemaining Words: {self.remaining_words}{attempt_history_string}"

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
