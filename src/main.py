"""
# Filename: main.py
"""

import time
from selenium import webdriver

from dotenv import load_dotenv
import os

from connections import Connections
from game import Game

# Environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Choose Chrome Browser
browser = webdriver.Chrome()
connections = Connections(browser, 100)

# Create a new game
game = Game(connections)

# Wait for 10 seconds
time.sleep(5)
browser.quit()
