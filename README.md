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

### Параллельный запуск (4 потока)
pytest tests/ -n 4 --alluredir=allure-results

### Генерация и открытие Allure отчета
allure generate allure-results -o allure-report --clean
allure open allure-report
