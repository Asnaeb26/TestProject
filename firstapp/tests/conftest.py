import pytest
from django import urls
from faker import Faker

from firstapp.models import Ticket

fake = Faker()


@pytest.fixture
def user_data():
    return {'username': fake.user_name(), 'password': fake.password()}


@pytest.fixture
def faker_admin_data():
    return {'username': 'admin', 'password': 'password'}


@pytest.fixture
def created_user(user_data, django_user_model):
    """Create new user and return user.object"""
    test_user = django_user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user


@pytest.fixture
def created_ticket(django_user_model, created_user):
    """Создает новый тикет"""
    new_ticket = Ticket.objects.create(user_id=created_user.id)
    return new_ticket


@pytest.fixture
def get_token(client, user_data):
    """Передает созданный токен"""
    url = urls.reverse('token_obtain_pair')
    resp = client.post(url, user_data)
    token = resp.data['access']
    return 'Bearer ' + token


@pytest.fixture
def get_token_for_admin(client, faker_admin_data):
    url = urls.reverse('token_obtain_pair')
    resp = client.post(url, faker_admin_data)
    token = resp.data['access']
    return 'Bearer ' + token
