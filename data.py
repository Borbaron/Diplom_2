import random
import string
from faker import Faker

def generate_user_data(length=10):

    fake = Faker()

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    name = generate_random_string(length)
    password = generate_random_string(length)

    email = fake.email()

    return {
        "email": email,
        "password": password,
        "name": name
    }

valid_ingredients_data = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
invalid_ingredients_data = {"ingredients": ["invalid_ingredient_id"]}