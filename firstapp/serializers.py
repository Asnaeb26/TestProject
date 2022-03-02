from rest_framework import serializers

from .models import Message, Ticket


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        exclude = ('ticket',)

    def create(self, validated_data):
        user_id = self.initial_data.get('user_id')
        ticket_id = self.initial_data.get('ticket_id')
        to_user_id = self.initial_data.get('to_user_id')
        return Message.objects.create(
            user_id=user_id,
            to_user_id=to_user_id,
            ticket_id=ticket_id,
            text=validated_data.get('text'),
        )


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'status',)
