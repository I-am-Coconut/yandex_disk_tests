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

# URL с протоколом для запроса информации о диске
url = "https://cloud-api.yandex.net/v1/disk"

# Формируем заголовки с токеном из .env для авторизации в API
headers = {"Authorization": f"OAuth {oauth_token}"}

try:
    # Отправляем GET-запрос к API Яндекс.Диска с таймаутом 10 секунд
    response = requests.get(url, headers=headers, timeout=10)

 # Анализируем статус-код ответа сервера
    if response.status_code == 200:
        # Успешный ответ (200 OK) — парсим JSON и подтверждаем корректность токена
        data = response.json()
        assert True, "Токен корректен, получен ответ от API Яндекс.Диска"
    elif response.status_code == 401:
        # Ошибка авторизации: неверный или просроченный токен (401 Unauthorized)
        assert False, "Ошибка 401: Неверный или просроченный OAuth-токен."
    elif response.status_code == 403:
        # Запрещено: недостаточно прав у токена (403 Forbidden)
        assert False, "Ошибка 403: Недостаточно прав у OAuth-токена."
    else:
        # Другие ошибки — формируем сообщение с кодом и данными ответа
        try:
            # Пытаемся распарсить JSON ошибки, если он есть в ответе сервера
            error_data = response.json()
            assert False, f"Ошибка {response.status_code}: {error_data}"
        except ValueError:
            # Если ответ не в формате JSON, используем текст ответа как описание ошибки
            assert False, f"Ошибка {response.status_code}: {response.text}"

except requests.exceptions.RequestException as e:
    # Обработка сетевых ошибок (нет соединения, тайм-аут, неверный URL и т. п.)
    assert False, f"Сетевая ошибка: {e}"
except ValueError as e:
    # Обработка ошибок конфигурации (например, отсутствие токена)
    assert False, f"Ошибка конфигурации: {e}"