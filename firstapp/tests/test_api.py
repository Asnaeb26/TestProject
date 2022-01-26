import os
from django import urls
from django.contrib.auth import get_user_model
from firstapp.models import Ticket, Message
import pytest
from firstapp.tasks import divisor


@pytest.mark.skip(reason='не готов')
@pytest.mark.django_db
def test_create_new_message(client, user_data):
    """
    Тест проверяет создается ли новый тикет, при создании
    нового сообщения, учитывая то, что все тикеты данного
    пользователя либо не созданы, либо имеют статус
    'Замороженный' или 'Решенный'
    """
    pass


# @pytest.mark.parametrize('a, b, exp_res', [(19, 1, 19),
#                                            (25, 5, 5),
#                                            (20, 2, 10)])
# def test_divisor_good(a, b, exp_res):
#     assert divisor(a, b) == exp_res


# @pytest.mark.parametrize('param', [
#     'home',
#     'messages'
# ])
# def test_render_views(client, param):
#     temp_url = urls.reverse(param)
#     resp = client.get(temp_url)
#     assert resp.status_code == 401


@pytest.mark.django_db
def test_login(client, user_data):
    user_model = get_user_model()
    assert user_model.objects.count() == 0
    signup_url = urls.reverse('sign_up_page')
    resp = client.post(signup_url, user_data)
    assert user_model.objects.count() == 1
    assert resp.status_code == 302