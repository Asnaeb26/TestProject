from django.shortcuts import get_object_or_404, render
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet

from firstapp.serializers import MessageSerializer, TicketSerializer, UserSerializer

from .models import Message, Ticket, User
from .permissions import IsAuthenticatedAndAdmin
from .tasks import sending_mail


class UserViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MessagesView(ViewSet):
    """Тут кароч сообщения"""
    def list(self, request):
        queryset = Message.objects.filter(user_id=request.user.id)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Message.objects.filter(user_id=request.user.id)
        user = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(user)
        return Response(serializer.data)

# class MessagesView(APIView):
#     """Список тикетов и сообщений"""
#     serializer_class = TicketSerializer
#
#     def get(self, request):
#         if request.user.is_staff:
#             queryset = Ticket.objects.all()
#         else:
#             queryset = Ticket.objects.filter(user_id=request.user.id)
#         serializer = TicketSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         user_id = request.user.id
#         current_object = Ticket.objects.filter(user_id=user_id,
#                                                status='unresolved')
#         if not current_object.exists() and not request.user.is_staff:
#             ticket = Ticket.objects.create(user_id=user_id)
#         else:
#             if request.user.is_staff:
#                 return Response({"message": "Admin user cannot create a ticket"},
#                                 status=HTTP_400_BAD_REQUEST)
#             ticket = current_object.last()
#         ticket_id = ticket.id
#         new_message = Message(
#             user_id=user_id,
#             to_user_id=1,
#             text=request.data.get('text'),
#             ticket_id=ticket_id
#         )
#         if not new_message.text:
#             return Response({'message': 'Message is empty'},
#                             status=HTTP_400_BAD_REQUEST)
#         new_message.save()
#         serializer = TicketSerializer(ticket)
#         return Response({'message': 'Successful new message'},
#                         status=HTTP_201_CREATED)


class TicketsView(ModelViewSet):
    """Список всех тикетов данного тикета"""
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticatedAndAdmin,)
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        else:
            return Ticket.objects.filter(user_id=user.id)

    def create(self, request):
        user_id = request.user.id
        current_object = Ticket.objects.filter(user_id=user_id,
                                               status='unresolved')
        if not current_object.exists() and not request.user.is_staff:
            ticket = Ticket.objects.create(user_id=user_id)
        else:
            if request.user.is_staff:
                return Response({"message": "Admin user cannot create a ticket"},
                                status=HTTP_400_BAD_REQUEST)
            ticket = current_object.last()
        ticket_id = ticket.id
        new_message = Message(
            user_id=user_id,
            to_user_id=1,
            text=request.data.get('text'),
            ticket_id=ticket_id
        )
        if not new_message.text:
            return Response({'message': 'Message is empty'},
                            status=HTTP_400_BAD_REQUEST)
        new_message.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)


class CurrentTicketView(APIView):
    """Список сообщений данного тикета"""
    permission_classes = (IsAuthenticatedAndAdmin, )

    def get(self, request, pk=None):
        if not pk in [ticket.id for ticket in Ticket.objects.all()]:
            return Response({'message': f'No ticket with id = {pk}'},
                            status=HTTP_400_BAD_REQUEST)
        queryset = Message.objects.filter(ticket_id=pk)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, pk=None):
        user = request.user
        if user.is_staff:
            to_user_id = Ticket.objects.get(id=pk).user_id
        else:
            to_user_id = 1
        new_message = Message(
            user_id=user.id,
            to_user_id=to_user_id,
            text=request.data.get('text', None),
            ticket_id=pk
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
            return Response({'message': 'Successful new message'},
                            status=HTTP_201_CREATED)
        return Response({'message': 'Something went wrong'},
                        status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        statuses = [status[0] for status in Ticket.STATUS]
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, id=pk)
        new_status = request.data.pop('status')
        if new_status not in statuses:
            return Response({'message': 'Wrong status'},
                            status=HTTP_400_BAD_REQUEST)
        ticket.status = new_status
        ticket.save()
        return Response({'message': 'Update complete'},
                        status=HTTP_200_OK)


def index(request):
    return render(request, 'firstapp/index.html')
