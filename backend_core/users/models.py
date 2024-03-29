from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from decimal import Decimal


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must provide the email.')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.is_active = True

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email=email, username=username, password=password)

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    is_musician = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    objects = CustomUserManager()


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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        super().save(*args, **kwargs)
