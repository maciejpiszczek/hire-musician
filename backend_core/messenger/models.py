from django.contrib.auth import get_user_model
from django.db import models


class PrivateMessage(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='receiver', on_delete=models.CASCADE)
    message_text = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sent} - FROM {self.sender} TO {self.receiver}'

    class Meta:
        ordering = ('sent',)
