import requests
from config import COPY_URL, RESOURCES_URL, HEADERS, TEST_FOLDER

def test_copy_folder_success(setup_and_cleanup_test_folder):
    """Тест: копируем папку (успешный случай)"""
    source_path = TEST_FOLDER
    destination_path = f"{TEST_FOLDER}_copy"

    params = {
        "from": source_path,
        "path": destination_path
    }

    response = requests.post(COPY_URL, headers=HEADERS, params=params)

    # Успешное копирование возвращает 201 или 202 (если операция асинхронная)
    assert response.status_code in [201, 202], f"Ожидался код 201/202, получен {response.status_code}"

    if response.status_code == 201:
        # Синхронное копирование — проверяем, что копия создана
        check_response = requests.get(RESOURCES_URL, headers=HEADERS, params={"path": destination_path})
        assert check_response.status_code == 200, "Копия папки не была создана!"
    else:
        # Асинхронное копирование — здесь можно добавить логику отслеживания статуса
        operation_data = response.json()
        assert "href" in operation_data, "В ответе нет ссылки на операцию"

    # Удаляем скопированную папку
    delete_params = {"path": destination_path, "permanently": "true"}
    requests.delete(RESOURCES_URL, headers=HEADERS, params=delete_params)
    print("Папка успешно скопирована и удалена!")
