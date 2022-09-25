from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from . import models


class CreateJobForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Post', css_class='btn btn-primary'))
    helper.form_method = 'POST'


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


class JobAccessForm(CreateJobForm):
    class Meta:
        model = models.JobAccess
        exclude = ('candidate', 'job')
