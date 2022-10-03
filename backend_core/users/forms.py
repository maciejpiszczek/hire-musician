from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'minlength': 5,
        'placeholder': 'Enter password'
    }))
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your email',
        'validators': EmailValidator,
    }))

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
    username = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'username',
        'placeholder': 'Username',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
    }))

    class Meta:
        fields = ('username', 'password')
