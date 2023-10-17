from selenium.webdriver.common.by import By
from connections import Connections


class Game:
    def __init__(self, connections: Connections):
        self.connections = connections
        valid_words = self.connections.getValidWords()
        print(valid_words)
        for word in ["BOOKMARK", "HISTORY", "TAB", "WINDOW"]:
            self.connections.clickWord(word)
        self.connections.submit()
