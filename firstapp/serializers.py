from rest_framework import serializers

from .models import Message, Ticket


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        exclude = ['ticket']


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True,
                                 source='message_set')

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'status', 'messages']
