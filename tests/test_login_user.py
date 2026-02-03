import pytest
import allure
from api.user_api import UserApiClient

@allure.suite("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация пользователя возвращает код ответа 200, accessToken и refreshToken")
    def test_login_user_returns_200_and_tokens_on_success(self, user_data, login_data):
        user_client = UserApiClient()
        user_client.create_user(user_data)
        response = user_client.login_user(login_data)

        assert response.status_code == 200, f"Ожидался код ответа 200, получен {response.status_code}"
        response_body = response.json()
        assert response_body["success"] == True, "Поле 'success' должно быть True"
        assert "accessToken" in response_body, "Поле 'accessToken' отсутствует в ответе"
        assert "refreshToken" in response_body, "Поле 'refreshToken' отсутствует в ответе"
        assert "user" in response_body, "Поле 'user' отсутствует в ответе"
        assert "email" in response_body["user"], "Поле 'email' отсутствует в user"
        assert "name" in response_body["user"], "Поле 'name' отсутствует в user"

    @allure.title("Неуспешная авторизация с неверным логином/паролем")
    def test_login_user_fails_with_invalid_credentials(self):
        user_client = UserApiClient()
        invalid_login_data = {
            "email": "invalid_user@example.com",
            "password": "invalid_password"
        }
        
        response = user_client.login_user(invalid_login_data)

        assert response.status_code == 401, f"Ожидался код ответа 401, получен {response.status_code}"
        response_body = response.json()
        assert response_body["success"] == False, "Поле 'success' должно быть False"
        assert "message" in response_body, "Поле 'message' отсутствует в ответе"
        assert response_body["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"
