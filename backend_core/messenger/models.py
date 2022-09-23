from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


# class Thread(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True, blank=True)
#     started = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)


class PrivateMessage(models.Model):
    # thread = models.ForeignKey('Thread', related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(get_user_model(), related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='receiver', on_delete=models.CASCADE)
    message_text = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sent} - {self.sender} TO {self.receiver}'

    class Meta:
        ordering = ('sent',)
