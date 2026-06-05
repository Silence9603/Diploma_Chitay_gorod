# Diploma_Chitay_gorod

## Шаблон для автоматизации тестирования на Python

### Шаги:
1.Склонировать проект 'git clone https://github.com/Silence9603/Diploma_Chitay_gorod.git'
2.Установить все зависимости
3.Запустить тесты 'pytest'

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure
- config

### Структура:
- ./test - тесты
- ./pages - описание страниц
- ./api - хелпер для работы с API
- ./db - хелпер для работы с БД

### Библиотеки:
- pip install pytest
- pip install selenium
- pip install webdriver-manager

## Команды для запуска тестов и генерации Allure отчета

### Установка зависимостей
pip install -r requirements.txt

### Запуск всех тестов с генерацией Allure результатов
pytest tests/ --alluredir=allure-results -v

### Запуск конкретного тестового модуля
pytest tests/test_main_page.py --alluredir=allure-results -v

### Запуск тестов с метками
pytest tests/ -m "critical" --alluredir=allure-results

### Генерация и открытие Allure отчета
allure generate allure-results -o allure-report --clean
allure open allure-report


Проект поддерживает три режима запуска через маркеры (pytest -m "ui", pytest -m "api", pytest)
Ссылка на финальный проект по ручному тестированию https://zaytsevamn-qa121-2.yonote.ru/share/e1b1d744-210e-4d35-b234-ffb07af068aa
