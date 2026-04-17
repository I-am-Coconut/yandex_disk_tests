# Импорты подключают необходимые библиотеки и конфигурационные константы
import urllib.parse
import requests
import time
from config import BASE_URL, HEADERS, TEST_FOLDER, TEST_FILE_NAME, TEST_FILE_CONTENT


""" Тест проверяет доступ к API и получение базовой информации о диске """

def test_get_disk_info():
    # Формируем URL для запроса информации о диске
    url = f"{BASE_URL}/disk"
    # Отправляем GET‑запрос к API Яндекс.Диска с авторизационными заголовками
    response = requests.get(url, headers=HEADERS)
    # Проверяем, что запрос успешен (статус 200)
    assert response.status_code == 200, f"Ошибка GET-запроса: {response.status_code}"
    # Парсим JSON‑ответ от сервера
    data = response.json()
     # Убеждаемся, что в ответе присутствуют ключевые поля о пространстве диска
    assert "total_space" in data
    assert "used_space" in data
    # Проверяем, что total_space имеет тип int (целое число)
    assert isinstance(data["total_space"], int)


""" Тест создание подпапки и проверка её наличия в списке ресурсов"""

def test_create_and_list_folder(setup_test_folder):
    # Формируем путь для создания подпапки внутри тестовой папки
    folder_path = f"{TEST_FOLDER}/subfolder"
    # URL для работы с ресурсами Яндекс.Диска
    url = f"{BASE_URL}/disk/resources"
    # Параметры запроса: указываем путь к создаваемой подпапке
    params = {"path": folder_path}

    # PUT‑запрос на создание подпапки
    response = requests.put(url, headers=HEADERS, params=params)
    # Проверяем успешность создания (201 — создано, 202 — принято в обработку)
    assert response.status_code in [201, 202], f"Не удалось создать подпапку: {response.text}"
    # Ждём 1 секунду, чтобы операция гарантированно завершилась
    time.sleep(1)

    # Получаем список ресурсов в тестовой папке
    params = {"path": TEST_FOLDER}
    # GET‑запрос на получение списка ресурсов
    response = requests.get(url, headers=HEADERS, params=params)
    # Проверяем, что запрос списка прошёл успешно
    assert response.status_code == 200, f"Ошибка получения списка ресурсов: {response.status_code}"
    # Парсим JSON‑ответ
    data = response.json()

    # Проверяем наличие вложенной структуры '_embedded' в ответе
    assert "_embedded" in data, "В ответе отсутствует поле '_embedded'"
    embedded = data["_embedded"]
    # Внутри '_embedded' должно быть поле 'items' с перечнем ресурсов
    assert "items" in embedded, "В '_embedded' отсутствует поле 'items'"

    # Извлекаем список элементов
    items = embedded["items"]
    # Ищем подпапку с именем 'subfolder' в списке ресурсов
    found = any(item.get("name") == "subfolder" for item in items)
    # Утверждаем, что подпапка найдена
    assert found, "Подпапка 'subfolder' не найдена в списке ресурсов"


"""Тест загрузка файла, скачивание, проверка содержимого"""

def test_upload_and_download_file(setup_test_folder):
    # Формируем полный путь к файлу внутри тестовой папки
    file_path = f"{TEST_FOLDER}/{TEST_FILE_NAME}"
    # URL для получения ссылки на загрузку файла
    url_for_upload = f"{BASE_URL}/disk/resources/upload"


    # Шаг 1: получаем URL для загрузки файла (разрешаем перезапись, если файл уже есть)
    params = {"path": file_path, "overwrite": "true"}
    response = requests.get(url_for_upload, headers=HEADERS, params=params)
    # Проверяем, что получили ссылку на загрузку
    assert response.status_code == 200, f"Не удалось получить URL для загрузки: {response.status_code}"
    upload_url = response.json()["href"]

    # Шаг 2: загружаем файл с тестовым содержимым
    response = requests.put(upload_url, data=TEST_FILE_CONTENT)
    # Проверяем статус загрузки (201 — создан, 202 — принят, 409 — конфликт, но может быть допустимым)
    assert response.status_code in [201, 202, 409], f"Ошибка загрузки файла: {response.status_code}"
    # Ждём завершения операции
    time.sleep(1)

    # Шаг 3: получаем URL для скачивания
    url_for_download = f"{BASE_URL}/disk/resources/download"
    params = {"path": file_path}
    response = requests.get(url_for_download, headers=HEADERS, params=params)
    # Проверяем, что получили ссылку для скачивания
    assert response.status_code == 200, f"Не удалось получить URL для скачивания: {response.status_code}"
    download_url = response.json()["href"]

    # Шаг 4: скачиваем файл
    response = requests.get(download_url)
    # Проверяем, что скачивание прошло успешно
    assert response.status_code == 200, f"Ошибка скачивания файла: {response.status_code}"
    # Сравниваем содержимое скачанного файла с исходным
    assert response.text == TEST_FILE_CONTENT, "Содержимое файла не совпадает с исходным"


"""Тест восстановления файла из Корзины"""

