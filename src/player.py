from connections import Connections
from game_state import GameState, AttemptResult
from game import Game
from ai import AI, AIResponse
from typing import List, Set


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
        remaining_words = self.game.get_game_state().get_remaining_words()
        if len(remaining_words) == 4:
            print("==Logic (4 words remaining)==")
            return remaining_words
        print("==AI guess==")
        ai = AI(self.open_api_key)
        ai_guesses: List[AIResponse] = []
        relevant_attempt = (
            self.game.get_game_state().get_most_recent_attempt_where_all_words_still_remain()
        )
        if relevant_attempt != None:
            print(f"Using relevant attempt for context: {relevant_attempt}")
        ai_guesses = ai.get_initial_guesses(remaining_words, relevant_attempt)
        for guess in ai_guesses:
            print(guess)
        ai_guess = ai_guesses[0]
        previous_attempt = self.game.get_game_state().get_previous_attempt_for_words(
            ai_guess.get_words()
        )
        if previous_attempt == None:
            return ai_guess.get_words()
        print("==AI guess 2 (prev already attempted)==")
        ai_guesses = ai.get_modified_guess(remaining_words, previous_attempt)
        for guess in ai_guesses:
            print(guess)
        ai_guess = ai_guesses[0]
        return ai_guess.get_words()

    def play_game(self):
        while not self.game.get_game_state().is_game_over():
            self.play_turn()
        print(self.game.get_game_state().get_game_over_message())
