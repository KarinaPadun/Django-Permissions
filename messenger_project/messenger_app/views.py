from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView, CreateView

from .models import Chat, Message
from .mixins import LoginRequiredMixin, ChatPermissionMixin, MessagePermissionMixin, FormValidMixin

from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import DetailView, UpdateView
from .models import File


class FileCreateView(CreateView):
    model = File
    fields = ['name', 'file']
    success_url = '/'


class FileListView(ListView):
    model = File
    template_name = 'file_list.html'



class FileDetailView(DetailView):
    model = File
    template_name = 'file_detail.html'

class FileUpdateView(UpdateView):
    model = File
    fields = ['content']
    template_name = 'file_edit.html'

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        if self.object.content_type.startswith('text/'):
            form.fields['content'].widget = forms.Textarea()
        return form





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
