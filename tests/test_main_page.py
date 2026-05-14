import pytest
import allure
from pages.main_page import MainPage


@allure.feature("Главная страница")
@allure.story("Загрузка и отображение")
class TestMainPage:

    @allure.title("Загрузка главной страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_page_loads(self, driver, base_url):
        """Тест загрузки главной страницы"""
        main_page = MainPage(driver)

        with allure.step("Открыть главную страницу"):
            main_page.open(base_url)

        with allure.step("Проверить, что страница загрузилась"):
            assert main_page.is_page_loaded(), "Страница не загрузилась полностью"

        with allure.step("Проверить наличие поля поиска"):
            assert main_page.is_element_visible(main_page.SEARCH_INPUT), "Поле поиска отсутствует"

        with allure.step("Проверить наличие селектора города"):
            assert main_page.is_element_visible(main_page.CITY_SELECTOR), "Селектор города отсутствует"

        with allure.step("Проверить наличие книг на странице"):
            assert main_page.has_books_displayed(), "На странице нет книг"

    @allure.title("Проверка заголовка страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_title(self, driver, base_url):
        """Проверка текста заголовка страницы"""
        main_page = MainPage(driver)
        main_page.open(base_url)

        title = driver.title
        with allure.step("Проверить заголовок страницы"):
            assert "Читай-город" in title, f"Заголовок '{title}' не содержит 'Читай-город'"

    @allure.title("Проверка наличия основных элементов UI")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ui_elements_presence(self, driver, base_url):
        """Проверка наличия ключевых UI элементов"""
        main_page = MainPage(driver)
        main_page.open(base_url)

        ui_elements = [
            ("Корзина", main_page.CART_ICON),
            ("Поиск", main_page.SEARCH_INPUT),
            ("Выбор города", main_page.CITY_SELECTOR),
            ("Секция с книгами", main_page.BOOKS_SECTION)
        ]

        for element_name, locator in ui_elements:
            with allure.step(f"Проверить наличие элемента: {element_name}"):
                assert main_page.is_element_visible(locator), f"Элемент '{element_name}' не найден"

    @allure.title("Проверка работы карусели/баннеров")
    @allure.severity(allure.severity_level.MINOR)
    def test_banner_carousel_exists(self, driver, base_url):
        """Проверка наличия карусели с баннерами"""
        main_page = MainPage(driver)
        main_page.open(base_url)

        with allure.step("Проверить наличие карусели"):
            assert main_page.is_element_visible(main_page.BANNER_CAROUSEL), "Карусель с баннерами отсутствует"
