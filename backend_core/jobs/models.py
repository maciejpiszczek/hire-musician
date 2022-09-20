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
        ('hour', 'hour',),
        ('song', 'song'),
        ('concert', 'concert'),
        ('session', 'session'),
    ]
    cut_unit = models.CharField(max_length=200, choices=cut_unit_choices, default=1)
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.event_start.date()} - {self.event_end.date()} - {self.instrument} - {self.title}'

    class Meta:
        ordering = ('-added',)

    def get_class(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.event_start < datetime.now(timezone.utc):
            raise ValidationError("The event date cannot be in the past!")
        if self.event_end < self.event_start:
            raise ValidationError("Invalid date - time travelling is not possible yet :)")
        super().save(*args, **kwargs)


class StudioSession(Job):
    location = models.CharField(max_length=200, default='Remote')
    studio_name = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return f'STUDIO - {self.event_start.date()} {self.event_start.time()} - {self.event_end.date()} ' \
               f'{self.event_end.time()} - {self.instrument} - {self.title}'


class Concert(Job):
    location = models.CharField(max_length=200)
    venue = models.CharField(max_length=200, default='', blank=True)
    capacity = models.PositiveIntegerField(default=0, blank=True)
    duration = models.PositiveIntegerField()
    rehearsals = models.BooleanField(default=False, blank=True)
    includes_transfer = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'CONCERT - {self.event_start.date()} {self.event_start.time()} - {self.instrument} - {self.title}'


class Tour(Job):
    region = models.CharField(max_length=200)
    concert_amount = models.PositiveIntegerField()
    days_off = models.PositiveIntegerField(default=0, blank=True)
    rehearsals = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'TOUR - {self.event_start.date()} - {self.event_end.date()} ' \
               f'- {self.title} ({self.concert_amount} concerts)'
