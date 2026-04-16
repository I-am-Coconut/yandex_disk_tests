import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Базовый URL API Яндекс.Диска с указанием версии v1
BASE_URL = "https://cloud-api.yandex.net/v1"

# Получаем OAuth-токен из переменных окружения (.env файл)
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")

# Заголовки для всех запросов: авторизация и тип контента
HEADERS = {
    "Authorization": f"OAuth {OAUTH_TOKEN}",  # Заголовок авторизации с OAuth-токеном
    "Content-Type": "application/json"  # Указываем, что отправляем JSON-данные
}

# Имя тестовой папки, которая будет создаваться для тестов
TEST_FOLDER = "test_folder"

# Имя тестового файла для операций загрузки/скачивания
TEST_FILE_NAME = "test_file.txt"

# Содержимое тестового файла
TEST_FILE_CONTENT = "Hello, Yandex.Disk!"
