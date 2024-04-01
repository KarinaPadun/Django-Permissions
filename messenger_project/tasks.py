from celery import shared_task
from .models import Message

@shared_task
def log_messages():
    messages = Message.objects.order_by('-created_at')[:10]
    for message in messages:
        print(f"[{message.created_at}] {message.sender}: {message.text}")

