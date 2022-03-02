from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework import permissions
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from firstapp.models import Message, Ticket, User
from firstapp.permissions import MessagePermission, TicketPermission
from firstapp.serializers import MessageSerializer, TicketSerializer
from firstapp.tasks import sending_mail


def send_mail_to_user(to_user_id: int, text: str):
    recipient = User.objects.get(id=to_user_id)
    return sending_mail.delay(recipient.email,
                              recipient.username,
                              text)


class MessagesViewSet(ModelViewSet):
    """Список сообщений данного пользователя"""
    serializer_class = MessageSerializer
    permission_classes = (MessagePermission,)
    lookup_field = 'pk'

    def get_queryset(self):
        return Message.objects.filter(ticket_id=self.kwargs.get('id'))

    def create(self, request, *args, **kwargs):
        ticket_id = kwargs.get('id')
        user = request.user
        if user.is_staff:
            to_user_id = Ticket.objects.filter(id=ticket_id).values_list('user_id', flat=True)[0]
        else:
            to_user_id = 1
        data = dict(
            user_id=user.id,
            ticket_id=ticket_id,
            to_user_id=to_user_id,
            text=request.data.get('text')
        )
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if user.is_staff:
            send_mail_to_user(to_user_id, serializer.validated_data['text'])
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
