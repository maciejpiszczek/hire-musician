from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Job(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='job_creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    instrument = models.CharField(max_length=200)
    music_style = models.CharField(max_length=200)
    description = models.TextField()
    cut = models.DecimalField(max_digits=10, decimal_places=2)
    cut_unit_choices = [
        (1, 'hour'),
        (2, 'song'),
        (3, 'concert'),
        (4, 'session'),
    ]
    cut_unit = models.CharField(max_length=200, choices=cut_unit_choices, default=1)
    event_start = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.event_start} - {self.instrument} - {self.title}'

    class Meta:
        ordering = ('-added',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.event_start < datetime.now(timezone.utc):
            raise ValidationError("The event date cannot be in the past!")
        super().save(*args, **kwargs)


class StudioSession(Job):
    location = models.CharField(max_length=200, default='Remote')
    studio_name = models.CharField(max_length=200, default='', blank=True)
