from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, FormMixin

import users.models
from . import models, forms


class MessengerListView(LoginRequiredMixin, ListView):
    model = models.PrivateMessage
    login_url = reverse_lazy('users:login')
    raise_exception = False


class InboxView(MessengerListView):
    template_name = 'messenger/messages_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = models.PrivateMessage.objects.filter(receiver=self.request.user).order_by('-sent')
        context['msgs'] = msgs
        context['inbox'] = True

        return context


class OutboxView(MessengerListView):
    template_name = 'messenger/messages_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = models.PrivateMessage.objects.filter(sender=self.request.user).order_by('-sent')
        context['msgs'] = msgs
        context['inbox'] = False

        return context


class ConversationsListView(MessengerListView):
    template_name = 'messenger/conversations.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs_in = models.PrivateMessage.objects.filter(receiver=self.request.user)
        msgs_out = models.PrivateMessage.objects.filter(sender=self.request.user)
        senders = []
        receivers = []

        for msg in msgs_in:
            sender_profile = users.models.UserProfile.objects.get(user=msg.sender)
            sender_id = msg.sender.id
            sender_set = (sender_id, sender_profile)
            senders.append(sender_set)

        for msg in msgs_out:
            receiver_profile = users.models.UserProfile.objects.get(user=msg.receiver)
            receiver_id = get_user_model().objects.get(username=receiver_profile.user.username).id
            receiver_set = (receiver_id, receiver_profile)
            receivers.append(receiver_set)

        addresates = list(set(list(chain(senders, receivers))))
        context['addresates'] = addresates

        return context


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'messenger/conversation.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        messages_in = models.PrivateMessage.objects.filter(receiver=self.request.user).filter(sender=self.object)
        messages_out = models.PrivateMessage.objects.filter(receiver=self.object).filter(sender=self.request.user)
        context['messages'] = chain(messages_in, messages_out)
        context['my_profile'] = users.models.UserProfile.objects.get(user=self.request.user)
        context['talker_profile'] = users.models.UserProfile.objects.get(user=self.object)
        return context


class NewMessageView(LoginRequiredMixin, FormView):
    model = models.PrivateMessage
    template_name = 'messenger/new_message.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    form_class = forms.NewMessageForm
    success_url = reverse_lazy('messenger:inbox')

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = form.cleaned_data['receiver']
        form.instance.message_text = form.cleaned_data['message_text']
        form.save()
        return HttpResponseRedirect('/messenger/outbox')


class NewPersonalMessageView(LoginRequiredMixin, FormMixin, DetailView):
    model = get_user_model()
    template_name = 'messenger/new_message.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    form_class = forms.PersonalMessageForm

    def get_success_url(self):
        user = self.object
        return reverse_lazy('messenger:conversation', kwargs={'id': user.id})

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = self.object
        form.save()
        return super().form_valid(form)