def test_restore_from_trash(setup_test_folder):
    # Полный путь к тестовому файлу внутри тестовой папки
    file_path = f"{TEST_FOLDER}/{TEST_FILE_NAME}"
    # URL для работы с Корзиной Яндекс.Диска
    trash_url = f"{BASE_URL}/disk/trash/resources"
    # URL для работы с основными ресурсами Яндекс.Диска
    resources_url = f"{BASE_URL}/disk/resources"

    # Шаг 1: создаём файл для удаления (если ещё не создан)
    upload_url_endpoint = f"{BASE_URL}/disk/resources/upload"
    params = {"path": file_path, "overwrite": "true"}
    response = requests.get(upload_url_endpoint, headers=HEADERS, params=params)
    # Проверяем, что получили URL для загрузки
    assert response.status_code == 200, f"Не удалось получить URL для загрузки: {response.status_code}"
    upload_url = response.json()["href"]
    # Загружаем файл
    response = requests.put(upload_url, data=TEST_FILE_CONTENT)
    # Проверяем успешность загрузки
    assert response.status_code in [201, 202], f"Ошибка загрузки файла: {response.status_code}"
    # Ждём завершения операции
    time.sleep(1)

    # Шаг 2: удаляем файл в Корзину
    delete_params = {"path": file_path}
    response = requests.delete(resources_url, headers=HEADERS, params=delete_params)
    # Проверяем, что файл успешно перемещён в Корзину (202 — принято, 204 — успешно удалено)
    assert response.status_code in [202, 204], f"Не удалось удалить файл в Корзину: {response.status_code}"
    # Ждём 2 секунды для надёжного завершения операции удаления
    time.sleep(2)

    # Шаг 3: получаем содержимое Корзины и ищем файл
    response = requests.get(trash_url, headers=HEADERS)
    # Проверяем успешность запроса к Корзине
    assert response.status_code == 200, f"Ошибка получения содержимого Корзины: {response.status_code}"
    # Извлекаем список элементов из ответа API
    trash_items = response.json().get("_embedded", {}).get("items", [])
    trash_item = None
    # Перебираем элементы Корзины, ищем файл по части имени (учитываем возможное автопереименование)
    for item in trash_items:
        if TEST_FILE_NAME in item.get("name"):
            trash_item = item
            break
    # Убеждаемся, что файл найден в Корзине после удаления
    assert trash_item is not None, "Файл не найден в Корзине после удаления"

    # Получаем полный путь к ресурсу в корзине (например: disk:/Приложения/MyApp/test_folder/test_file.txt_123...)
    full_trash_path = trash_item["path"]  
    # Извлекаем относительный путь: разбиваем строку по "Приложения/", берём последнюю часть, затем разбиваем по "/"
    relative_path_parts = full_trash_path.split("Приложения/")[-1].split("/")
    # Формируем относительный путь, исключая имя приложения (берём всё после него)
    relative_trash_path = "/".join(relative_path_parts[1:]) 
    # Кодируем путь в URL-формат
    encoded_trash_path = urllib.parse.quote(relative_trash_path)

    # Шаг 4: восстанавливаем файл из Корзины
    restore_params = {
        "path": encoded_trash_path,  # относительный путь в Корзине (URL‑закодированный)
        "destination": file_path  # путь, куда восстанавливать файл
    }

    response = requests.put(f"{trash_url}/restore", headers=HEADERS, params=restore_params)

    # Проверяем статус ответа API: 201 — готово, 202 — операция в процессе
    if response.status_code not in [201, 202]:
        # Если статус не соответствует, прерываем тест с ошибкой и выводом полного ответа API
        assert False, f"Не удалось восстановить файл из Корзины: {response.status_code}, {response.text}"

    if response.status_code == 202:
        # Если операция запущена, но не завершена, получаем ссылку на статус операции
        link = response.json().get("href")
        # Убеждаемся, что ссылка на статус присутствует в ответе
        assert link is not None, "В ответе отсутствует ссылка на статус операции"
        # Настраиваем параметры ожидания завершения операции
        max_wait = 30  # время ожидания в секундах
        wait_interval = 2 # интервал между проверками в секундах
        elapsed = 0 # счётчик прошедшего времени

        # Опрашиваем статус до завершения или таймаута
        while elapsed < max_wait:
            status_response = requests.get(link, headers=HEADERS)
            if status_response.status_code == 200:
                status_data = status_response.json()
                # Если операция завершена успешно, выходим из цикла
                if status_data.get("status") == "success":
                    break
                # Если операция завершилась ошибкой, прерываем тест
                elif status_data.get("status") == "failed":
                    assert False, f"Операция восстановления завершилась ошибкой: {status_data}"
            # Ждём перед следующей проверкой
            time.sleep(wait_interval)
            elapsed += wait_interval
        else:
            # Если время ожидания истекло, прерываем тест с ошибкой таймаута
            assert False, "Таймаут ожидания завершения операции восстановления"
    # Ждём 2 секунды после завершения операции восстановления
    time.sleep(2)

    # Шаг 5: проверяем, что файл восстановлен в исходном расположении
    check_params = {"path": file_path}
    response = requests.get(resources_url, headers=HEADERS, params=check_params)
    # Проверяем, что файл доступен по исходному пути
    assert response.status_code == 200, f"Файл не найден после восстановления: {response.status_code}"
    file_info = response.json()
    # Убеждаемся, что имя восстановленного файла совпадает с исходным
    assert file_info["name"] == TEST_FILE_NAME, "Имя восстановленного файла не совпадает с исходным"