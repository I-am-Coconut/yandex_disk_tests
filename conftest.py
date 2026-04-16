import pytest
import requests
import time
from config import BASE_URL, HEADERS, TEST_FOLDER

"""
    #Фикстура pytest: создаёт тестовую папку перед запуском тестов
    и удаляет её после завершения всех тестов в сессии.
    """
@pytest.fixture(scope="session")
def setup_test_folder():
    
    # Формируем URL для работы с ресурсами Яндекс.Диска
    folder_url = f"{BASE_URL}/disk/resources" 
    # Задаём параметры запроса: указываем путь к создаваемой папке
    params = {"path": TEST_FOLDER} 

    # Создаём папку
    # PUT запрос для создания папки на Яндекс.Диске
    response = requests.put(folder_url, headers=HEADERS, params=params) 

    # Проверяем статус ответа: 201 — «создано», 202 — «операция принята в обработку»
    # Если статус не соответствует, прерываем тест с ошибкой
    if response.status_code not in [201, 202]:  # Учитываем 202 Accepted
        pytest.fail(f"Не удалось создать тестовую папку: {response.text}")

    # Ждём завершения операции 2 секунды
    time.sleep(2)

    # Передаём имя папки в тесты 
    yield TEST_FOLDER  # «yield» разделяет подготовку и очистку)

    # Удаляем тестовую папку после завершения всех тестов
    try:
        # DELETE запрос для удаления тестовой папки
        response = requests.delete(folder_url, headers=HEADERS, params={"path": TEST_FOLDER})
        
        # Проверяем статус удаления: 202 — «принято», 204 — «успешно удалено»
        # Если статус не подходит, фиксируем проблему, но не прерываем выполнение
        if response.status_code not in [202, 204]:
            # Записываем предупреждение о проблеме с удалением в лог фикстуры
            pytest.warns(UserWarning, match=f"Не удалось удалить тестовую папку: {response.status_code}")
    except Exception as e:
        # Обрабатываем возможные исключения (например, сетевые ошибки) при удалении папки
        # Прерываем выполнение с ошибкой, если удаление невозможно из‑за исключения
        pytest.fail(f"Критическая ошибка при удалении тестовой папки: {e}")

