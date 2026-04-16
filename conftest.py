import pytest
from config import BASE_URL, HEADERS, TEST_FOLDER
import requests

@pytest.fixture(scope="session")
def setup_test_folder():
    """
    Фикстура pytest: создаёт тестовую папку перед запуском тестов
    и удаляет её после завершения всех тестов в сессии.
    scope="session" означает, что фикстура выполняется один раз для всей сессии тестов.
    """
    folder_url = f"{BASE_URL}/disk/resources"  # URL для работы с ресурсами (папками/файлами)
    params = {"path": TEST_FOLDER}  # Параметры запроса: путь к создаваемой папке

    # Создаём папку с помощью PUT-запроса
    response = requests.put(folder_url, headers=HEADERS, params=params)
    # Проверяем, что папка создана успешно (код 201 — Created)
    assert response.status_code == 201, f"Не удалось создать тестовую папку: {response.text}"

    yield TEST_FOLDER  # Передаём имя папки в тесты, которые используют эту фикстуру

    # Код после yield выполняется после завершения всех тестов, использующих эту фикстуру
    params = {"path": TEST_FOLDER}  # Указываем путь к папке для удаления
    response = requests.delete(folder_url, headers=HEADERS, params=params)
    # Проверяем, что удаление прошло успешно (коды 202 — Accepted или 204 — No Content)
    assert response.status_code in [202, 204], f"Не удалось удалить тестовую папку: {response.text}"
