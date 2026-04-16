import requests
import time
from config import BASE_URL, HEADERS, TEST_FOLDER, TEST_FILE_NAME, TEST_FILE_CONTENT

def test_get_disk_info():
    url = f"{BASE_URL}/disk"
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200, f"Ошибка GET-запроса: {response.status_code}"
    data = response.json()
    assert "total_space" in data
    assert "used_space" in data

    assert isinstance(data["total_space"], int)

def test_create_and_list_folder(setup_test_folder):
    folder_path = f"{TEST_FOLDER}/subfolder"
    url = f"{BASE_URL}/disk/resources"
    params = {"path": folder_path}

    # Создаём подпапку
    response = requests.put(url, headers=HEADERS, params=params)
    assert response.status_code in [201, 202], f"Не удалось создать подпапку: {response.text}"
    time.sleep(1)

    # Получаем список ресурсов в тестовой папке
    params = {"path": TEST_FOLDER}
    response = requests.get(url, headers=HEADERS, params=params)
    assert response.status_code == 200, f"Ошибка получения списка ресурсов: {response.status_code}"

    data = response.json()

    # Проверяем наличие _embedded и items внутри него
    assert "_embedded" in data, "В ответе отсутствует поле '_embedded'"
    embedded = data["_embedded"]
    assert "items" in embedded, "В '_embedded' отсутствует поле 'items'"

    # Ищем подпапку в списке ресурсов
    items = embedded["items"]
    found = any(item.get("name") == "subfolder" for item in items)
    assert found, "Подпапка 'subfolder' не найдена в списке ресурсов"


def test_upload_and_download_file(setup_test_folder):
    file_path = f"{TEST_FOLDER}/{TEST_FILE_NAME}"
    url_for_upload = f"{BASE_URL}/disk/resources/upload"


    # Шаг 1: получаем URL для загрузки файла
    params = {"path": file_path, "overwrite": "true"}
    response = requests.get(url_for_upload, headers=HEADERS, params=params)
    assert response.status_code == 200, f"Не удалось получить URL для загрузки: {response.status_code}"
    upload_url = response.json()["href"]

    # Шаг 2: загружаем файл
    response = requests.put(upload_url, data=TEST_FILE_CONTENT)
    assert response.status_code in [201, 202, 409], f"Ошибка загрузки файла: {response.status_code}"
    time.sleep(1)  # Ждём завершения операции

    # Шаг 3: получаем URL для скачивания
    url_for_download = f"{BASE_URL}/disk/resources/download"
    params = {"path": file_path}
    response = requests.get(url_for_download, headers=HEADERS, params=params)
    assert response.status_code == 200, f"Не удалось получить URL для скачивания: {response.status_code}"
    download_url = response.json()["href"]

    # Шаг 4: скачиваем файл
    response = requests.get(download_url)
    assert response.status_code == 200, f"Ошибка скачивания файла: {response.status_code}"
    assert response.text == TEST_FILE_CONTENT, "Содержимое файла не совпадает с исходным"
