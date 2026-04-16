import pytest
import requests
import time
from config import BASE_URL, HEADERS, TEST_FOLDER

@pytest.fixture(scope="session")
def setup_test_folder():
    """
    Фикстура pytest: создаёт тестовую папку перед запуском тестов
    и удаляет её после завершения всех тестов в сессии.
    """
    folder_url = f"{BASE_URL}/disk/resources"
    params = {"path": TEST_FOLDER}

    # Создаём папку
    response = requests.put(folder_url, headers=HEADERS, params=params)
    if response.status_code not in [201, 202]:  # Учитываем 202 Accepted
        pytest.fail(f"Не удалось создать тестовую папку: {response.text}")

    # Ждём завершения операции
    time.sleep(2)

    yield TEST_FOLDER  # Передаём имя папки в тесты

    # Удаление папки после тестов
    try:
        response = requests.delete(folder_url, headers=HEADERS, params={"path": TEST_FOLDER})
        if response.status_code not in [202, 204]:
            print(f"Предупреждение: не удалось удалить тестовую папку: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при удалении тестовой папки: {e}")

