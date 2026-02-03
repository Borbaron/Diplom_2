import requests
import allure
from url import Url
import json

class UserApiClient:
    def __init__(self):
        self.base_url = Url.BASE_URL

    @allure.step("Создание пользователя")
    def create_user(self, user_data):
        url = Url.USER_CREATE
        response = requests.post(url, data=json.dumps(user_data), headers={'Content-Type': 'application/json'})
        return response

    @allure.step("Авторизация пользователя")
    def login_user(self, login_data):
        url = Url.USER_LOGIN
        response = requests.post(url, data=json.dumps(login_data), headers={'Content-Type': 'application/json'})
        return response