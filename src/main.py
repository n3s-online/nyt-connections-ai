"""
# Filename: main.py
"""

import time
from selenium import webdriver

from dotenv import load_dotenv
import os

from connections import Connections, GameState
from game import Game
from ai import AI

# Environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ai = AI(OPENAI_API_KEY)

# Choose Chrome Browser
browser = webdriver.Chrome()
connections = Connections(browser, 100)

# Create a new game
game = Game(connections)


def gameLoop():
    ai_responses = ai.getWords(game.game_state)
    ai_response = ai_responses[0]
    game.playTurn(ai_response.words)


while connections.getGameState() == GameState.IN_PROGRESS:
    gameLoop()

print("Final game result: " + str(connections.getGameState()))
print("Number of total guesses: " + str(connections.attempts))

# Wait for 10 seconds
time.sleep(5)
browser.quit()
