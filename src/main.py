import time
from selenium import webdriver

from dotenv import load_dotenv
import os

from ai import AI
from connections import Connections
from player import Player


# Environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ai = AI(OPENAI_API_KEY)

# Choose Chrome Browser
browser = webdriver.Chrome()
connections = Connections(browser, 100)

# Create a new player
player = Player(connections, ai)
player.play_game()

# Wait for 10 seconds
time.sleep(5)
browser.quit()
