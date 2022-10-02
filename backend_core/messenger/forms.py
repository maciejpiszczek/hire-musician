from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from . import models


class NewMessageForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Send', css_class='btn btn-danger'))
    helper.form_method = 'POST'

    class Meta:
        model = models.PrivateMessage
        fields = ['receiver', 'message_text']


class PersonalMessageForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Send', css_class='btn btn-danger'))
    helper.form_method = 'POST'

    class Meta:
        model = models.PrivateMessage
        exclude = ['receiver']
        fields = ['message_text']
