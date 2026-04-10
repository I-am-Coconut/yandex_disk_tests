import requests
import pytest
from config import RESOURCES_URL, HEADERS

def test_create_folder_success(setup_and_cleanup_test_folder):
    """Тест: создаём папку (успешный случай)"""
    folder_path = "/new_test_folder"
    params = {"path": folder_path}

    response = requests.put(RESOURCES_URL, headers=HEADERS, params=params)

    # Успешное создание папки возвращает код 201 Created
    assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

    # Проверяем, что папка действительно создана
    check_response = requests.get(RESOURCES_URL, headers=HEADERS, params={"path": folder_path})
    assert check_response.status_code == 200, "Папка не была создана!"

    # Удаляем созданную папку
    delete_params = {"path": folder_path, "permanently": "true"}
    requests.delete(RESOURCES_URL, headers=HEADERS, params=delete_params)
    print("Папка успешно создана и удалена!")

def test_create_folder_invalid_path():
    """Тест: создание папки с некорректным путём"""
    invalid_path = "//invalid//path"
    params = {"path": invalid_path}
    response = requests.put(RESOURCES_URL, headers=HEADERS, params=params)

    # Некорректный путь должен вызвать ошибку (400 или 404)
    assert response.status_code in [400, 404], f"Ожидался код 400/404, получен {response.status_code}"
    print("Тест некорректного пути пройден!")
