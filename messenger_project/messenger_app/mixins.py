from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse

class LoginRequiredMixin(object):
    @login_required
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class SuccessMessageMixin(object):
    success_message = ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class RedirectMixin(object):
    redirect_url = ''

    def get_success_url(self):
        return self.redirect_url

class ChatPermissionMixin(object):
    def has_permission(self, request, chat_id):
        chat = get_object_or_404(Chat, pk=chat_id)
        return chat.has_permission(request.user)

    def dispatch(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        if not self.has_permission(request, chat_id):
            messages.error(request, "У вас нет доступа к этому чату.")
            return redirect('home')
        return super(ChatPermissionMixin, self).dispatch(request, *args, **kwargs)

class MessagePermissionMixin(object):
    def has_permission(self, request, message_id):
        message = get_object_or_404(Message, pk=message_id)
        return message.has_permission(request.user)

    def dispatch(self, request, *args, **kwargs):
        message_id = kwargs.get('message_id')
        if not self.has_permission(request, message_id):
            messages.error(request, "У вас нет доступа к этому сообщению.")
            return redirect('home')
        return super(MessagePermissionMixin, self).dispatch(request, *args, **kwargs)

class FormValidMixin(object):
    def form_valid(self, form):
        return super(FormValidMixin, self).form_valid(form)

class FormInvalidMixin(object):
    def form_invalid(self, form):
        return super(FormInvalidMixin, self).form_invalid(form)

class PaginateMixin(object):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PaginateMixin, self).get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get('page')
        context['paginator'] = paginator
        context['page_obj'] = paginator.get_page(page)
        return context

class SearchMixin(object):
    search_fields = []

    def get_queryset(self):
        queryset = super(SearchMixin, self).get_queryset()
        search_term = self.request.GET.get('q')
        if search_term:
            queryset = queryset.filter(Q(**{field: search_term for field in self.search_fields}))
        return queryset

class AjaxFormMixin(object):
    def form_valid(self, form):
        if self.request.is_ajax():
            response = super(AjaxFormMixin, self).form_valid(form)
            return HttpResponse('success')
        else:
            return super(AjaxFormMixin, self).form_valid(form)
