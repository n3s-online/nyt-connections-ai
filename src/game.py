from selenium.webdriver.remote.webdriver import WebDriver


class Game:
    def __init__(self, browser: WebDriver, game_id: int):
        url = f"https://connections.swellgarfo.com/nyt/{game_id}"
        browser.get(url)
