from django.contrib.auth.signals import user_logged_in
from .models import Message

user_logged_in.connect(log_user_login)
message_sent.connect(log_message_send)
