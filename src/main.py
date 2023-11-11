"""Main file. Run this file to start the bot."""

import time
import os
from selenium import webdriver
import openai

from dotenv import load_dotenv

from connections import Connections
from player import Player
from single_ai_guess_player import SingleAiGuessPlayer
from results_tracker import ResultsTracker


# Environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("OPENAI_API_KEY environment variable not set.")
openai.api_key = OPENAI_API_KEY
MODEL_TO_USE = "gpt-4-1106-preview"


# Choose Chrome Browser
browser = webdriver.Chrome()

GAME_IDS = range(58, 153)


def run_game(game_id: int):
    result_tracker = ResultsTracker("gpt-4-1106-preview_single_guess_v2")
    if result_tracker.already_has_result(game_id):
        print(f"Game {game_id} already has result. Skipping.")
        return
    print(f"Running game {game_id}")
    connections = Connections(browser, game_id)

    # Create a new player
    # player = Player(GAME_ID, connections, MODEL_TO_USE)
    player = SingleAiGuessPlayer(game_id, connections, MODEL_TO_USE)
    game_result = player.play_game()
    # Save result
    result_tracker.save_result(game_result)


for game_id in GAME_IDS:
    run_game(game_id)

# Wait for 5 seconds
time.sleep(5)
browser.quit()
