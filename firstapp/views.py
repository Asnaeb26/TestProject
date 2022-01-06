from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import authentication, permissions, status
from firstapp.models import UserProfile, Tickets
from firstapp.serializers import UserSerializer, UserProfileSerializer, TicketSerializer
from rest_framework.response import Response
from .tasks import supper_sum

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import *


# Signals
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Message)
def create_message(sender, instance, created, **kwargs):
    if created:
        Tickets.objects.create(
            # message_id=instance.id,
            user_id=instance.user_id,

        )


class UserView(ModelViewSet):
    """Список всех имеющихся юзеров"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]


class UserProfileView(ModelViewSet):
    """Профильная информация юзеров"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # permission_classes = [IsAdminUser]


class TicketView(ModelViewSet):
    """Список всех тикетов"""
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer

    # permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        data = request.data
        statuses = [i[0] for i in Tickets.STATUS]
        current_id = data['id']
        status_message = data['status']
        if status_message in statuses:
            Tickets.objects.filter(id=current_id).update(
                status=status_message
            )
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f"incorrect status - '{status_message}'"})


def index(request):
    ls = (1, 2, 4, 5, 6)
    context = {
        'users': User.objects.all(),
        'nums': ls
    }
    return render(request, 'firstapp/index.html', context)


def profile(request, pk):
    current_user = User.objects.get(id=pk)
    context = {
        'current_user': current_user
    }
    return render(request, 'firstapp/profile.html', context)


def messages(request):
    current_id = request.user.id
    received_message = Message.objects.filter(to_user_id=current_id)
    sent_message = Message.objects.filter(user_id=current_id)
    sender = User.objects.get(id=sent_message[0].to_user_id)
    context = {
        'sender': sender,
        'received_message': received_message,
        'sent_message': sent_message
    }
    return render(request, 'firstapp/messages.html', context)


def add_message(request):
    # message = request.GET['text_message']
    to_user_id = request.POST['user_from_id']
    new_message = Message(
        user_id=request.user.id,
        to_user_id=request.POST['user_from_id'],
        message=request.POST['text_message']
    )
    new_message.save()
    # return HttpResponseRedirect('firstapp/profile.html')
    return render(request, 'firstapp/profile.html')