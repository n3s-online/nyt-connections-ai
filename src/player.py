""" Player class for playing a game of Connections. """

from typing import List, Set
from connections import Connections
from game import Game
from ai import AI, AIGuess


class Player:
    def __init__(self, game_id: int, connections: Connections, open_api_key: str):
        self.game = Game(game_id, connections)
        self.open_api_key = open_api_key

    def play_turn(self):
        print(f"====Player turn {self.game.get_game_state().get_turn_number()}====")
        if self.game.get_game_state().was_previous_attempt_failure():
            print("==Shuffling==")
            self.game.shuffle()
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
        while not self.game.get_game_state().is_game_over():
            self.play_turn()
        print(self.game.get_game_state().get_game_over_message())
