from django_filters.views import FilterView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import forms
from . import models
from django.views.generic import DetailView

from .filters import MusicianFilter


class MusiciansProfilesListView(FilterView):
    model = models.UserProfile
    template_name = 'users/users_profiles_list.html'
    context_object_name = 'musicians'
    filterset_class = MusicianFilter
    paginate_by = 10


class MusicianProfileView(DetailView):
    model = models.UserProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'


def registration_view(request):
    form = forms.RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_musician = True
            user.save()
            return redirect(reverse_lazy('users:login'))
    return render(request, 'users/registration.html', {'form': form})


def login_user_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse_lazy('home:home'))
    else:
        form = forms.LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('home:home'))
