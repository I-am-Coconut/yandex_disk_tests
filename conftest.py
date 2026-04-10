import pytest
import requests
from config import RESOURCES_URL, HEADERS, TEST_FOLDER

@pytest.fixture(scope="session")
def setup_and_cleanup_test_folder():
    """
    Фикстура: создаёт тестовую папку перед тестами, удаляет после
    """
    # Создаём тестовую папку
    params = {"path": TEST_FOLDER}
    response = requests.put(RESOURCES_URL, headers=HEADERS, params=params)
    assert response.status_code == 201, f"Не удалось создать тестовую папку: {response.json()}"

    print(f"Тестовая папка {TEST_FOLDER} создана")

    # Возвращаем путь к папке — он будет доступен в тестах
    yield TEST_FOLDER

    # Удаляем тестовую папку после всех тестов
    delete_params = {"path": TEST_FOLDER, "permanently": "true"}
    response = requests.delete(RESOURCES_URL, headers=HEADERS, params=delete_params)

    if response.status_code in [204, 404]:
        print(f"Тестовая папка {TEST_FOLDER} удалена")
    else:
        print(f"Предупреждение: не удалось удалить папку: {response.json()}")
