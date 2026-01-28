import pytest
import allure
from api.order_api import OrderApiClient
from data import valid_ingredients_data, invalid_ingredients_data

class TestCreateOrder:

    @allure.title("Создание заказа (пользователь авторизован, есть ингредиенты)")
    def test_create_order_authorized_with_ingredients(self, order_client, auth_token):
        with allure.step("Создание заказа с ингредиентами"):
            order_response = order_client.create_order(valid_ingredients_data, auth_token=auth_token)

        with allure.step("Проверка успешности создания заказа"):
            assert order_response.status_code == 200
            assert order_response.json()["success"] is True

    @allure.title("Создание заказа (пользователь не авторизован, есть ингредиенты)")
    def test_create_order_unauthorized_with_ingredients(self, order_client):
        with allure.step("Создание заказа с ингредиентами"):
            order_response = order_client.create_order(valid_ingredients_data)

        with allure.step("Проверка успешности создания заказа"):
            assert order_response.status_code == 200
            assert order_response.json()["success"] is True

    @allure.title("Создание заказа (пользователь авторизован, нет ингредиентов)")
    def test_create_order_authorized_no_ingredients(self, order_client, auth_token):
        with allure.step("Создание заказа без ингредиентов"):
            order_response = order_client.create_order({"ingredients": []}, auth_token=auth_token)

        with allure.step("Проверка ошибки при создании заказа без ингредиентов"):
            assert order_response.status_code == 400
            assert order_response.json()["success"] is False
            assert order_response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа (пользователь не авторизован, нет ингредиентов)")
    def test_create_order_unauthorized_no_ingredients(self, order_client):
        with allure.step("Создание заказа без ингредиентов"):
            order_response = order_client.create_order({"ingredients": []})

        with allure.step("Проверка ошибки при создании заказа без ингредиентов"):
            assert order_response.status_code == 400
            assert order_response.json()["success"] is False
            assert order_response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, order_client):
        with allure.step("Создание заказа с неверным хешем ингредиентов"):
            order_response = order_client.create_order(invalid_ingredients_data)

        with allure.step("Проверка ошибки при создании заказа с неверным хешем"):
            assert order_response.status_code == 500
