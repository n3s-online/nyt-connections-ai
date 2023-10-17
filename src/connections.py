from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import time
from typing import List
from enum import Enum

URL_PREFIX = "https://connections.swellgarfo.com/nyt/"

SECONDS_TO_WAIT_AFTER_CLICK = 0.3


def waitAfterClick():
    time.sleep(SECONDS_TO_WAIT_AFTER_CLICK)


def getGameUrl(game_id: int):
    return f"{URL_PREFIX}{game_id}"


VALID_WORDS_PARENT_CLASS_PREFIX = "HomePage_words-wrap"


def isButtonWordForGame(button: WebElement):
    parent = button.find_element(By.XPATH, "..")
    parent_class = parent.get_attribute("class")
    return parent_class.startswith(VALID_WORDS_PARENT_CLASS_PREFIX)


def getButtonWithText(browser: WebDriver, text: str):
    text_div = browser.find_element(By.XPATH, f"//div[text()='{text}']")
    # get closest parent to this div that is a button
    return text_div.find_element(By.XPATH, "ancestor::button")


def getDivWithClassSubstring(browser: WebDriver, class_substring: str):
    return browser.find_element(
        By.XPATH, f"//div[contains(@class, '{class_substring}')]"
    )


class AttemptResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    ONE_AWAY = 3


class Connections:
    def __init__(self, browser: WebDriver, game_id: int):
        self.browser = browser
        self.game_id = game_id
        self.navigateToGame()

    def navigateToGame(self):
        url = getGameUrl(self.game_id)
        self.browser.get(url)
        # TODO: replace this by a wait for the page to load
        time.sleep(3)
        self.loadData()

    def loadData(self):
        self.getValidWords()
        self.loadButtons()
        self.loadToastify()

    def getValidWords(self):
        if hasattr(self, "valid_words"):
            return self.valid_words
        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button")

        self.valid_words = []
        self.valid_words_to_elements = {}
        for button in buttons:
            if not isButtonWordForGame(button):
                continue
            self.valid_words.append(button.text)
            self.valid_words_to_elements[button.text] = button
        return self.valid_words

    def loadButtons(self):
        self.submit_button = getButtonWithText(self.browser, "Submit")
        self.clear_button = getButtonWithText(self.browser, "Clear")

    def loadToastify(self):
        self.toastify = getDivWithClassSubstring(self.browser, "Toastify")

    def isOneAwayMessageVisible(self):
        # return if toastify has children
        return len(self.toastify.find_elements(By.XPATH, "./*")) > 0

    def getNumberOfCorrectGroups(self):
        correct_div = getDivWithClassSubstring(
            self.browser, "HomePage_correct-answers-wrap"
        )
        # return number of children of correct_div
        return len(correct_div.find_elements(By.XPATH, "./*"))

    def clickWord(self, word: str):
        print("Clicking word: ", word)
        button = self.valid_words_to_elements[word]
        button.click()
        waitAfterClick()

    def submit(self):
        self.submit_button.click()
        waitAfterClick()

    def clear(self):
        self.clear_button.click()
        waitAfterClick()

    def attemptGroup(self, words: List[str]) -> AttemptResult:
        print("Current number of correct groups: ", self.getNumberOfCorrectGroups())
        print("Attempting group: ", words)
        current_groups = self.getNumberOfCorrectGroups()
        self.clear()
        for word in words:
            self.clickWord(word)
        self.submit()
        if self.isOneAwayMessageVisible():
            print("One away!")
            return AttemptResult.ONE_AWAY

        new_groups = self.getNumberOfCorrectGroups()
        new_group_formed = new_groups > current_groups

        if new_group_formed:
            print("New group formed!")
            return AttemptResult.SUCCESS
        else:
            print("No new group formed.")
            return AttemptResult.FAILURE
