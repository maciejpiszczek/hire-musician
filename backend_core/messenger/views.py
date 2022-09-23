from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django_filters.views import FilterView

from . import models, forms
from .filters import PrivMessagesFilter


# class ThreadView(LoginRequiredMixin, DetailView):
#     model = models.PrivateMessage
#     template_name = 'messenger/message_thread.html'
#     login_url = reverse_lazy('users:login')
#     raise_exception = False
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         thread_msgs = models.PrivateMessage.objects.filter(Q(receiver=self.request.user),
#                                                            Q(sender=self.request.user)).order_by('sent')
#         sorted_msgs = sorted(thread_msgs, key=operator.attrgetter('thread_title'))
#         context['msgs'] = sorted_msgs
#         return context


class MessagesListView(LoginRequiredMixin, FilterView):
    model = models.PrivateMessage
    template_name = 'messenger/messages_list.html'
    filterset_class = PrivMessagesFilter
    login_url = reverse_lazy('users:login')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['my_messages'] = models.PrivateMessage.objects.filter(Q(sender=self.request.user) |
        #                                                               Q(receiver=self.request.user))
        context['mes_outbox'] = models.PrivateMessage.objects.filter(sender=self.request.user)
        context['mes_inbox'] = models.PrivateMessage.objects.filter(receiver=self.request.user)

        return context


class NewMessageView(LoginRequiredMixin, FormView):
    model = models.PrivateMessage
    template_name = 'messenger/new_message.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    form_class = forms.NewMessageForm
    success_url = reverse_lazy('messages:list')

    def form_valid(self, form):
        form.instance.thread_title = form.cleaned_data['thread_title']
        form.instance.sender = self.request.user
        form.instance.receiver = form.cleaned_data['receiver']
        form.instance.message_text = form.cleaned_data['message_text']
        form.save()
        return HttpResponseRedirect('/messenger/')

#
# class NewMessageView(LoginRequiredMixin, FormMixin, DetailView):
#     model = models.PrivateMessage
#     template_name = 'messenger/new_message.html'
#     form_class = forms.NewMessageForm
#     login_url = reverse_lazy('users:login')
#     login_url = reverse_lazy('users:login')
#     raise_exception = False
#     success_url = reverse_lazy('messenger:list')
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         form.instance.sender = self.request.user
#         form.instance.receiver = get_user_model.objects.get(id=self.kwargs['receiver_id'])
#         form.save()
#         return HttpResponseRedirect('/messenger/')
