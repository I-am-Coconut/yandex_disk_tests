import requests
from config import DISK_INFO_URL, HEADERS

def test_get_disk_info_success():
    """Тест: получаем информацию о Диске (успешный случай)"""
    response = requests.get(DISK_INFO_URL, headers=HEADERS)

    # Проверяем, что статус ответа — 200 OK
    assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

    data = response.json()

    # Проверяем наличие основных полей в ответе
    assert "total_space" in data, "В ответе нет поля total_space"
    assert "used_space" in data, "В ответе нет поля used_space"
    assert "trash_size" in data, "В ответе нет поля trash_size"
    assert isinstance(data["total_space"], int), "total_space должен быть числом"
    print("Информация о Диске успешно получена!")

def test_get_disk_info_unauthorized():
    """Тест: ошибка авторизации (неверный токен)"""
    bad_headers = {"Authorization": "OAuth invalid_token"}
    response = requests.get(DISK_INFO_URL, headers=bad_headers)

    # При неверном токене ожидается код 401 Unauthorized
    assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
    print("Тест ошибки авторизации пройден!")
