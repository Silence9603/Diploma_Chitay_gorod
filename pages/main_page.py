from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class MainPage(BasePage):
    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], .search-input, input[placeholder*='Поиск']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Поиск'], .search-button")
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon, [data-testid='cart']")
    CART_COUNTER = (By.CSS_SELECTOR, ".cart-counter, .cart-count")
    CITY_SELECTOR = (By.CSS_SELECTOR, ".city-selector, .header-city, [data-testid='city']")
    BOOKS_SECTION = (By.CSS_SELECTOR, ".books-section, .product-grid, .catalog-grid")
    FIRST_BOOK = (By.CSS_SELECTOR, ".product-card:first-child, .book-item:first-child")
    PAGE_TITLE = (By.TAG_NAME, "h1")
    BANNER_CAROUSEL = (By.CSS_SELECTOR, ".banner-carousel, .main-slider")

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
