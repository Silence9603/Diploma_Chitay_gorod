import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания драйвера браузера"""
    #driver = webdriver.Chrome()
    #driver.maximize_window()
    #driver.implicitly_wait(4) # Ждем появления элементов до 4 секунд
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Этот хук срабатывает после каждого теста.
    Если тест упал - делает скриншот и сохраняет URL страницы.
    """
    outcome = yield
    report = outcome.get_result()

    # Проверяем, что тест выполнился (не setup/teardown) и упал
    if report.when == "call" and report.failed:
        # Проверяем, есть ли в тесте фикстура driver
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]

            # Делаем скриншот и добавляем в Allure отчёт
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"Скриншот в момент ошибки: {item.name}",
                attachment_type=allure.attachment_type.PNG
            )

            # Сохраняем URL страницы, где упал тест
            allure.attach(
                driver.current_url,
                name="URL страницы с ошибкой",
                attachment_type=allure.attachment_type.TEXT
            )

            # Сохраняем заголовок страницы
            allure.attach(
                driver.title,
                name="Заголовок страницы",
                attachment_type=allure.attachment_type.TEXT
            )