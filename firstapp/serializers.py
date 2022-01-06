from rest_framework import serializers
from .models import Tickets, UserProfile, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    # user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user_id', 'user', 'description')
        # fields = ('__all__')
        depth = 1


class TicketSerializer(serializers.ModelSerializer):
    all_users = [i.id for i in User.objects.all()]
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.ChoiceField(choices=all_users)
    messages = serializers.SlugRelatedField(slug_field='text', read_only=True, many=True)

    class Meta:
        model = Tickets
        fields = '__all__'
        # fields = ('user_id', 'user', 'message',)
        # exclude = ('id','message')
        # depth = 1
    # def create(self, validated_data):
