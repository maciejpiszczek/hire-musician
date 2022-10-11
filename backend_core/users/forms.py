from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


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


class ChangePasswordForm(PasswordChangeForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _(
            'Your old password was entered incorrectly. Please enter it again.'
        ),
    }
    old_password = forms.CharField(
        label=_('Old password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password',
                   'autofocus': True,
                   'placeholder': 'Current password...'}),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'New password...'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Confirm new password...'}),
    )
