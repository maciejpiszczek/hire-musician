from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from chat.models import Room, Message


def chat_view(request):
    return render(request, 'chat/chat_view.html')


def room_view(request, room_name):
    return render(request, 'chat/room_view.html', {
        'room_name': room_name
    })


class ChatRoomView(LoginRequiredMixin, View):
    queryset = Room.objects.all()

    def get(self, request, room_name, *args, **kwargs):
        get_object_or_404(Room, room_name=self.kwargs.get('room_name'))
        room = Room.objects.get(room_name=self.kwargs.get('room_name'))
        sender = request.user
        # sender_name = get_user_model().objects.get(id=sender_id).username

        if room.receiver == sender:
            receiver = room.sender
        else:
            receiver = room.receiver

        messages = Message.objects.filter(Q(sender=sender, receiver=receiver)
                                          | Q(sender=receiver, receiver=sender)).order_by('timestamp')

        return render(request, 'chat/room_view.html', {
            'room_name': room_name,
            'sender': sender,
            'sender_name': sender.username,
            'receiver': receiver,
            'receiver_name': receiver.username,
            'messages': messages,
        })
