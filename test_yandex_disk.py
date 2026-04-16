import requests
from config import BASE_URL, HEADERS, TEST_FOLDER, TEST_FILE_NAME, TEST_FILE_CONTENT

class TestYandexDiskAPI:
    def test_get_disk_info(self):
        """
        Тест GET-запроса: получение информации о Диске (свободное место, занятое место и т. д.)
        """
        url = f"{BASE_URL}/disk"  # Формируем URL для запроса информации о Диске
        response = requests.get(url, headers=HEADERS)  # Отправляем GET-запрос с заголовками авторизации

        # Проверяем, что запрос выполнен успешно (код 200 — OK)
        assert response.status_code == 200, f"Ошибка GET-запроса: {response.status_code}"
        data = response.json()  # Парсим JSON-ответ от API


        # Проверяем наличие ключевых полей в ответе
        assert "total_space" in data  # Общее пространство Диска
        assert "used_space" in data   # Занятое пространство
        assert isinstance(data["total_space"], int)  # Убеждаемся, что total_space — целое число

    def test_create_and_list_folder(self, setup_test_folder):
        """
        Тест POST/GET: создание подпапки внутри тестовой папки и получение списка ресурсов.
        Использует фикстуру setup_test_folder для получения имени тестовой папки.
        """
        folder_path = f"{TEST_FOLDER}/subfolder"  # Путь к подпапке, которую будем создавать
        url = f"{BASE_URL}/disk/resources"  # URL для операций с ресурсами
        params = {"path": folder_path}  # Параметры: путь к новой подпапке

        # Создаём подпапку с помощью PUT-запроса (в API Яндекс.Диска создание ресурса выполняется через PUT)
        response = requests.put(url, headers=HEADERS, params=params)
        # Проверяем успешное создание (код 201 — Created)
        assert response.status_code == 201, f"Не удалось создать подпапку: {response.text}"

        # Получаем список ресурсов в тестовой папке (GET-запрос)
        params = {"path": TEST_FOLDER}
        response = requests.get(url, headers=HEADERS, params=params)
        # Проверяем успешный ответ (код 200 — OK)
        assert response.status_code == 200, f"Ошибка получения списка ресурсов: {response.status_code}"

        data = response.json()  # Парсим JSON-ответ
        assert "items" in data  # Убеждаемся, что в ответе есть список элементов

        # Проверяем, что созданная подпапка присутствует в списке ресурсов
        found = any(item["name"] == "subfolder" for item in data["items"])
        assert found, "Подпапка не найдена в списке ресурсов"

    def test_upload_and_download_file(self, setup_test_folder):
        """
        Тест PUT/GET: загрузка файла на Диск и последующее скачивание.
        Демонстрирует двухэтапный процесс работы с файлами в API Яндекс.Диска.
        """
        file_path = f"{TEST_FOLDER}/{TEST_FILE_NAME}"  # Полный путь к файлу на Диске
        url_for_upload = f"{BASE_URL}/disk/resources/upload"  # Специальный URL для получения ссылки на загрузку

        # Шаг 1: получаем URL для загрузки файла
        params = {"path": file_path, "overwrite": "true"}  # Параметры: путь и флаг перезаписи
        response = requests.get(url_for_upload, headers=HEADERS, params=params)
        # Проверяем, что URL получен успешно (код 200 — OK)
        assert response.status_code == 200, f"Не удалось получить URL для загрузки: {response.status_code}"
        upload_url = response.json()["href"]  # Извлекаем ссылку для загрузки из ответа


        # Шаг 2: загружаем файл по полученному URL (PUT-запрос)
        response = requests.put(upload_url, data=TEST_FILE_CONTENT)
        # Проверяем успешную загрузку (код 201 — Created)
        assert response.status_code == 201, f"Ошибка загрузки файла: {response.status_code}"

        # Шаг 3: получаем URL для скачивания файла
        params = {"path": file_path}
        response = requests.get(url_for_upload, headers=HEADERS, params=params)
        # Проверяем получение ссылки (код 200 — OK)
        assert response.status_code == 200, f"Не удалось получить URL для скачивания: {response.status_code}"
        download_url = response.json()["href"]  # Извлекаем ссылку для скачивания


        # Шаг 4: скачиваем файл по полученному URL (GET-запрос)
        response = requests.get(download_url)
        # Проверяем успешное скачивание (код 200 — OK)
        assert response.status_code == 200, f"Ошибка скачивания файла: {response.status_code}"
        # Сравниваем содержимое скачанного файла с исходным
        assert response.text == TEST_FILE_CONTENT, "Содержимое файла не совпадает"

    def test_delete_resource(self, setup_test_folder):
        """
        Тест DELETE: удаление ресурса (папки или файла) с Яндекс.Диска.
        Проверяет, что удалённый ресурс больше не доступен.
        """
        resource_to_delete = f"{TEST_FOLDER}/to_be_deleted"  # Путь к ресурсу, который будем удалять
        url = f"{BASE_URL}/disk/resources"  # Базовый URL для операций с ресурсами

        # Сначала создаём ресурс для удаления (папку)
        params = {"path": resource_to_delete}
        response = requests.put(url, headers=HEADERS, params=params)
        # Проверяем создание ресурса (код 201 — Created)
        assert response.status_code == 201, f"Не удалось создать ресурс для удаления: {response.text}"

        # Удаляем ресурс с помощью DELETE-запроса
        params = {"path": resource_to_delete}
        response = requests.delete(url, headers=HEADERS, params=params)
        # Проверяем успешное удаление (коды 202 — Accepted или 204 — No Content)
        assert response.status_code in [202, 204], f"Ошибка удаления ресурса: {response.status_code}"


        # Проверяем, что ресурс действительно удалён (должен вернуть 404 — Not Found)
        params = {"path": resource_to_delete}
        response = requests.get(f"{BASE_URL}/disk/resources", headers=HEADERS, params=params)
        # Убеждаемся, что ресурс больше не существует
        assert response.status_code == 404, "Ресурс не был удалён"
