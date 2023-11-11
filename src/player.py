""" Player class for playing a game of Connections. """

from typing import List, Set
from connections import Connections
from game import Game
from ai import AI, AIGuess
from utils.attempt_utils import get_game_over_message


class Player:
    def __init__(self, game_id: int, connections: Connections, open_api_key: str):
        self.game = Game(game_id, connections)
        self.open_api_key = open_api_key

    def play_turn(self):
        print(f"====Player turn {self.game.get_game_state().get_turn_number()}====")
        print(self.game.get_game_state())

        guess = self.__get_guess()
        print("==Connections Result==")
        result = self.game.attempt_group(guess)
        print(result.pretty_str(), "\n\n")

    def __get_guess(self) -> Set[str]:
        ai = AI(self.game.get_game_state())
        print("==AI guess==")
        ai_guesses: List[AIGuess] = ai.get_initial_guesses()
        for guess in ai_guesses:
            print(guess)
        ai_guess = ai_guesses[0]
        return ai_guess.get_words()

    def play_game(self):
        game_state = self.game.get_game_state()
        while not game_state.is_game_over():
            self.play_turn()
        game_over_message = get_game_over_message(
            game_state.get_game_id(),
            game_state.get_attempts(),
            game_state.get_game_status(),
        )
        print(game_over_message)
