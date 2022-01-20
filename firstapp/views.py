from django.shortcuts import render
from rest_framework.viewsets import *
from rest_framework.views import Response, APIView
from firstapp.serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404


# from .tasks import supper_sum


class UserView(ModelViewSet):
    """Список всех имеющихся юзеров"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]


class MessagesView(ViewSet):
    """Список тикетов и сообщений"""
    serializer_class = TicketSerializer

    def list(self, request):
        if request.user.is_staff:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(user_id=request.user.id)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.user.id
        if not Ticket.objects.filter(status='unresolved').exists():
            ticket = Ticket.objects.create(user_id=user_id)
        else:
            if request.user.is_staff:
                return Response(f"Admin user cannot create ticket. Select the required ticket"
                                f" to write message")
            ticket = Ticket.objects.filter(user_id=user_id).last()
        new_message = Message(
            user_id=user_id,
            to_user_id=1,
            text=request.data.get('text'),
            ticket_id=ticket.id
        )
        new_message.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Message.objects.all()
        messages = get_list_or_404(queryset, ticket_id=pk)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class CurrentMessageView(APIView):
    """Список сообщений данного тикета"""

    def get(self, request, pk=None):
        if request.user.is_staff:
            queryset = Message.objects.filter(ticket_id=pk)
        else:
            queryset = Message.objects.filter(user_id=request.user.id, ticket_id=pk)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        user = request.user
        if user.is_staff:
            to_user_id = Ticket.objects.get(id=pk).user_id
        new_message = Message(
            user_id=user.id,
            to_user_id=to_user_id,
            text=request.data.get('text'),
            ticket_id=pk
        )
        new_message.save()
        serializer = MessageSerializer(new_message)
        return Response(serializer.data)

    def put(self, request, pk=None):
        statuses = [status[0] for status in Ticket.STATUS]
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, id=pk)
        new_status = request.data.pop('ticket')
        if new_status not in statuses:
            return Response(f'incorrect status - {new_status}')
        ticket.status = new_status
        ticket.save()
        serializer = TicketSerializer(ticket.status)
        return Response(f'Status has been changed to "{serializer.instance}"')


def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'firstapp/index.html', context)


def ticket_app(request):
    return render(request, 'firstapp/main_app.html')
