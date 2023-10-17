"""
# Filename: main.py
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from game import Game

# Choose Chrome Browser
browser = webdriver.Chrome()

# Create a new game
game = Game(browser, 100)

# Extract description from page and print
# description = browser.find_element(By.NAME, "description").get_attribute("content")
# print(f"{description}")

# Wait for 10 seconds
time.sleep(10)
browser.quit()
