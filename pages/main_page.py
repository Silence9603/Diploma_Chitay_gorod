from .base_page import BasePage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import allure


class MainPage(BasePage):
    # Локаторы
    #SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], .search-input, input[placeholder*='Поиск']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Поиск'], .search-button")
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon, [data-testid='cart']")
    CART_COUNTER = (By.CSS_SELECTOR, ".cart-counter, .cart-count")
    CITY_SELECTOR = (By.CSS_SELECTOR, ".city-selector, .header-city, [data-testid='city']")
    BOOKS_SECTION = (By.CSS_SELECTOR, ".books-section, .product-grid, .catalog-grid")
    FIRST_BOOK = (By.CSS_SELECTOR, ".product-card:first-child, .book-item:first-child")
    PAGE_TITLE = (By.TAG_NAME, "h1")
    BANNER_CAROUSEL = (By.CSS_SELECTOR, ".banner-carousel, .main-slider")
    SEARCH_INPUT = (By.XPATH, '//input[@id="app-search"]')
    TEXT_SEARCH_RESULT = (By.XPATH, "//h1[@class='search-title__head' and contains(text(), 'Результаты поиска')]")
    BOOK_TITLE = (By.XPATH, '//a[@class="product-card__title"]')

    #Адреса

    URL = "https://www.chitai-gorod.ru/"

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверка загрузки главной страницы")
    def is_page_loaded(self):
        """Проверка, что главная страница загрузилась"""
        return (self.is_element_visible(self.SEARCH_INPUT) and
                self.is_element_visible(self.CITY_SELECTOR) and
                self.is_element_visible(self.BOOKS_SECTION))

    @allure.step("Получение заголовка страницы")
    def get_page_title(self):
        """Получение текста H1 заголовка"""
        return self.get_text(self.PAGE_TITLE) if self.is_element_visible(self.PAGE_TITLE) else ""

    @allure.step("Получение текущего города")
    def get_current_city(self):
        """Получение текста текущего города"""
        return self.get_text(self.CITY_SELECTOR).strip()

    @allure.step("Проверка наличия книг на странице")
    def has_books_displayed(self):
        """Проверка, что на странице отображаются книги"""
        return self.is_element_visible(self.FIRST_BOOK, timeout=5)

    @allure.step("Проверка счетчика корзины")
    def get_cart_count(self):
        """Получение количества товаров в корзине"""
        if self.is_element_visible(self.CART_COUNTER, timeout=2):
            return int(self.get_text(self.CART_COUNTER))
        return 0

    def open_main_page(self)-> None:
        '''Открывает главную страницу'''
        self.driver.get(self.URL)

    def enter_title(self, title: str) -> None:
        '''Печатает название книги в строку поиска'''
        input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        input.clear()
        input.send_keys(title)
        input.send_keys(Keys.RETURN)

    def is_search_result_page(self):
        '''Проверяет, открылась ли страница с результатами поиска'''
        assert self.wait.until(EC.presence_of_element_located(self.TEXT_SEARCH_RESULT))

    def get_search_result(self):
        '''Возвращает список найденных книг'''
        books = self.find_element(self.BOOK_TITLE)
