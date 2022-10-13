from datetime import datetime, timezone

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.db.models import Q
from chat.models import Message, Room
from users.models import UserProfile
from utils.calculate_timedelta import calculate_timedelta


class ChatIndexView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'chat/index.html'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().exclude(user_id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = super().get_queryset().exclude(user_id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        user_list = []

        for user in queryset:
            user_msgs = Message.objects.filter(sender=get_user_model().objects.get(id=user.id)).order_by('-timestamp')

            chat_tdelta = calculate_timedelta(datetime.now(timezone.utc), user_msgs[0].timestamp) if user_msgs else ''
            user_list.append((user, chat_tdelta))

        context['musicians'] = user_list
        return context


class ChatRoomView(LoginRequiredMixin, DetailView):
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        my_id = self.request.user.id
        other_id = self.kwargs['pk']
        room_name = "_".join((str(my_id), str(other_id))) if my_id < other_id else "_".join((str(other_id), str(my_id)))
        room_in_db = Room.objects.filter(room_name=room_name)
        if not room_in_db:
            room = Room.objects.create(sender=self.request.user,
                                       receiver=get_user_model().objects.get(id=self.kwargs['pk']), room_name=room_name)
        else:
            room = Room.objects.get(room_name=room_name)
        sender = request.user

        if room.receiver == sender:
            receiver = room.sender
        else:
            receiver = room.receiver

        sender_profile = UserProfile.objects.get(user=sender)
        receiver_profile = UserProfile.objects.get(user=receiver)

        messages = Message.objects.filter(Q(sender=self.request.user,
                                            receiver=get_user_model().objects.get(id=self.kwargs['pk']))
                                          | Q(sender=get_user_model().objects.get(id=self.kwargs['pk']),
                                              receiver=self.request.user)).order_by('timestamp')

        return render(request, 'chat/chat.html', {
            'room_name': room_name,
            'sender': sender,
            'sender_name': sender.username,
            'sender_profile': sender_profile,
            'receiver': receiver,
            'receiver_name': receiver.username,
            'receiver_profile': receiver_profile,
            'messages': messages,
        })
