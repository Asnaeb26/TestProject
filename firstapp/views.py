from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from firstapp.models import Message, Ticket, User
from firstapp.permissions import MessagePermission, TicketPermission
from firstapp.serializers import MessageSerializer, TicketSerializer
from firstapp.tasks import sending_mail


def send_mail_to_user(self, to_user_id: int, text: str):
    recipient = User.objects.get(id=to_user_id)
    return sending_mail.delay(recipient.email,
                              recipient.username,
                              text)


class MessageAction:

    def __init__(self, user, ticket_id: int, text: str):
        self.user = user
        self.ticket_id = ticket_id
        self.text = text

    def to_user_id(self):
        """Метод определяет id пользователя, которому предназначено сообщение"""
        # current_ticket = Ticket.objects.filter(id=self.ticket_id).values_list('user_id', flat=True)[0]
        current_ticket = get_object_or_404(Ticket, id=self.ticket_id)
        if self.user.is_staff:
            return current_ticket.user_id
        return 1  # id администратора

    def send_mail_to_user(self):
        """Отправляет уведомление пользователю на электронную почту"""
        recipient = User.objects.get(id=self.to_user_id())
        return sending_mail.delay(recipient.email,
                                  recipient.username,
                                  self.text)

    def create_data(self):
        """Создает словарь со следующими данными о:
        1. id данного юзера
        2. id данного тикета
        3. id юзера, которому будет предназначено сообщение
        4. текст сообщения
        """
        return {
            'user_id': self.user.id,
            'ticket_id': self.ticket_id,
            'to_user_id': self.to_user_id(),
            'text': self.text
        }


class MessagesViewSet(ModelViewSet):
    """Список сообщений данного пользователя"""
    serializer_class = MessageSerializer
    permission_classes = (MessagePermission,)
    lookup_field = 'pk'

    def get_queryset(self):
        return Message.objects.filter(ticket_id=self.kwargs.get('id'))

    def create(self, request, *args, **kwargs):
        message = MessageAction(
            request.user,  # user
            kwargs.get('id'),  # ticket_id
            request.data.get('text')  # text
        )
        data = message.create_data()
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.user.is_staff:
            message.send_mail_to_user()
        return Response(serializer.data, status=HTTP_201_CREATED)


class TicketsViewSet(ModelViewSet):
    """Список тикетов пользователя"""
    serializer_class = TicketSerializer
    permission_classes = (TicketPermission,)
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(user_id=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return Response({"message": "Admin user cannot create a ticket"},
                            status=HTTP_400_BAD_REQUEST)
        queryset = Ticket.objects.create(user_id=user.id)
        serializer = TicketSerializer(queryset)
        return Response(serializer.data, status=HTTP_201_CREATED)
