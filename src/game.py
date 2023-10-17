from selenium.webdriver.common.by import By
from connections import Connections


# EXAMPLE_VALID_WORDS = ['CUFF', 'TIE', 'TAB', 'RELATION', 'LAUNDRY', 'BUTTON', 'COLLAR', 'LINK', 'MARTINI', 'JOKE', 'DOZEN', 'BOND', 'BOOKMARK', 'HISTORY', 'POCKET', 'WINDOW']


class Game:
    def __init__(self, connections: Connections):
        self.connections = connections
        print(self.connections.getGameState())
        self.connections.attemptGroup(["BOOKMARK", "HISTORY", "TAB", "WINDOW"])
        print(self.connections.getGameState())
        self.connections.attemptGroup(["BOND", "LINK", "RELATION", "TIE"])
        print(self.connections.getGameState())
        self.connections.attemptGroup(["CUFF", "BUTTON", "POCKET", "COLLAR"])
        print(self.connections.getGameState())
        self.connections.attemptGroup(["DOZEN", "JOKE", "MARTINI", "LAUNDRY"])
        print(self.connections.getGameState())
