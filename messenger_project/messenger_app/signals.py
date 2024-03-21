from .models import Message
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import UserStatus

def user_logged_in_handler(sender, user, **kwargs):
    user_status = UserStatus.objects.get_or_create(user=user)[0]
    user_status.status = True
    user_status.save()

def user_logged_out_handler(sender, user, **kwargs):
    user_status = UserStatus.objects.get(user=user)
    user_status.status = False
    user_status.save()

user_logged_in.connect(user_logged_in_handler)
user_logged_out.connect(user_logged_out_handler)

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
