""" Player which attempts a single AI guess for playing a game of Connections """

from typing import List, Set
from connections import Connections
from game import Game
from ai import AI, AIGuess
from results_tracker import GameResult
from utils.attempt_utils import get_game_over_message, get_number_of_correct_groups


class SingleAiGuessPlayer:
    def __init__(self, game_id: int, connections: Connections, model: str):
        self.game = Game(game_id, connections)
        self.model = model

    def play_turn(self):
        print(f"====Player turn {self.game.get_game_state().get_turn_number()}====")
        print(self.game.get_game_state())

        guess = self.__get_guess()
        print("==Connections Result==")
        result = self.game.attempt_group(guess)
        print(result.pretty_str(), "\n\n")
        if len(self.ai_guesses) == 0 and not self.game.get_game_state().is_game_over():
            self.game.get_game_state().quit()

    def __get_guess(self) -> Set[str]:
        print("==AI guess==")
        if not hasattr(self, "ai_guesses"):
            ai = AI(self.game.get_game_state(), self.model)
            self.ai_guesses: List[AIGuess] = ai.get_initial_guesses()

        for guess in self.ai_guesses:
            print(guess)
        ai_guess = self.ai_guesses[0]
        self.ai_guesses = self.ai_guesses[1:]

        return ai_guess.get_words()

    def play_game(self) -> GameResult:
        game_state = self.game.get_game_state()
        while not game_state.is_game_over():
            self.play_turn()
        game_over_message = get_game_over_message(
            game_state.get_game_id(),
            game_state.get_attempts(),
            game_state.get_game_status(),
        )
        print(game_over_message)
        return GameResult(
            game_state.get_game_id(),
            get_number_of_correct_groups(game_state.get_attempts()),
            len(game_state.get_attempts()),
        )
