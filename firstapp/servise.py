from django.core.mail import send_mail


def sending_mail(user_data, message_data):
    send_mail(
        'Ответ Support с сайта SupportTestSite.com',
        f'{user_data.username}, Вам ответили из службы поддержки.\n'
        f'"{message_data.text}"',
        'pustelnikov.ilya@gmail.com',
        # ['vp-11@mail.ru'],
        [user_data.email],
        fail_silently=False,
    )
