from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'minlength': 5
    }))
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-control',
    }))
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Post', css_class='btn btn-primary'))
    helper.form_method = 'POST'

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        result = get_user_model().objects.filter(email=email)

        if len(result):
            raise ValidationError('Email is not unique!')

        return email

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise ValidationError('Passwords are not matching!')

        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'name': 'username',
        'placeholder': 'Username',
    }))

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')