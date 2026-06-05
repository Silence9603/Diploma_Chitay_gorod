import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure

from pages.main_page_ui import MainPage


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера браузера"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")

    with allure.step("Инициализация Chrome драйвера"):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)

    yield driver

    with allure.step("Закрытие браузера"):
        driver.quit()


@pytest.fixture(scope="function")
def base_url():
    """Фикстура с базовым URL"""
    return "https://www.chitai-gorod.ru"


@pytest.fixture(scope="function")
def clean_state(driver):
    """Фикстура для очистки состояния (cookie, localStorage) перед тестом"""
    driver.execute_script("window.localStorage.clear();")
    driver.delete_all_cookies()
    yield
    driver.execute_script("window.localStorage.clear();")
    driver.delete_all_cookies()


@pytest.fixture
def main_page(driver):
    """Фикстура для MainPage с автоматической обработкой города"""
    page = MainPage(driver)
    page.open_main_page()

    # Закрываем окно выбора города, если оно появилось
    page.close_city_modal()

    return page
