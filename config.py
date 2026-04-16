import os # Импортирует модуль Python os. Используется для доступа к переменным окружения через os.getenv()
from dotenv import load_dotenv # Позволяет загружать переменные окружения из файла .env (OAUTH_TOKEN)
from datetime import datetime # Импортирует класс datetime для работы с датой и временем

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
# Функция, генерирующая имя тестовой папки с префиксом test_folder_ и суффиксом в виде текущего времени
def generate_test_foldername():
    return f"test_folder_{datetime.now().strftime('%H%M%S')}"

# Переменная, хранящая имя тестовой папки
TEST_FOLDER = generate_test_foldername()

# Функция, генерирующая имя тестового файла в формате .txt с префиксом test_file_ и суффиксом в виде текущего времени
def generate_test_filename():
    return f"test_file_{datetime.now().strftime('%H%M%S')}.txt"

# Переменная с именем тестового файла
TEST_FILE_NAME = generate_test_filename()

# Содержимое тестового файла 
TEST_FILE_CONTENT = "Hello, Yandex.Disk!"
