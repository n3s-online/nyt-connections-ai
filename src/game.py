from connections import Connections
from game_state import GameState, AttemptResult, AttemptResultStatus
from typing import List


class Game:
    def __init__(self, connections: Connections):
        self.connections = connections
        initial_words = self.connections.get_remaining_words()
        self.game_state = GameState(initial_words)

    def attempt_group(self, words: List[str]) -> AttemptResult:
        result = self.connections.attempt_group(words)
        attempt_result = self.game_state.record_attempt(words, result)
        if attempt_result.result == AttemptResultStatus.SUCCESS:
            remaining_words = self.connections.get_remaining_words()
            self.game_state.update_remaining_words(remaining_words)
        return attempt_result

    def get_game_state(self) -> GameState:
        return self.game_state
