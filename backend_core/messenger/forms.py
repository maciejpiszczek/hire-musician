from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from . import models


class NewMessageForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Send', css_class='btn btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = models.PrivateMessage
        fields = ['receiver', 'message_text']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'},
                                     choices=((user for user in get_user_model().objects.all())))
        }
