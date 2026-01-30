import requests
import allure
from url import Url

class OrderApiClient:
    def __init__(self):
        self.base_url = Url.BASE_URL

    @allure.step("Создание заказа")
    def create_order(self, order_data, auth_token=None):
        url = Url.ORDER_CREATE
        headers = {}
        if auth_token: # Если токен передан, добавляем заголовок авторизации
            headers['Authorization'] = f'Bearer {auth_token}'

        response = requests.post(url, json=order_data, headers=headers)
        return response
