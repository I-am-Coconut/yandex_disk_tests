Автотесты для API Яндекс.Диска

Тесты покрывают следующие операции:
GET — получение информации о Диске;
PUT — создание папок;
POST — копирование ресурсов;
DELETE — удаление файлов и папок.

Стек технологий
Python 3.7+
pytest (фреймворк для тестирования)
requests (библиотека для HTTP‑запросов)

Требования
Python 3.7 или выше;
Git (для клонирования репозитория);
аккаунт на Яндексе с доступом к Яндекс.Диску.

Структура проекта

yandex-disk-tests/
├── requirements.txt         # зависимости проекта
├── config.py                # конфигурация (URL API, токен, тестовые данные)
├── conftest.py              # фикстуры pytest (создание/удаление тестовой папки)
└── tests/
    ├── __init__.py
    ├── test_get_disk_info.py      # тесты GET‑запросов (информация о Диске)
    ├── test_put_create_folder.py  # тесты PUT‑запросов (создание папок)
    ├── test_post_copy_resource.py # тесты POST‑запросов (копирование ресурсов)
    └── test_delete_resource.py    # тесты DELETE‑запросов (удаление ресурсов)

Установка и настройка

Клонируйте репозиторий 
git clone <URL_вашего_репозитория>
cd yandex-disk-tests

Создайте виртуальное окружение (опционально)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Установите зависимости
pip install -r requirements.txt

 Настройте OAuth‑токен
Получите OAuth‑токен для Яндекс.Диска:
перейдите на страницу Яндекс OAuth: https://oauth.yandex.ru/;
войдите в свой аккаунт;
нажмите «Создать новое приложение»;
заполните название (например, Yandex Disk Test App);
в разделе «Права доступа» выберите:
disk:read — чтение всего Диска;
disk:write — запись в любом месте на Диске;
сохраните Client ID и Client Secret;
запросите OAuth‑токен (можно через интерфейс Яндекс OAuth или с помощью скрипта);
скопируйте полученный токен.
Откройте файл config.py.
Замените значение OAUTH_TOKEN на ваш реальный OAuth‑токен:
OAUTH_TOKEN = "ваш_реальный_oauth_токен_здесь"

Запуск тестов
Основные команды
Запустить все тесты: pytest
Запустить конкретный файл с тестами: pytest tests/test_get_disk_info.py
Запустить с подробным выводом (verbose):
pytest -v

Ожидаемые результаты
При успешном запуске вы увидите в консоли:

test session starts =====================
platform linux -- Python 3.x, pytest-7.4.0, pluggy-1.0.0
rootdir: /path/to/yandex-disk-tests
collected 4 items

tests/test_get_disk_info.py .                          [ 25%]
tests/test_put_create_folder.py .                     [ 50%]
tests/test_post_copy_resource.py .                   [ 75%]
tests/test_delete_resource.py .                      [100%]

============================== 4 passed in 5.21s ======================

Расшифровка символов:
. — тест пройден успешно;
F — тест упал (failed);
E — произошла ошибка выполнения (error).
