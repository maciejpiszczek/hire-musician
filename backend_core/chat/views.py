from datetime import datetime, timezone

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from chat.models import Message, Room
from users.models import UserProfile
from utils.calculate_timedelta import calculate_timedelta


class ChatIndexView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'chat/index.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = super().get_queryset().exclude(user_id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        user_list = []

        for user in queryset:
            user_msgs = Message.objects.filter(user=get_user_model().objects.get(id=user.id)).order_by('-date_added')

            chat_tdelta = calculate_timedelta(datetime.now(timezone.utc), user_msgs[0].date_added) if user_msgs else ''
            user_list.append((user, chat_tdelta))

        context['musicians'] = user_list
        return context


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = Room

    def get(self, request, *args, **kwargs):
        receiver_ = get_user_model().objects.get(id=self.kwargs['pk'])
        profile = UserProfile.objects.get(user=receiver_)
        try:
            try:
                room_ = Room.objects.get(slug=('room-' + str(self.kwargs['pk']) + '-' + str(self.request.user.id)))
            except ObjectDoesNotExist:
                room_ = Room.objects.get(slug=('room-' + str(self.request.user.id) + '-' + str(self.kwargs['pk'])))
        except ObjectDoesNotExist:
            room_ = Room.objects.create(name=(str(self.request.user) + '-' + str(receiver_)),
                                        slug=('room-' + str(self.request.user.id) + '-' + str(self.kwargs['pk'])))

        messages = Message.objects.filter(room=room_)
        if messages:
            mes_len = len(messages)
            if mes_len >= 25:
                messages_ = messages.order_by('date_added')[(mes_len - 25):mes_len]
            else:
                messages_ = messages.order_by('date_added')
        else:
            messages_ = None

        return render(request, 'chat/chat.html', {'room': room_, 'messages': messages_, 'receiver': receiver_,
                                                  'profile': profile})
