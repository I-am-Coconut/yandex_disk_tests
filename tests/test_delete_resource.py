import requests
from config import RESOURCES_URL, HEADERS, TEST_FOLDER


def test_delete_folder_success(setup_and_cleanup_test_folder):
    """
    Тест: удаляем папку (успешный случай)
    Проверяем, что пустая папка удаляется с кодом 204 No Content
    """
    # Используем тестовую папку, созданную фикстурой
    folder_path = setup_and_cleanup_test_folder

    # Параметры запроса: путь к папке и признак безвозвратного удаления
    params = {
        "path": folder_path,
        "permanently": "true"  # удаляем без помещения в Корзину
    }

    response = requests.delete(RESOURCES_URL, headers=HEADERS, params=params)

    # Успешное удаление пустой папки возвращает код 204
    assert response.status_code == 204, (
        f"Ожидался код 204 (No Content), получен {response.status_code}. "
        f"Ответ сервера: {response.text}"
    )

    print(f"Папка {folder_path} успешно удалена!")



def test_delete_nonexistent_resource():
    """
    Тест: попытка удалить несуществующий ресурс
    Ожидаем ошибку 404 Not Found
    """
    nonexistent_path = "/nonexistent_folder_12345"

    params = {
        "path": nonexistent_path
    }

    response = requests.delete(RESOURCES_URL, headers=HEADERS, params=params)

    # При попытке удалить несуществующий ресурс сервер возвращает 404
    assert response.status_code == 404, (
        f"Ожидался код 404 (Not Found), получен {response.status_code}"
    )

    error_data = response.json()
    assert "message" in error_data, "В ответе об ошибке нет описания"
    print("Тест удаления несуществующего ресурса пройден успешно!")


def test_delete_with_invalid_token():
    """
    Тест: удаление с неверным токеном (ошибка авторизации)
    Ожидаем код 401 Unauthorized
    """
    folder_path = "/some_folder"

    # Создаём заголовки с заведомо неверным токеном
    bad_headers = {
        "Authorization": "OAuth invalid_token_123"
    }

    params = {
        "path": folder_path
    }

    response = requests.delete(RESOURCES_URL, headers=bad_headers, params=params)

    # При неверном токене сервер возвращает 401
    assert response.status_code == 401, (
        f"Ожидался код 401 (Unauthorized), получен {response.status_code}"
    )

    error_data = response.json()
    assert "message" in error_data, "В ответе об ошибке нет описания"
    print("Тест ошибки авторизации при удалении пройден успешно!")
