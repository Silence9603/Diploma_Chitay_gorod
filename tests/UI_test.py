from pages.main_page import MainPage


def test_search_book(driver):
    book = 'Маленький принц'
    main = MainPage(driver)

#поиск по ключевому слову (Маленький принц) id="app-search"
    main.open_main_page()
    main.enter_title(book)