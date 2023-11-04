from connections import Connections
from game_state import GameState, AttemptResult
from game import Game
from ai import AI


class Player:
    def __init__(self, connections: Connections, ai: AI):
        self.game = Game(connections)
        self.ai = ai

    def play_turn(self):
        print(f"====Player turn {self.game.get_game_state().get_turn_number()}====")
        print(self.game.get_game_state())
        ai_guesses = self.ai.get_words(self.game.get_game_state())
        print("==AI guesses==")
        for guess in ai_guesses:
            print(guess)
        ai_guess = ai_guesses[0]
        ai_guess_words = ai_guess.get_words()
        print("==Connections Result==")
        result = self.game.attempt_group(ai_guess_words)
        print(result.pretty_str(), "\n\n")

    def play_game(self):
        while not self.game.get_game_state().is_game_over():
            self.play_turn()
        print("Game over!")
        print(self.game.get_game_state())
