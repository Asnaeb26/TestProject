import pytest
from django import urls

from firstapp.models import Ticket


def test_get_ticket_list(client, created_user, get_token):
    ticket_url = urls.reverse('tickets-list')
    resp = client.get(ticket_url, HTTP_AUTHORIZATION=get_token)
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
