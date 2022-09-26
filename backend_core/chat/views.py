from django.shortcuts import render


def chat_view(request):
    return render(request, 'chat/chat_view.html')


def room_view(request, room_name):
    return render(request, 'chat/room_view.html', {
        'room_name': room_name
    })
