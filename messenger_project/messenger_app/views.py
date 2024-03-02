from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Chat, Message, UserProfile
from .forms import MessageForm
from .permissions import IsChatUserOrSuperuser, IsChatSuperuser
from rest_framework import viewsets
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, users=request.user)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat
            message.save()
            messages.success(request, 'Message sent successfully.')
            form = MessageForm()

    return render(request, 'messenger_app/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, author=request.user, timestamp__gte=timezone.now() - timezone.timedelta(days=1))

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message edited successfully.')
    else:
        form = MessageForm(instance=message)

    return render(request, 'messenger_app/edit_message.html', {'form': form, 'message': message})

@login_required
def add_user_to_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, users=request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        user_to_add = get_object_or_404(User, username=username, profile__is_active=True)
        chat.users.add(user_to_add)
        messages.success(request, f'{username} added to the chat.')
    return redirect('messenger_app:chat_detail', chat_id=chat_id)

@login_required
def remove_user_from_chat(request, chat_id, user_id):
    chat = get_object_or_404(Chat, id=chat_id, users=request.user)
    user_to_remove = get_object_or_404(User, id=user_id)
    chat.users.remove(user_to_remove)
    messages.success(request, f'{user_to_remove.username} removed from the chat.')
    return redirect('messenger_app:chat_detail', chat_id=chat_id)

