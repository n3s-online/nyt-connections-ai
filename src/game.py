from connections import Connections
from game_state import GameState, Attempt
from ai import AI
from typing import List


class Game:
    def __init__(self, connections: Connections, ai: AI):
        self.connections = connections
        words = connections.loadRemainingWords()
        self.game_state = GameState()
        self.game_state.setRemainingWords(words)
        self.ai = ai

    def playTurn(self, words: List[str]):
        attempt_result = self.connections.attemptGroup(words)
        attempt = Attempt(words, attempt_result)
        self.game_state.addAttempt(attempt)
        words = self.connections.loadRemainingWords()
        self.game_state.setRemainingWords(words)

    def tick(self):
        print("=====================================")
        print("Remaining words")
        print(self.game_state.remaining_words)
        ai_responses = self.ai.getWords(self.game_state)
        print("AI responses")
        print(", ".join(map(str, ai_responses)))
        ai_response = ai_responses[0]
        print("Playing")
        print(ai_response)
        self.playTurn(ai_response.words)

    def loop(self):
        while self.connections.isInProgress():
            self.tick()
        print("Final game result: " + str(self.connections.getGameState()))
        print("Number of total guesses: " + str(self.connections.attempts))
