from connections import Connections
from game_state import GameState, Attempt
from typing import List


class Game:
    def __init__(self, connections: Connections):
        self.connections = connections
        words = connections.loadRemainingWords()
        self.game_state = GameState()
        self.game_state.setRemainingWords(words)

    def playTurn(self, words: List[str]):
        attempt_result = self.connections.attemptGroup(words)
        attempt = Attempt(words, attempt_result)
        self.game_state.addAttempt(attempt)
        words = self.connections.loadRemainingWords()
        self.game_state.setRemainingWords(words)
