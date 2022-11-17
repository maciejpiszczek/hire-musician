from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sender', on_delete=models.SET(AnonymousUser.id))
    receiver = models.ForeignKey(get_user_model(), related_name='receiver', on_delete=models.SET(AnonymousUser.id))
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp} - FROM {self.sender} TO {self.receiver}'


class Room(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='room_sender', on_delete=models.SET(AnonymousUser.id))
    receiver = models.ForeignKey(get_user_model(), related_name='room_receiver', on_delete=models.SET(AnonymousUser.id))
    room_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.room_name
