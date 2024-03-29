from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class CutUnit(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cut_unit = CutUnit.objects.filter(name=self.name.lower())

        if not cut_unit:
            self.name = self.name.lower()
            return super().save(*args, **kwargs)

        return cut_unit


class Job(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='job_creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    instrument = models.CharField(max_length=200)
    music_style = models.CharField(max_length=200)
    description = models.TextField()
    cut = models.DecimalField(max_digits=10, decimal_places=2)
    cut_unit = models.ForeignKey('CutUnit', on_delete=models.CASCADE, related_name='jobs')
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.event_start.date()} - {self.event_end.date()} - {self.instrument} - {self.title}'

    def get_class(self):
        return self.__class__.__name__

    def get_matching_subclass_object(self):
        obj = None
        for klass in self.__class__.__subclasses__():
            obj = klass.objects.filter(title=self.title)
            if obj:
                break
        return obj[0]

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
    days_off = models.PositiveIntegerField(default=0)
    rehearsals = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'TOUR - {self.event_start.date()} - {self.event_end.date()} ' \
               f'- {self.title} ({self.concert_amount} concerts)'


class JobAccess(models.Model):
    candidate = models.ForeignKey(get_user_model(), related_name='candidate', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f'{self.candidate} - {self.job.title}'

    def get_job(self):
        return Job.objects.get(id=self.job_id)
