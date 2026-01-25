import pytest
from data import generate_user_data

@pytest.fixture(scope="function")
def user_data():
    return generate_user_data()

@pytest.fixture(scope="function")
def login_data(user_data):
    return {
        "email": user_data["email"],
        "password": user_data["password"]
    }


