from selenium.webdriver.common.by import By
from connections import Connections
from game_state import GameState


class Game:
    def __init__(self, connections: Connections):
        self.connections = connections
        words = connections.loadRemainingWords()
        self.game_state = GameState()
        self.game_state.setRemainingWords(words)
        self.playTurn(["BOOKMARK", "HISTORY", "TAB", "WINDOW"])
        self.playTurn(["BOND", "LINK", "RELATION", "TIE"])
        self.playTurn(["CUFF", "BUTTON", "POCKET", "COLLAR"])
        self.playTurn(["DOZEN", "JOKE", "MARTINI", "LAUNDRY"])

    def playTurn(self, words: list):
        self.connections.attemptGroup(words)
        words = self.connections.loadRemainingWords()
        self.game_state.setRemainingWords(words)
        print(self.connections.getGameState())
