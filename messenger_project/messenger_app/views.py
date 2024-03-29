from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessageDetailSerializer, MessageCreateSerializer
from rest_framework import viewsets

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.filter(user=self.request.user)
    serializer_class = ChatSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.filter(chat__user=self.request.user)
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(chat__user=self.request.user)

class MessageDetailViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.kwargs['pk'])

class MessageCreateViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
