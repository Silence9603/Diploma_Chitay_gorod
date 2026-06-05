from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import allure


class CityModal(BasePage):
    # Локаторы
    MODAL_WINDOW = (By.CSS_SELECTOR, ".city-modal, .modal, [role='dialog']")
    SEARCH_CITY_INPUT = (By.CSS_SELECTOR, "input[placeholder*='город'], input[placeholder*='населен']")
    CITY_LIST = (By.CSS_SELECTOR, ".city-list, .cities-list")
    CITY_ITEM = (By.CSS_SELECTOR, ".city-item, .cities-list li")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Подтвердить'], .confirm-city-btn")
    CLOSE_BUTTON = (By.CSS_SELECTOR, ".modal-close, .close-btn")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Открытие модального окна выбора города")
    def open_city_modal(self, main_page):
        """Открыть модальное окно выбора города"""
        main_page.click(main_page.CITY_SELECTOR)
        self.wait.until(lambda d: self.is_modal_visible())

    @allure.step("Проверка видимости модального окна")
    def is_modal_visible(self):
        """Проверка, что модальное окно отображается"""
        return self.is_element_visible(self.MODAL_WINDOW, timeout=3)

    @allure.step("Поиск города: {city_name}")
    def search_city(self, city_name):
        """Поиск города в модальном окне"""
        search_input = self.find_element(self.SEARCH_CITY_INPUT)
        search_input.clear()
        search_input.send_keys(city_name)
        search_input.send_keys(Keys.RETURN)

    @allure.step("Выбор города из списка")
    def select_city(self, city_name):
        """Выбор конкретного города из результатов поиска"""
        cities = self.driver.find_elements(*self.CITY_ITEM)
        for city in cities:
            if city_name.lower() in city.text.lower():
                city.click()
                return True
        return False

    @allure.step("Подтверждение выбора города")
    def confirm_city_selection(self):
        """Нажать кнопку подтверждения"""
        self.click(self.CONFIRM_BUTTON)

    @allure.step("Закрытие модального окна")
    def close_modal(self):
        """Закрыть модальное окно"""
        if self.is_element_visible(self.CLOSE_BUTTON, timeout=2):
            self.click(self.CLOSE_BUTTON)

    @allure.step("Смена города на {city_name}")
    def change_city(self, main_page, city_name):
        """Полный процесс смены города"""
        self.open_city_modal(main_page)
        self.search_city(city_name)
        self.select_city(city_name)
        self.confirm_city_selection()
        self.wait.until(lambda d: not self.is_modal_visible())
