import pytest
from django import urls

from firstapp.models import Ticket


@pytest.fixture
def user_data():
    return {'username': 'TestUser', 'password': '123456789Cc'}


@pytest.fixture
def admin_data():
    return {'username': 'admin', 'password': 'password'}


@pytest.fixture
def message_data():
    return {'text': 'Test message by user'}


@pytest.fixture
def created_user(user_data, django_user_model):
    """Create new user and return user.object"""
    test_user = django_user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user


@pytest.fixture
def created_ticket(django_user_model, created_user):
    """Created new ticket"""
    new_ticket = Ticket.objects.create(user_id=created_user.id)
    return new_ticket


@pytest.fixture
def get_token(client, user_data):
    url = urls.reverse('token_obtain_pair')
    resp = client.post(url, user_data)
    token = resp.data['access']
    return 'Bearer ' + token


@pytest.fixture
def get_token_for_admin(client, admin_data):
    url = urls.reverse('token_obtain_pair')
    resp = client.post(url, admin_data)
    token = resp.data['access']
    return 'Bearer ' + token
