import pytest
import allure
from pages.main_page_ui import MainPage
from pages.cart_page_ui import CartPage


@allure.title("Загрузка главной страницы")
@allure.severity(allure.severity_level.CRITICAL)
def test_main_page_loads(driver):
    """Тест загрузки главной страницы"""
    main_page = MainPage(driver)

    with allure.step("Открыть главную страницу"):
        main_page.open_main_page()

    with allure.step("Проверить, что страница загрузилась"):
        assert main_page.is_page_loaded(), "Страница не загрузилась полностью"


@allure.title("Проверка заголовка страницы")
@allure.severity(allure.severity_level.NORMAL)
def test_page_title(driver):
    """Проверка текста заголовка страницы"""
    main_page = MainPage(driver)
    main_page.open_main_page()

    title = driver.title
    with allure.step("Проверить заголовок страницы"):
        assert "Читай-город" in title, f"Заголовок '{title}' не содержит 'Читай-город'"


@allure.title("Проверка наличия основных элементов UI")
@allure.severity(allure.severity_level.NORMAL)
def test_ui_elements_presence(driver):
    """Проверка наличия ключевых UI элементов"""
    main_page = MainPage(driver)
    main_page.open_main_page()

    ui_elements = [
        ("Корзина", main_page.CART_ICON),
        ("Поиск", main_page.SEARCH_INPUT),
        ("Выбор города", main_page.CITY_SELECTOR)
    ]

    for element_name, locator in ui_elements:
        with allure.step(f"Проверить наличие элемента: {element_name}"):
            assert main_page.is_element_visible(locator), f"Элемент '{element_name}' не найден"


def test_search_book(driver):
    """Тест поиска книги по названию"""
    book = 'Обломов'
    main = MainPage(driver)
    main.open_main_page()
    main.enter_title(book)
    main.is_search_result_page()
    assert main.get_search_result() == book


def test_cart_counter(driver):
    """Тест проверки счетчика корзины после добавления товара"""
    book = 'Ходячий замок'
    main = MainPage(driver)
    cart = CartPage(driver)
    main.open_main_page()
    main.enter_title(book)
    main.is_search_result_page()
    cart.click_buy()
    assert cart.get_count_cart() == '1'


def test_delete_book_and_cart_becomes_empty(driver):
    """Тест удаления товара из корзины"""
    book = 'Маленький принц'
    main = MainPage(driver)
    cart = CartPage(driver)

    # Добавляем книгу в корзину
    main.open_main_page()
    main.enter_title(book)
    main.is_search_result_page()
    cart.click_buy()

    # Переходим на страницу корзины, удаляем товар
    cart.open_cart_page()
    cart.remove_one_item()

    # Обновляем страницу корзины и проверяем, что корзина пуста
    cart.refresh_cart_page()
    assert cart.is_cart_empty(), "Сообщение 'В корзине ничего нет' не появилось"
