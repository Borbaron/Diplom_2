import pytest
import allure
from api.user_api import UserApiClient
from api.order_api import OrderApiClient
from data import generate_user_data

@pytest.fixture(scope="function", name="user_data")
def user_data_fixture():
    """Генерирует данные нового пользователя."""
    with allure.step("Генерация данных пользователя"):
        user_data = generate_user_data()
    return user_data

@pytest.fixture(scope="function", name="login_data")
def login_data_fixture(user_data):
    """Формирует данные для логина пользователя на основе данных пользователя."""
    with allure.step("Формирование данных для логина"):
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
    return login_data

@pytest.fixture()
def user_client():
    """Создает клиент для работы с User API."""
    with allure.step("Создание UserApiClient"):
        user_client = UserApiClient()
    return user_client

@pytest.fixture()
def order_client():
    """Создает клиент для работы с Order API."""
    with allure.step("Создание OrderApiClient"):
        order_client = OrderApiClient()
    return order_client

@pytest.fixture(scope="function")
def auth_token(user_client, user_data, login_data):
    """Создает и авторизует пользователя, возвращает токен доступа."""
    with allure.step("Создание пользователя"):
        user_client.create_user(user_data)

    with allure.step("Логин пользователя"):
        login_response = user_client.login_user(login_data)
        access_token = login_response.json().get('accessToken').split('Bearer ')[1]
    return access_token