from .base_page_ui import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import allure


class MainPage(BasePage):
    # Локаторы
    CHOOSE_CITY_BUTTON = (By.CSS_SELECTOR, "button.header-location[aria-expanded='true']")
    CHOOSE_CITY_MODAL = (By.CSS_SELECTOR, "div[class*='city-modal'], div[class*='location-modal']")
    CART_ICON = (By.XPATH, "//span[@class='header-controls__icon-wrapper']")
    CART_COUNTER = (By.CSS_SELECTOR, ".cart-counter, .cart-count")
    CITY_SELECTOR = (By.XPATH, "//button[@class='header-location']")
    FIRST_BOOK = (By.CSS_SELECTOR, ".product-card:first-child, .book-item:first-child")
    PAGE_TITLE = (By.TAG_NAME, "h1")
    SEARCH_INPUT = (By.XPATH, '//input[@id="app-search"]')
    TEXT_SEARCH_RESULT = (By.XPATH, "//h1[@class='search-title__head' and contains(text(), 'Результаты поиска')]")
    BOOK_TITLE = (By.XPATH, '//a[@class="product-card__title"]')
    CATALOG_BUTTON = (By.XPATH, "//button[contains(@class, 'catalog-btn') and contains(text(), 'Каталог')]")
    CATALOG_MENU_VISIBLE = (By.CSS_SELECTOR, "div.vfm__content.ui-modal__content.ui-modal__content--view-sideLeft")
    BOOKS_MENU = (By.XPATH, "//span[contains(@class, 'categories-level-menu__item-title') and text()='Книги']")

    # Адреса

    URL = "https://www.chitai-gorod.ru/"

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверка загрузки главной страницы")
    def is_page_loaded(self):
        """Проверка, что главная страница загрузилась"""
        search_visible = self.is_element_visible(self.SEARCH_INPUT)
        city_visible = self.is_element_visible(self.CITY_SELECTOR)
        cart_visible = self.is_element_visible(self.CART_ICON)

        # Для отладки - выводим информацию
        if not search_visible:
            print("Поле поиска НЕ видно")
        if not city_visible:
            print("Селектор города НЕ виден")
        if not cart_visible:
            print("Иконка корзины НЕ видна")

        return search_visible and city_visible and cart_visible

    @allure.step("Получение заголовка страницы")
    def get_page_title(self):
        """Получение текста H1 заголовка"""
        return self.get_text(self.PAGE_TITLE) if self.is_element_visible(self.PAGE_TITLE) else ""

    @allure.step("Получение текущего города")
    def get_current_city(self):
        """Получение текста текущего города"""
        return self.get_text(self.CITY_SELECTOR).strip()

    @allure.step("Закрыть окно выбора города")
    def close_city_modal(self):
        """Нажимаем кнопку свернуть, если окно открыто"""
        try:
            # Ждём появления активной кнопки (окно открыто)
            button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.header-location[aria-expanded='true']"))
            )
            button.click()
            allure.attach("Окно выбора города закрыто", name="Modal closed")
        except TimeoutException:
            pass  # Окна нет — ничего не делаем

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

    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        """Открывает главную страницу и обрабатывает попап с городом"""
        self.driver.get(self.URL)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        # Обрабатываем попап с городом
        self.close_city_modal()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )

    def enter_title(self, title: str) -> None:
        '''Печатает название книги в строку поиска'''
        input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
        input.clear()
        input.send_keys(title)
        # Ждём, пока текст появился
        self.wait.until(EC.text_to_be_present_in_element_value(self.SEARCH_INPUT, title))
        # Небольшая пауза для обработки событий
        self.wait.until(lambda driver: input.get_attribute('value') == title)
        # Отправляем Enter
        input.send_keys(Keys.RETURN)

    def is_search_result_page(self):
        '''Проверяет, открылась ли страница с результатами поиска'''
        assert self.wait.until(EC.presence_of_element_located(self.TEXT_SEARCH_RESULT),
                               message="Элемент результатов поиска не найден")

    def get_search_result(self) -> str:
        '''Возвращает список найденных книг'''
        books = self.find_element(self.BOOK_TITLE)
        return books.text
