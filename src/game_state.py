from typing import List
from connections import AttemptResult


class Attempt:
    def __init__(self, words: List[str], result: AttemptResult):
        self.words = words
        self.result = result

    def __str__(self):
        return f"Attempt(words={self.words}, result={self.result})"


class GameState:
    def __init__(self):
        self.remaining_words: List[str] = []
        self.attempt_history: List[Attempt] = []

    def getRemainingWords(self) -> List[str]:
        return self.remaining_words

    def setRemainingWords(self, words: List[str]):
        self.remaining_words = words

    def getAttemptHistory(self) -> List[Attempt]:
        return self.attempt_history

    def addAttempt(self, attempt: Attempt):
        self.attempt_history.append(attempt)
