from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)

    if not chat.has_permission(request.user):
        messages.error(request, "У вас нет доступа к этому чату.")
        return redirect('home')

    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat = chat
            message.save()
            messages.success(request, 'Сообщение отправлено.')
            form = MessageForm()

    return render(request, 'messenger_app/chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    if not message.has_permission(request.user):
        messages.error(request, "У вас нет доступа к этому сообщению.")
        return redirect('home')

    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отредактировано.')
            return redirect('messenger_app:chat_detail', chat_id=message.chat.id)

    form = MessageForm(instance=message)
    return render(request, 'messenger_app/edit_message.html', {'form': form, 'message': message})

