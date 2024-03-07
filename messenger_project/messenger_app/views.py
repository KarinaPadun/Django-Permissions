from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView, CreateView

from .models import Chat, Message
from .mixins import LoginRequiredMixin, ChatPermissionMixin, MessagePermissionMixin, FormValidMixin

@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    return render(request, 'messenger_app/chat_list.html', {'chats': chats})

class ChatDetailView(LoginRequiredMixin, ChatPermissionMixin, DetailView):
    model = Chat

class EditMessageView(LoginRequiredMixin, MessagePermissionMixin, UpdateView):
    model = Message
    fields = ['content']

class CreateMessageView(LoginRequiredMixin, ChatPermissionMixin, FormValidMixin, CreateView):
    model = Message
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.chat = Chat.objects.get(pk=self.kwargs['chat_id'])
        return super(CreateMessageView, self).form_valid(form)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    if not message.has_permission(request.user):
        messages.error(request, "У вас нет доступа к этому сообщению.")
        return redirect('home')

    message.delete()
    messages.success(request, "Сообщение удалено.")
    return redirect('messenger_app:chat_detail', chat_id=message.chat.id)
