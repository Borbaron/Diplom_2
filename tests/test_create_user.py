import pytest
import allure
import copy
from api.user_api import UserApiClient


@allure.suite("Создание пользователя")
class TestCreateUser:

    @allure.title("Запрос на создание пользователя возвращает код ответа 200 для успешного создания")
    def test_create_user_returns_200_on_success(self, user_data):
        user_client = UserApiClient() 
        response = user_client.create_user(user_data)
        assert response.status_code == 200, f"Ожидался код ответа 200, получен {response.status_code}"

        assert response.json()["success"] == True, "Поле 'success' должно быть True"
        assert "user" in response.json(), "Поле 'user' отсутствует в ответе"
        assert "email" in response.json()["user"], "Поле 'email' отсутствует в user"
        assert "name" in response.json()["user"], "Поле 'name' отсутствует в user"
        assert "accessToken" in response.json(), "Поле 'accessToken' отсутствует"
        assert "refreshToken" in response.json(), "Поле 'refreshToken' отсутствует"

    @allure.title("Попытка создания уже зарегистрированного пользователя возвращает код ответа 403 и сообщение об ошибке")
    def test_create_existing_user_returns_403(self, user_data):
        user_client = UserApiClient() 
        user_client.create_user(user_data)
        response = user_client.create_user(user_data)
        response_body = response.json()
        assert response.status_code == 403, f"Ожидался код ответа 403, получен {response.status_code}"
        assert response_body["success"] == False, "Поле 'success' должно быть False"
        assert "message" in response_body, "Поле 'message' отсутствует в ответе"
        assert response_body["message"] == "User already exists", "Сообщение об ошибке не соответствует ожидаемому"

    @allure.title("Попытка создания пользователя с отсутствующим обязательным полем возвращает код ответа 403 и сообщение об ошибке")
    def test_create_user_with_missing_field_returns_400(self, user_data):
        user_client = UserApiClient()
        user_data_missing_email = copy.deepcopy(user_data) 
        del user_data_missing_email["email"]

        response = user_client.create_user(user_data_missing_email)
        response_body = response.json()

        assert response.status_code == 403, f"Ожидался код ответа 403, получен {response.status_code}"
        assert response_body["success"] == False, "Поле 'success' должно быть False"
        assert response_body["message"] == "Email, password and name are required fields"

