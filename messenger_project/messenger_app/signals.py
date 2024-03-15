from django.contrib.auth.signals import user_logged_in
from .models import Message

def log_user_login(sender, user, request, **kwargs):
    LogEntry.objects.create(
        user=user,
        action="Logged in",
        content_type=ContentType.objects.get_for_model(user),
        object_id=user.id,
    )

def log_message_send(sender, message, **kwargs):
    if message.recipient.is_superuser:
        messages.success(message.sender, "Вы успешно отправили сообщение суперюзеру")
        LogEntry.objects.create(
            user=message.sender,
            action="Sent message",
            content_type=ContentType.objects.get_for_model(message),
            object_id=message.id,
        )
