from django.shortcuts import get_object_or_404, render
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet

from firstapp.serializers import MessageSerializer, TicketSerializer

from .models import Message, Ticket, User
from .permissions import IsAuthenticatedAndAdmin
from .tasks import sending_mail


class MessagesView(ModelViewSet):
    """Список тикетов и сообщений"""
    serializer_class = MessageSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        ticket_id = self.kwargs.get('id')
        return Message.objects.filter(ticket_id=ticket_id)

    def create(self, request, id=None):
        user = request.user
        if user.is_staff:
            to_user_id = Ticket.objects.get(id=id).user_id
        else:
            to_user_id = 1
        new_message = Message(
            user_id=user.id,
            to_user_id=to_user_id,
            text=request.data.get('text', None),
            ticket_id=id
        )
        if not new_message.text:
            return Response({'message': 'Message is empty'},
                            status=HTTP_400_BAD_REQUEST)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_message.save()
        if new_message:
            if user.is_staff:
                recipient = User.objects.get(id=to_user_id)
                sending_mail.delay(recipient.email,
                                   recipient.username,
                                   new_message.text)
            serializer = MessageSerializer(new_message)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response({'message': 'Something went wrong'},
                        status=HTTP_400_BAD_REQUEST)


class TicketsView(ModelViewSet):
    """Список сообщений данного тикета"""
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticatedAndAdmin,)
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


def index(request):
    return render(request, 'firstapp/index.html')
