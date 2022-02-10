from django.conf import settings
from django.core.mail import send_mail

from TestProject.celery import app


@app.task
def sending_mail(recipient, username, text):
    title = 'Ответ Support с сайта SupportTestSite.com'
    message = f'Здравствуйте {username}, ' \
              f'Вам ответили из службы поддержки.\n ' \
              f'"{text}"\n'
    send_mail(
        title,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )