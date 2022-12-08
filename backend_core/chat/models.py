from django.db import models
from django.contrib.auth import get_user_model


class Room(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey('Room', related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date_added} - FROM {self.user}'
