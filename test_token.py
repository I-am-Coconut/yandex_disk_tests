import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env-файла
load_dotenv()

# Получаем токен из переменных окружения
oauth_token = os.getenv("OAUTH_TOKEN")

# Проверяем, что токен загружен
if not oauth_token:
    raise ValueError("OAuth-токен не найден в .env-файле. Проверьте наличие переменной OAUTH_TOKEN.")

# Корректный URL с правильным протоколом
url = "https://cloud-api.yandex.net/v1/disk"

# Формируем заголовки с токеном из .env
headers = {"Authorization": f"OAuth {oauth_token}"}

try:
    # Отправляем GET-запрос к API Яндекс.Диска с таймаутом 10 секунд
    response = requests.get(url, headers=headers, timeout=10)

    # Выводим статус-код ответа
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        # Успешный ответ — парсим JSON и выводим данные
        data = response.json()
        print("Корректный токен")
    elif response.status_code == 401:
        # Ошибка авторизации: неверный или просроченный токен
        print("Ошибка 401: Неверный или просроченный OAuth-токен.")
    elif response.status_code == 403:
        # Запрещено: недостаточно прав у токена
        print("Ошибка 403: Недостаточно прав у OAuth-токена.")
    else:
        # Другие ошибки — выводим статус и текст ответа
        print(f"Ошибка {response.status_code}:")
        try:
            # Пытаемся распарсить JSON ошибки, если он есть
            error_data = response.json()
            print(error_data)
        except ValueError:
            # Если ответ не в формате JSON, выводим текст как есть
            print(response.text)

except requests.exceptions.RequestException as e:
    # Обработка сетевых ошибок (нет соединения, тайм-аут и т. п.)
    print(f"Сетевая ошибка: {e}")
except ValueError as e:
    # Обработка ошибок конфигурации (например, отсутствие токена)
    print(f"Ошибка конфигурации: {e}")
