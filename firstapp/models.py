from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_supportive = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Tickets(models.Model):
    STATUS = [
        ('unresolved', 'Нерешенная'),
        ('resolved', 'Решенная'),
        ('freezy', 'Замороженная'),
    ]
    # title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='unresolved',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # messages = models.ManyToManyField(Message, verbose_name='сообщения')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    to_user_id = models.IntegerField(default=0)
    text = models.TextField("Текст")
    date_message = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
