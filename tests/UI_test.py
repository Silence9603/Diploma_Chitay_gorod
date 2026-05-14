from pages.UI_page import MainPage


def test1(driver):
    main = MainPage(driver)

#поиск по ключевому слову (Маленький принц) id="app-search"
    main.open()