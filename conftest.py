import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()      
    driver.maximize_window()
    driver.implicitly_wait(4) # Ждем появления элементов до 4 секунд


    yield driver


    driver.quit()
