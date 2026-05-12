from pages.UI_page import MainPage


def test1(driver):
    main = MainPage(driver)
    main.open()