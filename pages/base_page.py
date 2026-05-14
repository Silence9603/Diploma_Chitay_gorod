from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=0.5)

    def open(self, url):
        with allure.step(f"Открыть URL: {url}"):
            self.driver.get(url)

    def find_element(self, locator):
        with allure.step(f"Поиск элемента: {locator}"):
            return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        with allure.step(f"Клик по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

    def input_text(self, locator, text):
        with allure.step(f"Ввод текста '{text}' в поле {locator}"):
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)

    def get_text(self, locator):
        with allure.step(f"Получение текста из элемента: {locator}"):
            return self.find_element(locator).text

    def is_element_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except:
            return False