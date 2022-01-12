from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, GenericAPIView
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import Response
from rest_framework.permissions import *
from rest_framework import authentication, status
from firstapp.models import *
from firstapp.serializers import *

from .tasks import supper_sum


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


class MessageView(ModelViewSet):
    """Список сообщений"""

    serializer_class = MessageSerializer

    def get_permissions(self):
        if self.action == 'delete':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user_id = self.request.user
        return Message.objects.filter(user_id=user_id)

    def create(self, request):
        user_id = request.user.id

        obj = Tickets.objects.filter(user_id=user_id)
        # if not obj.exists() or (obj.exists() and obj.exclude(status='unresolved')):
        #     new_ticket = Tickets.objects.create(user_id=user_id)
        #     ticket_id = new_ticket.id
        # else:
        #     current_ticket = obj.get(status="unresolved")
        #     ticket_id = current_ticket.id

        new_message = Message(
            user_id=user_id,
            to_user_id=request.data.get('to_user_id', 1),
            text=request.data.get('text'),
            # ticket_id=ticket_id
        )
        new_message.save()
        serializer = MessageSerializer(new_message)
        return Response(serializer.data)


class TicketView(ModelViewSet):
    """Список всех тикетов"""
    serializer_class = TicketSerializer

    def get_queryset(self):
        user_id = self.request.user
        return Tickets.objects.filter(user_id=user_id)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    # def list(self, request):
    #     # if request.user.
    #     queryset = Tickets.objects.filter(user_id=request.user.id)
    #     serializer = TicketSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Tickets.objects.filter(user_id=request.user.id)
    #     ticket = get_object_or_404(queryset, pk=pk)
    #     serializer = TicketSerializer(ticket)
    #     return Response(serializer.data)


class AllTicketView(ModelViewSet):
    """Список всех тикетов"""
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer

    permission_classes = [IsAdminUser]


def get_permissions(self):
    if self.action == 'list' or self.action == 'create':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]


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
