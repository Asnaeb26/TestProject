import pytest
from django import urls

from firstapp.models import Ticket


@pytest.mark.django_db
def test_api_jwt(client, created_user, faker_user_data):
    url = urls.reverse('token_obtain_pair')
    resp = client.post(url, faker_user_data)
    assert resp.status_code == 200
    assert 'access' and 'refresh' in resp.data
    token_access = resp.data['access']

    verification_url = urls.reverse('token_verify')
    resp = client.post(verification_url, {'token': token_access}, format='json')
    assert resp.status_code == 200
    resp = client.post(verification_url, {'token': 'fake token'}, format='json')
    assert resp.status_code == 401

    url_messages = urls.reverse('tickets-list')

    resp = client.get(url_messages, HTTP_AUTHORIZATION='Bearer ' + 'fake token')
    assert resp.status_code == 401

    resp = client.get(url_messages, HTTP_AUTHORIZATION='Bearer ' + token_access)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_delete_ticket_by_admin(client, admin_user, get_token_for_admin, created_ticket):
    """Тест проверяет способность удалять тикеты администратором"""
    assert Ticket.objects.count() == 1
    ticket_id = created_ticket.id
    ticket_url = urls.reverse('tickets-detail', kwargs={'id': ticket_id})
    resp = client.delete(ticket_url, HTTP_AUTHORIZATION=get_token_for_admin)
    assert resp.status_code == 204
    assert Ticket.objects.count() == 0


@pytest.mark.django_db
def test_delete_ticket_by_user(client, created_user, get_token, created_ticket):
    """Тест проверяет способность удалять тикеты юзером"""
    assert Ticket.objects.count() == 1
    ticket_id = created_ticket.id
    ticket_url = urls.reverse('tickets-detail', kwargs={'id': ticket_id})
    resp = client.delete(ticket_url, HTTP_AUTHORIZATION=get_token)
    assert resp.status_code == 403
    assert Ticket.objects.count() == 1


def test_name1(faker):
    print(faker.unique)
    pass