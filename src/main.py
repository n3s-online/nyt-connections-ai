"""
# Filename: main.py
"""

import time
from selenium import webdriver

from connections import Connections
from game import Game


# Choose Chrome Browser
browser = webdriver.Chrome()

connections = Connections(browser, 100)

# Create a new game
game = Game(connections)

# Wait for 10 seconds
time.sleep(5)
browser.quit()
