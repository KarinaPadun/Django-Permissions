from django.urls import path, include
from .views import ChatViewSet, MessageViewSet, MessageDetailViewSet, MessageCreateViewSet

urlpatterns = [
    path('chats/', ChatViewSet.as_view({'get': 'list'})),
    path('messages/', MessageViewSet.as_view({'get': 'list'})),
    path('messages/<int:pk>/', MessageDetailViewSet.as_view({'get': 'retrieve'})),
    path('messages/create/', MessageCreateViewSet.as_view({'post': 'create'})),
]
