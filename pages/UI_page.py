from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MainPage:
    URL = "https://www.chitai-gorod.ru/"


    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
      
    def open(self)-> None:
        '''Открывает главную страницу'''
        self.driver.get(self.URL)
