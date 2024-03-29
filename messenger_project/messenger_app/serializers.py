from .models import Chat, Message
from rest_framework import serializers

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'name', 'created_at', 'updated_at')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at', 'updated_at', 'sender', 'chat')

class MessageDetailSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at', 'updated_at', 'sender', 'chat')

class MessageCreateSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at', 'updated_at', 'sender', 'chat')
