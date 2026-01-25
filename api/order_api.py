import requests
import allure
from url import Url

class OrderApiClient:
    def __init__(self, token=None):
        self.base_url = Url.BASE_URL
        self.token = token

    @allure.step("Создание заказа")
    def create_order(self, ingredients_data):
        url = Url.ORDER_CREATE
        response = requests.post(url, data=ingredients_data)
        return response