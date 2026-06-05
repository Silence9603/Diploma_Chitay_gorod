from .base_page_ui import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure


class CartPage(BasePage):
    # Локаторы
    CAN_BUY = (By.XPATH, '//button[@data-testid-button-mini-product-card="canBuy"]')
    CART_COUNTER = (By.XPATH, '//div[@data-testid-indicator-header="cartCounter"]')
    DELETE_ONE_ITEM = (By.XPATH, '//button[@data-testid-button-cart="removeProduct"]')
    CLEAR_ALL_CART = (By.XPATH, '//button[@data-testid-button-cart="clearAll"]')
    EMPTY_CART_MESSAGE = (By.XPATH, '//span[@data-testid-text-stub="emptyCart"]')

    CART_URL = "https://www.chitai-gorod.ru/cart"

    @allure.step("Открытие страницы корзины")
    def open_cart_page(self):
        """Открывает страницу корзины"""
        self.driver.get(self.CART_URL)

    @allure.step("Нажатие кнопки 'Купить'")
    def click_buy(self):
        button = self.driver.find_element(*self.CAN_BUY)
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Получение значения счётчика корзины")
    def get_count_cart(self):
        count = self.driver.find_element(*self.CART_COUNTER)
        return count.text

    @allure.step("Удаление одного товара из корзины")
    def remove_one_item(self):
        """Удаляет товар в корзине (кнопка удаления у товара)"""
        remove_button = self.wait.until(EC.element_to_be_clickable(self.DELETE_ONE_ITEM))
        self.driver.execute_script("arguments[0].click();", remove_button)

    @allure.step("Обновление страницы корзины")
    def refresh_cart_page(self):
        """Обновляет страницу корзины"""
        self.driver.refresh()
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    @allure.step("Очистка всей корзины")
    def clear_all_cart(self):
        """Нажимает кнопку 'Очистить корзину'"""
        clear_button = self.wait.until(EC.element_to_be_clickable(self.CLEAR_ALL_CART))
        self.driver.execute_script("arguments[0].click();", clear_button)

    @allure.step("Проверка, что корзина пуста")
    def is_cart_empty(self):
        """Проверяет наличие сообщения 'В корзине ничего нет'"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=5)
