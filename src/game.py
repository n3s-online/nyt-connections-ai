"""Wrapper class for the Connections selenium class and the GameState class."""

from typing import Set
from connections import Connections
from game_state import GameState, AttemptResult, AttemptResultStatus


class Game:
    """Wrapper class for the Connections selenium class and the GameState class."""

    def __init__(self, game_id: int, connections: Connections):
        self.connections = connections
        initial_words = self.connections.get_remaining_words()
        self.game_state = GameState(game_id, initial_words)

    def attempt_group(self, words: Set[str]) -> AttemptResult:
        """Attempt to group the given words."""
        result = self.connections.attempt_group(words)
        attempt_result = self.game_state.record_attempt(words, result)
        if attempt_result.result == AttemptResultStatus.SUCCESS:
            remaining_words = self.connections.get_remaining_words()
            self.game_state.update_remaining_words(remaining_words)
        return attempt_result

    def shuffle(self):
        """Shuffle words"""
        self.connections.shuffle()
        remaining_words = self.connections.get_remaining_words()
        self.game_state.update_remaining_words(remaining_words)

    def get_game_state(self) -> GameState:
        """Return the game state."""
        return self.game_state
