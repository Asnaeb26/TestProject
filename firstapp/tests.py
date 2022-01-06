from django.test import TestCase
from firstapp.tasks import supper_sum
from django.core.mail import send_mail


def sending_mail():
    send_mail(
        'Ну здарова епта',
        'Вот тебе спамчик сука, переходи по ссылочке и там тебя ждет подарок))))).'
        'https://www.youtube.com/',
        'pustelnikov.ilya@gmail.com',
        ['vp-11@mail.ru', 'Asnaeb26@yandex.by'],
        fail_silently=False,
    )


result = supper_sum.delay(7, 9)
print(result.state)
print(result)