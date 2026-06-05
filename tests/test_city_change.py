import pytest
import allure
from pages.main_page import MainPage
from pages.city_modal import CityModal


@allure.feature("Выбор города")
@allure.story("Смена города и обновление контента")
class TestCityChange:

    @allure.title("Открытие модального окна выбора города")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_city_modal(self, driver, base_url):
        """Тест открытия модального окна смены города"""
        main_page = MainPage(driver)
        city_modal = CityModal(driver)

        main_page.open(base_url)
        default_city = main_page.get_current_city()

        with allure.step("Открыть модальное окно города"):
            city_modal.open_city_modal(main_page)

        with allure.step("Проверить, что модальное окно отображается"):
            assert city_modal.is_modal_visible(), "Модальное окно не открылось"

        with allure.step("Закрыть модальное окно"):
            city_modal.close_modal()

        with allure.step("Проверить, что город не изменился"):
            assert main_page.get_current_city() == default_city, "Город изменился после закрытия окна"

    @allure.title("Поиск города в модальном окне")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_city_in_modal(self, driver, base_url):
        """Тест поиска города в модальном окне"""
        main_page = MainPage(driver)
        city_modal = CityModal(driver)

        main_page.open(base_url)
        city_modal.open_city_modal(main_page)

        test_city = "Санкт-Петербург"

        with allure.step(f"Поиск города '{test_city}'"):
            city_modal.search_city(test_city)

        with allure.step("Проверить отображение результатов поиска"):
            assert city_modal.is_element_visible(city_modal.CITY_LIST), "Результаты поиска не отображаются"

    @allure.title("Успешная смена города")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("new_city", ["Санкт-Петербург", "Екатеринбург", "Новосибирск"])
    def test_change_city_successfully(self, driver, base_url, new_city):
        """Тест успешной смены города"""
        main_page = MainPage(driver)
        city_modal = CityModal(driver)

        main_page.open(base_url)
        old_city = main_page.get_current_city()

        with allure.step(f"Сменить город на '{new_city}'"):
            city_modal.change_city(main_page, new_city)

        with allure.step("Проверить, что город изменился"):
            current_city = main_page.get_current_city()
            assert new_city.lower() in current_city.lower() or current_city.lower() in new_city.lower(), \
                f"Город не изменился. Ожидался {new_city}, получен {current_city}"

    @allure.title("Смена города на несуществующий")
    @allure.severity(allure.severity_level.NORMAL)
    def test_change_city_invalid(self, driver, base_url):
        """Тест попытки выбора несуществующего города"""
        main_page = MainPage(driver)
        city_modal = CityModal(driver)
        invalid_city = "ВымышленныйГород123"

        main_page.open(base_url)
        city_modal.open_city_modal(main_page)

        with allure.step(f"Поиск несуществующего города '{invalid_city}'"):
            city_modal.search_city(invalid_city)

        with allure.step("Проверить, что город не найден"):
            city_found = city_modal.select_city(invalid_city)
            assert not city_found, "Найден несуществующий город"

    @allure.title("Сохранение выбранного города после перезагрузки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_city_persists_after_reload(self, driver, base_url):
        """Тест сохранения выбранного города после перезагрузки страницы"""
        main_page = MainPage(driver)
        city_modal = CityModal(driver)
        test_city = "Казань"

        main_page.open(base_url)
        city_modal.change_city(main_page, test_city)

        with allure.step("Перезагрузить страницу"):
            driver.refresh()

        with allure.step("Проверить, что город сохранился"):
            current_city = main_page.get_current_city()
            assert test_city.lower() in current_city.lower(), \
                f"Город не сохранился. Ожидался {test_city}, получен {current_city}"
