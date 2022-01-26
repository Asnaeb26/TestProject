import pytest


@pytest.fixture
def user_data():
    return {'username': 'TestUser5', 'password': '123456789Cc'}


@pytest.fixture
def get_name():
    return {'a': 'Ilya', 'b': 'Max'}