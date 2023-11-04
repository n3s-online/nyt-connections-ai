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


ALLOWED_MISTAKES = 3


class GameState(Enum):
    IN_PROGRESS = 1
    WON = 2
    LOST = 3


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
        self.attempts = 0
        self.loadRemainingWords()
        self.loadButtons()
        self.loadToastify()

    def getGameState(self) -> GameState:
        correct_groups = self.getNumberOfCorrectGroups()
        mistakes = self.attempts - correct_groups
        if mistakes > ALLOWED_MISTAKES:
            return GameState.LOST
        elif correct_groups == 4:
            return GameState.WON
        return GameState.IN_PROGRESS

    def loadRemainingWords(self) -> List[str]:
        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button")

        self.remaining_words = []
        self.remaining_words_to_elements = {}
        for button in buttons:
            if not isButtonWordForGame(button):
                continue
            self.remaining_words.append(button.text)
            self.remaining_words_to_elements[button.text] = button
        return self.remaining_words

    def loadButtons(self):
        self.submit_button = getButtonWithText(self.browser, "Submit")
        self.clear_button = getButtonWithText(self.browser, "Clear")

    def loadToastify(self):
        self.toastify = getDivWithClassSubstring(self.browser, "Toastify")

    def isOneAwayMessageVisible(self):
        # return if toastify has children
        is_visible = len(self.toastify.find_elements(By.XPATH, "./*")) > 0
        # if its visible, wait for it to disappear
        if not is_visible:
            return False
        while len(self.toastify.find_elements(By.XPATH, "./*")) > 0:
            time.sleep(0.5)
        return True

    def getNumberOfCorrectGroups(self):
        correct_div = getDivWithClassSubstring(
            self.browser, "HomePage_correct-answers-wrap"
        )
        # return number of children of correct_div
        return len(correct_div.find_elements(By.XPATH, "./*"))

    def clickWord(self, word: str):
        button = self.remaining_words_to_elements[word]
        button.click()
        waitAfterClick()

    def submit(self):
        self.submit_button.click()
        waitAfterClick()

    def clear(self):
        self.clear_button.click()
        waitAfterClick()

    def attemptGroup(self, words: List[str]) -> AttemptResult:
        current_groups = self.getNumberOfCorrectGroups()
        self.clear()
        for word in words:
            self.clickWord(word)
        self.submit()
        time.sleep(1)
        self.attempts += 1
        if self.isOneAwayMessageVisible():
            return AttemptResult.ONE_AWAY

        new_groups = self.getNumberOfCorrectGroups()
        new_group_formed = new_groups > current_groups

        if new_group_formed:
            self.loadRemainingWords()
            return AttemptResult.SUCCESS
        else:
            return AttemptResult.FAILURE
