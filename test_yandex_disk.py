import urllib.parse
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

def test_restore_from_trash(setup_test_folder):
    """
    Тест: восстановление файла из Корзины.
    Проверяет:
    - удаление файла в Корзину;
    - поиск файла в Корзине;
    - восстановление файла из Корзины;
    - наличие файла в исходном расположении после восстановления.
    """
    file_path = f"{TEST_FOLDER}/{TEST_FILE_NAME}"
    trash_url = f"{BASE_URL}/disk/trash/resources"
    resources_url = f"{BASE_URL}/disk/resources"

    # Шаг 1: создаём файл для удаления (если ещё не создан)
    upload_url_endpoint = f"{BASE_URL}/disk/resources/upload"
    params = {"path": file_path, "overwrite": "true"}
    response = requests.get(upload_url_endpoint, headers=HEADERS, params=params)
    assert response.status_code == 200, f"Не удалось получить URL для загрузки: {response.status_code}"
    upload_url = response.json()["href"]
    response = requests.put(upload_url, data=TEST_FILE_CONTENT)
    assert response.status_code in [201, 202], f"Ошибка загрузки файла: {response.status_code}"
    time.sleep(1)

    # Шаг 2: удаляем файл в Корзину
    delete_params = {"path": file_path}
    response = requests.delete(resources_url, headers=HEADERS, params=delete_params)
    assert response.status_code in [202, 204], f"Не удалось удалить файл в Корзину: {response.status_code}"
    time.sleep(3)  # Увеличиваем ожидание для надёжности

    # Шаг 3: получаем содержимое Корзины и ищем файл
    response = requests.get(trash_url, headers=HEADERS)
    assert response.status_code == 200, f"Ошибка получения содержимого Корзины: {response.status_code}"

    trash_items = response.json().get("_embedded", {}).get("items", [])
    trash_item = None
    for item in trash_items:
        # Ищем по части имени (учитываем автопереименование)
        if TEST_FILE_NAME in item.get("name"):
            trash_item = item
            break

    assert trash_item is not None, "Файл не найден в Корзине после удаления"

    # Получаем относительный путь к ресурсу в Корзине
    full_trash_path = trash_item["path"]  # например: disk:/Приложения/MyApp/test_folder/test_file.txt_123...
    # Извлекаем относительный путь (после "disk:/Приложения/...")
    relative_path_parts = full_trash_path.split("Приложения/")[-1].split("/")
    relative_trash_path = "/".join(relative_path_parts[1:])  # берём всё после имени приложения

    # Кодируем путь в URL-формат
    encoded_trash_path = urllib.parse.quote(relative_trash_path)

    print(f"Восстанавливаем ресурс: {relative_trash_path} -> {file_path}")

    # Шаг 4: восстанавливаем файл из Корзины
    restore_params = {
        "path": encoded_trash_path,  # относительный путь в Корзине (URL‑закодированный)
        "destination": file_path  # куда восстанавливать
    }

    response = requests.put(f"{trash_url}/restore", headers=HEADERS, params=restore_params)

    # API может вернуть 201 (готово) или 202 (операция в процессе)
    if response.status_code not in [201, 202]:
        print(f"Полный ответ API при ошибке: {response.text}")
        assert False, f"Не удалось восстановить файл из Корзины: {response.status_code}, {response.text}"

    if response.status_code == 202:
        # Если операция запущена, но не завершена, ждём и проверяем статус
        link = response.json().get("href")
        assert link is not None, "В ответе отсутствует ссылка на статус операции"
        # Опрашиваем статус до завершения (с таймаутом)
        max_wait = 30  # секунд
        wait_interval = 2
        elapsed = 0
        while elapsed < max_wait:
            status_response = requests.get(link, headers=HEADERS)
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data.get("status") == "success":
                    break
                elif status_data.get("status") == "failed":
                    assert False, f"Операция восстановления завершилась ошибкой: {status_data}"
            time.sleep(wait_interval)
            elapsed += wait_interval
        else:
            assert False, "Таймаут ожидания завершения операции восстановления"

    time.sleep(2)  # Ждём завершения операции

    # Шаг 5: проверяем, что файл восстановлен в исходном расположении
    check_params = {"path": file_path}
    response = requests.get(resources_url, headers=HEADERS, params=check_params)
    assert response.status_code == 200, f"Файл не найден после восстановления: {response.status_code}"
    file_info = response.json()
    assert file_info["name"] == TEST_FILE_NAME, "Имя восстановленного файла не совпадает с исходным"