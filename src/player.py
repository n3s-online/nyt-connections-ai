from connections import Connections
from game_state import GameState, AttemptResult
from game import Game
from ai import AI
from typing import List


class Player:
    def __init__(self, connections: Connections, open_api_key: str):
        self.game = Game(connections)
        self.open_api_key = open_api_key

    def play_turn(self):
        print(f"====Player turn {self.game.get_game_state().get_turn_number()}====")
        print(self.game.get_game_state())
        guess = self.__get_guess()
        print("==Connections Result==")
        result = self.game.attempt_group(guess)
        print(result.pretty_str(), "\n\n")

    def __get_guess(self) -> List[str]:
        remaining_words = self.game.get_game_state().get_remaining_words()
        if len(remaining_words) == 4:
            print("==Logic (4 words remaining)==")
            return remaining_words
        print("==AI guess==")
        ai = AI(self.open_api_key)
        ai_guesses = ai.get_words(self.game.get_game_state())
        for guess in ai_guesses:
            print(guess)
        ai_guess = ai_guesses[0]
        return ai_guess.get_words()

    def play_game(self):
        while not self.game.get_game_state().is_game_over():
            self.play_turn()
        print("Game over!")
        print(self.game.get_game_state().get_game_status())