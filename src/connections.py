from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import time
from typing import List, Dict
from game_state import AttemptResultStatus

URL_PREFIX = "https://connections.swellgarfo.com/nyt/"
SECONDS_TO_WAIT_AFTER_CLICK = 0.3
VALID_WORDS_PARENT_CLASS_PREFIX = "HomePage_words-wrap"


class Connections:
    def __init__(self, browser: WebDriver, game_id: int):
        self.browser = browser
        self.__navigate_to_game(game_id)
        self.__load_buttons()

    def __navigate_to_game(self, game_id: int):
        url = getGameUrl(game_id)
        self.browser.get(url)
        # TODO: replace this by a wait for the page to load
        time.sleep(3)

    def __load_buttons(self):
        self.words_to_button_elements: Dict[str, WebElement] = {}
        for button in self.browser.find_elements(By.CSS_SELECTOR, "button"):
            if not isButtonWordForGame(button):
                continue
            self.words_to_button_elements[button.text] = button
        self.submit_button = getButtonWithText(self.browser, "Submit")
        self.clear_button = getButtonWithText(self.browser, "Clear")
        self.toastify = getDivWithClassSubstring(self.browser, "Toastify")

    def __is_one_away_message_visible(self):
        # return if toastify has children
        is_visible = len(self.toastify.find_elements(By.XPATH, "./*")) > 0
        # if its visible, wait for it to disappear
        if not is_visible:
            return False
        while len(self.toastify.find_elements(By.XPATH, "./*")) > 0:
            time.sleep(0.5)
        return True

    def get_remaining_words(self) -> List[str]:
        buttons = self.browser.find_elements(By.CSS_SELECTOR, "button")

        remaining_words = []
        for button in buttons:
            if not isButtonWordForGame(button):
                continue
            remaining_words.append(button.text)
            self.words_to_button_elements[button.text] = button
        return remaining_words

    def get_number_of_correct_groups(self) -> int:
        correct_div = getDivWithClassSubstring(
            self.browser, "HomePage_correct-answers-wrap"
        )
        # return number of children of correct_div
        return len(correct_div.find_elements(By.XPATH, "./*"))

    def attempt_group(self, words: List[str]) -> AttemptResultStatus:
        if len(words) != 4:
            raise ValueError("Must have 4 words in a group")
        current_number_of_correct_groups = self.get_number_of_correct_groups()
        for word in words:
            word_button = self.words_to_button_elements[word]
            word_button.click()
            waitAfterClick()
        self.submit_button.click()
        waitAfterClick()
        if self.__is_one_away_message_visible():
            return AttemptResultStatus.ONE_AWAY
        new_number_of_correct_groups = self.get_number_of_correct_groups()
        new_group_formed = (
            new_number_of_correct_groups > current_number_of_correct_groups
        )
        if new_group_formed:
            return AttemptResultStatus.SUCCESS
        return AttemptResultStatus.FAILURE


def waitAfterClick():
    time.sleep(SECONDS_TO_WAIT_AFTER_CLICK)


def getGameUrl(game_id: int):
    return f"{URL_PREFIX}{game_id}"


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
