import pytest
from django import urls

from firstapp.models import Message, Ticket


@pytest.mark.django_db
def test_api_jwt(client, created_user, user_data):
    url = urls.reverse('token_obtain_pair')
    resp = client.post(url, user_data)
    assert resp.status_code == 200
    assert 'access' and 'refresh' in resp.data
    token_access = resp.data['access']

    verification_url = urls.reverse('token_verify')
    resp = client.post(verification_url, {'token': token_access}, format='json')
    assert resp.status_code == 200
    resp = client.post(verification_url, {'token': 'fake token'}, format='json')
    assert resp.status_code == 401

    url_messages = urls.reverse('messages')

    resp = client.get(url_messages, HTTP_AUTHORIZATION='Bearer ' + 'fake token')
    assert resp.status_code == 401

    resp = client.get(url_messages, HTTP_AUTHORIZATION='Bearer ' + token_access)
    assert resp.status_code == 200


# @pytest.mark.skip(reason='не готов')
@pytest.mark.django_db
def test_create_message(client, created_user, message_data, get_token):
    """
    Тест проверяет создается ли новый тикет, при создании
    нового сообщения, учитывая то, что все тикеты данного
    пользователя либо не созданы, либо имеют статус
    'Замороженный' или 'Решенный'
    """
    assert Message.objects.count() == 0
    assert Ticket.objects.count() == 0
    messages_url = urls.reverse('messages')
    resp = client.post(messages_url, message_data, HTTP_AUTHORIZATION=get_token)
    assert resp.status_code == 201
    assert Message.objects.count() == 1
    assert Ticket.objects.count() == 1

    resp = client.post(messages_url, message_data, HTTP_AUTHORIZATION=get_token)
    assert resp.status_code == 201
    assert Message.objects.count() == 2
    assert Ticket.objects.count() == 1
    Ticket.objects.filter().update(status='resolved')

    resp = client.post(messages_url, message_data, HTTP_AUTHORIZATION=get_token)
    assert resp.status_code == 201
    assert Message.objects.count() == 3
    assert Ticket.objects.count() == 2



