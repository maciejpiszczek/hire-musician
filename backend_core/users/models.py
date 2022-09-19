from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from django.db import models

from decimal import Decimal

from django.utils.text import slugify


class CustomUser(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='user_avatar')
    bio = models.TextField(default="", blank=True)
    location = models.CharField(default="", blank=True, max_length=100)
    instrument = models.CharField(default="", blank=True, max_length=255)
    music_style = models.CharField(default="", blank=True, max_length=255, verbose_name="musical styles")
    equipment = models.TextField(default="", blank=True)
    is_mobile = models.BooleanField(default=False)
    cut = models.DecimalField(default=Decimal(0), max_digits=6, decimal_places=2)
    rating = models.FloatField(default=0.00)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-rating',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        super().save(*args, **kwargs)
