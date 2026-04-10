# Базовый URL API Яндекс.Диска (версия 1)
BASE_URL = "https://cloud-api.yandex.net/v1"

# Эндпоинты для разных операций
DISK_INFO_URL = f"{BASE_URL}/disk"
RESOURCES_URL = f"{BASE_URL}/disk/resources"
COPY_URL = f"{BASE_URL}/disk/resources/copy"

# ВАЖНО: замените на ваш OAuth-токен
OAUTH_TOKEN = "y0__xDN8_XkCBjLlkAggc-JhBcwu7yKgwgGUxlyRAsMo1T_RqnvV-J2rT_-_A"

# Заголовки для всех запросов
HEADERS = {
    "Authorization": f"OAuth {OAUTH_TOKEN}"
}

# Тестовые данные
TEST_FOLDER = "/test_folder_for_automation"
TEST_FILE = "test_file.txt"
