from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django import forms
from django.urls import reverse

from . import models


class NewMessageForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Send', css_class='btn btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = models.PrivateMessage
        fields = ['receiver', 'thread_title', 'message_text']
