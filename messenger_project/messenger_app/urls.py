from django.urls import path
from .views import chat_detail, edit_message

app_name = 'messenger_app'

urlpatterns = [
    path('chat/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    # Добавьте другие URL-маршруты по мере необходимости
]
