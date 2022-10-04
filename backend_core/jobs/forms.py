from django import forms
from . import models


class CreateJobForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'cols': 23,
    }))


class CreateStudioSessionForm(CreateJobForm):
    class Meta:
        model = models.StudioSession
        exclude = ('owner', 'added', 'updated', 'is_active')


class CreateConcertForm(CreateJobForm):
    class Meta:
        model = models.Concert
        exclude = ('owner', 'added', 'updated', 'is_active')


class CreateTourForm(CreateJobForm):
    class Meta:
        model = models.Tour
        exclude = ('owner', 'added', 'updated', 'is_active')


class JobAccessForm(forms.ModelForm):
    class Meta:
        model = models.JobAccess
        exclude = ('candidate', 'job')
