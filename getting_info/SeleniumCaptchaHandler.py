from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


class MonkeyWorker:
    def __init__(self):
        options = Options()
        options.add_experimental_option("detach", True)
        self.base_URL = "https://www.python.org/"
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.action = webdriver.ActionChains(self.driver)
        self.driver.maximize_window()

        self.driver.get(self.base_URL)

    def process_image(self, url):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url)


if __name__ == '__main__':
    monkey = MonkeyWorker()
    monkey.process_image("https://api.vk.com/captcha.php?sid=188340706040&s=1")