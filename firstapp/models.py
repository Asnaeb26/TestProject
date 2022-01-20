from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    STATUS = [
        ('unresolved', 'Нерешенная'),
        ('resolved', 'Решенная'),
        ('freezy', 'Замороженная'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='unresolved',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ticket №{self.id} created by {self.user}'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    text = models.TextField("Текст")
    date_message = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f'Message id:{self.id} created by {self.user}'