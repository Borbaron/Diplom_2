import requests
import allure
from url import Url

class UserApiClient:
    def __init__(self):
        self.base_url = Url.BASE_URL

    @allure.step("Создание пользователя")
    def create_user(self, user_data):
        url = Url.USER_CREATE
        response = requests.post(url, data=user_data)
        return response
    
    @allure.step("Авторизация пользователя")
    def login_user(self, login_data):
        url = Url.USER_LOGIN
        response = requests.post(url, data=login_data)
        return response

