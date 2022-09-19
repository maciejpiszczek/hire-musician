from django import forms
from django.db import models

from .models import UserProfile
import django_filters


class MusicianFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['instrument', 'music_style', 'is_mobile']
