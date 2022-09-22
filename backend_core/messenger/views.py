from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView

from . import models, forms


class MessagesListView(LoginRequiredMixin, ListView):
    model = models.PrivateMessage
    template_name = 'messenger/messages_list.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_messages'] = models.PrivateMessage.objects.filter(Q(sender=self.request.user) |
                                                                      Q(receiver=self.request.user))
        return context


class NewMessageView(LoginRequiredMixin, FormView):
    model = models.PrivateMessage
    template_name = 'messenger/new_message.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    form_class = forms.NewMessageForm
    success_url = reverse_lazy('messages:list')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = form.cleaned_data['receiver']
        form.instance.message_text = form.cleaned_data['message_text']
        form.save()
        return HttpResponseRedirect('/messenger/')
