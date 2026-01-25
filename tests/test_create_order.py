import pytest
import allure
import json
from api.user_api import UserApiClient
from api.order_api import OrderApiClient
from data import valid_ingredients_data, invalid_ingredients_data

class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.step("Создание и авторизация пользователя")
    def test_create_order_with_auth_and_ingredients(self, user_data, login_data):
        user_client = UserApiClient()
        order_client = OrderApiClient()

        create_response = self.create_user(user_client, user_data)
        login_response = self.login_user(user_client, login_data)

        access_token = self.extract_token(login_response)

        order_client = OrderApiClient(token=access_token)
        order_response = self.create_order(order_client, access_token, valid_ingredients_data)
        self.assert_order_creation_success(order_response)

    @allure.step("Создание пользователя через API")
    def create_user(self, user_client, user_data):
        with allure.step("Отправка запроса на создание пользователя"):
            create_response = user_client.create_user(user_data)
        with allure.step("Проверка статус кода ответа"):
            assert create_response.status_code == 200, f"Expected status code 200, but got {create_response.status_code}"
        return create_response

    @allure.step("Логин пользователя через API")
    def login_user(self, user_client, login_data):
        with allure.step("Отправка запроса на логин пользователя"):
            login_response = user_client.login_user(login_data)
        with allure.step("Проверка статус кода ответа"):
            assert login_response.status_code == 200, f"Expected status code 200, but got {login_response.status_code}"
        return login_response

    @allure.step("Извлечение токена из ответа")
    def extract_token(self, login_response):
        with allure.step("Извлечение access token из json ответа"):
            access_token = login_response.json().get('accessToken')
        with allure.step("Проверка, что токен существует"):
            assert access_token is not None, "Access token not found in login response"
        with allure.step("Удаление 'Bearer ' из токена"):
            access_token = access_token.split('Bearer ')[1]
        return access_token

    @allure.step("Создание заказа через API")
    def create_order(self, order_client, access_token, ingredients):
        with allure.step("Установка заголовка авторизации"):
            headers = {'Authorization': f'Bearer {access_token}'}
        with allure.step("Отправка запроса на создание заказа"):
            order_response = order_client.create_order(ingredients)

        return order_response

    @allure.step("Проверка успешности создания заказа")
    def assert_order_creation_success(self, order_response):
        with allure.step("Проверка статус кода ответа"):
            assert order_response.status_code == 200, f"Expected status code 200, but got {order_response.status_code}"
        with allure.step("Проверка, что заказ создан успешно (success == True)"):
            assert order_response.json()["success"] == True

    @allure.title("Создание заказа без авторизации и с ингредиентами")
    @allure.step("Создание заказа без авторизации и с ингредиентами")
    def test_create_order_without_auth_and_with_ingredients(self):
        order_client = OrderApiClient()
        order_response = order_client.create_order(valid_ingredients_data)

        assert order_response.status_code == 200, f"Expected status code 200, but got {order_response.status_code}"
        assert order_response.json()["success"] == True

    @allure.title("Создание заказа с авторизацией и без ингредиентов")
    @allure.step("Создание заказа с авторизацией и без ингредиентов")
    def test_create_order_with_auth_and_no_ingredients(self, user_data, login_data):
        user_client = UserApiClient()
        order_client = OrderApiClient()

        create_response = self.create_user(user_client, user_data)
        login_response = self.login_user(user_client, login_data)

        access_token = self.extract_token(login_response)
        order_client = OrderApiClient(token=access_token)

        order_response = order_client.create_order({"ingredients": []})
        assert order_response.status_code == 400, f"Expected status code 400, but got {order_response.status_code}"
        assert order_response.json()["success"] == False
        assert order_response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа без авторизации и без ингредиентов")
    @allure.step("Создание заказа без авторизации и без ингредиентов")
    def test_create_order_without_auth_and_no_ingredients(self):
        order_client = OrderApiClient()
        order_response = order_client.create_order({"ingredients": []})

        assert order_response.status_code == 400, f"Expected status code 400, but got {order_response.status_code}"
        assert order_response.json()["success"] == False
        assert order_response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.step("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self):
        order_client = OrderApiClient()
        order_response = order_client.create_order(invalid_ingredients_data)

        assert order_response.status_code == 500, f"Expected status code 500, but got {order_response.status_code}"
