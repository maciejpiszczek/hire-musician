from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from . import models


class CreateStudioSessionForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Post', css_class='btn btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = models.StudioSession
        fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
                  'location', 'studio_name')
