"""Main file. Run this file to start the bot."""

import time
import os
from selenium import webdriver
import openai

from dotenv import load_dotenv

from connections import Connections
from player import Player


# Environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("OPENAI_API_KEY environment variable not set.")
openai.api_key = OPENAI_API_KEY

GAME_ID = 147

# Choose Chrome Browser
browser = webdriver.Chrome()
connections = Connections(browser, GAME_ID)

# Create a new player
player = Player(GAME_ID, connections, OPENAI_API_KEY)
player.play_game()

# Wait for 10 seconds
time.sleep(5)
browser.quit()
