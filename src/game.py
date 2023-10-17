from selenium.webdriver.common.by import By
from connections import Connections


# EXAMPLE_VALID_WORDS = ['CUFF', 'TIE', 'TAB', 'RELATION', 'LAUNDRY', 'BUTTON', 'COLLAR', 'LINK', 'MARTINI', 'JOKE', 'DOZEN', 'BOND', 'BOOKMARK', 'HISTORY', 'POCKET', 'WINDOW']


class Game:
    def __init__(self, connections: Connections):
        self.connections = connections
        valid_words = self.connections.getValidWords()
        print(valid_words)
        # self.connections.attemptGroup(["BOOKMARK", "HISTORY", "TAB", "WINDOW"])
        self.connections.attemptGroup(["BOOKMARK", "HISTORY", "TAB", "TIE"])
