from django.shortcuts import render, HttpResponseRedirect, Http404
from rest_framework.status import *
from rest_framework.viewsets import *
from rest_framework.views import Response, APIView
from firstapp.serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout


# from .tasks import supper_sum


class MessagesView(APIView):
    """Список тикетов и сообщений"""
    serializer_class = TicketSerializer

    def get(self, request):
        if request.user.is_staff:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(user_id=request.user.id)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.user.id
        current_object = Ticket.objects.filter(user_id=user_id, status='unresolved')
        if not current_object.exists() and not request.user.is_staff:
            ticket = Ticket.objects.create(user_id=user_id)
        else:
            if request.user.is_staff:
                return Response({"message": "Admin user cannot create a ticket. Select the required ticket"
                                            " to write message"})
            ticket = current_object.last()
        ticket_id = ticket.id
        new_message = Message(
            user_id=user_id,
            to_user_id=1,
            text=request.data.get('text'),
            ticket_id=ticket_id
        )
        new_message.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)


class CurrentMessageView(APIView):
    """Список сообщений данного тикета"""

    def get(self, request, pk=None):
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
            return Response({'message': 'Message is empty'}, status=HTTP_400_BAD_REQUEST)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_message.save()
        if new_message:
            return Response({'message': 'Successful new message'}, status=HTTP_201_CREATED)
        return Response({'message': 'Something went wrong'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        statuses = [status[0] for status in Ticket.STATUS]
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, id=pk)
        new_status = request.data.pop('status')
        if new_status not in statuses:
            return Response({'message': 'Wrong status'}, status=HTTP_400_BAD_REQUEST)
        ticket.status = new_status
        ticket.save()
        serializer = TicketSerializer(ticket.status)
        return Response({'message': 'Update complete'}, status=HTTP_200_OK)


def index(request):
    context = {}
    return render(request, 'firstapp/main_app.html')


def login_page(request):
    # return HttpResponseRedirect('/')
    return render(request, 'firstapp/login.html')


def do_login(request):
    user = authenticate(
        username=request.POST.get('username'),
        password=request.POST.get('password')
    )
    if user:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        raise Http404


def sign_up_page(request):
    return render(request, 'firstapp/sign_up.html')


def do_sign_up(request):
    password = request.POST['password']
    username = request.POST['username']

    new_user = User.objects.create_user(username=username, password=password, email='test@mail.ru')
    if new_user:
        login(request, new_user)
        return HttpResponseRedirect('/')
    else:
        raise Http404
