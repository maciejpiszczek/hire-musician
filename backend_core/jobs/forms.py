from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from . import models


# class CreateJobForm(forms.ModelForm):
#     helper = FormHelper()
#     helper.add_input(Submit('submit', 'Post', css_class='btn btn-danger'))
#     helper.form_method = 'POST'


# class CreateStudioSessionForm(CreateJobForm):
#     class Meta:
#         model = models.StudioSession
#         exclude = ('owner', 'added', 'updated', 'is_active')
#
#
# class CreateConcertForm(CreateJobForm):
#     class Meta:
#         model = models.Concert
#         exclude = ('owner', 'added', 'updated', 'is_active')
#
#
# class CreateTourForm(CreateJobForm):
#     class Meta:
#         model = models.Tour
#         exclude = ('owner', 'added', 'updated', 'is_active')
#
#
# class JobAccessForm(CreateJobForm):
#     class Meta:
#         model = models.JobAccess
#         exclude = ('candidate', 'job')


class CreateStudioSessionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 2,
    }))

    class Meta:
        model = models.StudioSession
        exclude = ('owner', 'added', 'updated', 'is_active')


class CreateConcertForm(forms.ModelForm):
    class Meta:
        model = models.Concert
        exclude = ('owner', 'added', 'updated', 'is_active')


class CreateTourForm(forms.ModelForm):
    class Meta:
        model = models.Tour
        exclude = ('owner', 'added', 'updated', 'is_active')


class JobAccessForm(forms.ModelForm):
    class Meta:
        model = models.JobAccess
        exclude = ('candidate', 'job')
