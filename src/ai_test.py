"""
# Filename: ai_test.py
# Alternative entry point for testing AI only without the connections input
"""
from dotenv import load_dotenv
import os
from ai import AI
from game_state import GameState, Attempt
from connections import AttemptResult

# Environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Fake game state
EXAMPLE_VALID_WORDS = [
    "CUFF",
    "TIE",
    "TAB",
    "RELATION",
    "LAUNDRY",
    "BUTTON",
    "COLLAR",
    "LINK",
    "MARTINI",
    "JOKE",
    "DOZEN",
    "BOND",
    "BOOKMARK",
    "HISTORY",
    "POCKET",
    "WINDOW",
]

game_state = GameState()
game_state.setRemainingWords(EXAMPLE_VALID_WORDS)
fake_attempt = Attempt(
    ["BOOKMARK", "HISTORY", "BUTTON", "WINDOW"], AttemptResult.ONE_AWAY
)
game_state.addAttempt(fake_attempt)
game_state.addAttempt(
    Attempt(["CUFF", "TIE", "COLLAR", "BUTTON"], AttemptResult.ONE_AWAY)
)
game_state.addAttempt(Attempt(["CUFF", "TIE", "COLLAR", "LINK"], AttemptResult.FAILURE))
# logging off for the night - figure out how to put these attempts into the openai prompt

# Create AI
ai = AI(OPENAI_API_KEY)

ai_responses = ai.getWords(game_state)
