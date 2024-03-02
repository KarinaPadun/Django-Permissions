from django.urls import path
from .views import chat_detail, edit_message, add_user_to_chat, remove_user_from_chat

app_name = 'messenger_app'

urlpatterns = [
    path('chat/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('add_user/<int:chat_id>/', add_user_to_chat, name='add_user_to_chat'),
    path('remove_user/<int:chat_id>/<int:user_id>/', remove_user_from_chat, name='remove_user_from_chat'),

]
