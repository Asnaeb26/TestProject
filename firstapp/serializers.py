from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        # fields = ('id', 'email', 'username', 'first_name', 'last_name',
        #           'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=True)

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user_id', 'user', 'description')
        # fields = ('__all__')
        # depth = 1


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        # fields = '__all__'
        exclude = ['to_user_id', 'id', 'ticket']
        # fields = ['id', 'user', 'text', 'date_message']
        # depth = 1


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Tickets
        fields = '__all__'
        # depth = 1

