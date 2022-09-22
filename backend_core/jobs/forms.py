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
        fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
                  'location', 'studio_name')


class CreateConcertForm(CreateJobForm):
    class Meta:
        model = models.Concert
        fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
                  'location', 'venue', 'capacity', 'duration', 'rehearsals', 'includes_transfer')


class CreateTourForm(CreateJobForm):
    class Meta:
        model = models.Tour
        fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
                  'region', 'concert_amount', 'days_off', 'rehearsals')


class JobAccessForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Post', css_class='btn btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = models.JobAccess
        exclude = ('candidate', 'job')

    # def __init__(self, *args, **kwargs):
    #     candidate = kwargs.pop('candidate')
    #     job = kwargs.pop('job')
    #     super(JobAccessForm, self).__init__(*args, **kwargs)
    #     self.fields['candidate'] = candidate
    #     self.fields['job'] = job


