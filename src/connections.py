from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import time

URL_PREFIX = "https://connections.swellgarfo.com/nyt/"


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

    def clickWord(self, word: str):
        print("Clicking word: ", word)
        button = self.valid_words_to_elements[word]
        button.click()

    def submit(self):
        self.submit_button.click()

    def clear(self):
        self.clear_button.click()
