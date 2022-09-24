import star_ratings.models
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . import forms
from . import models
from django.views.generic import DetailView, UpdateView

from .filters import MusicianFilter


class MusiciansProfilesListView(LoginRequiredMixin, FilterView):
    model = models.UserProfile
    template_name = 'users/users_profiles_list.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    context_object_name = 'musicians'
    filterset_class = MusicianFilter
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mus_list = []
        for musician in context['musicians']:
            mus_user = models.UserProfile.objects.get(slug=musician.slug)
            if not star_ratings.models.Rating.objects.filter(object_id=mus_user.id):
                mus_rating = None
            else:
                mus_rate = star_ratings.models.Rating.objects.get(object_id=mus_user.id)
                mus_rating = mus_rate.average
            mus_list.append((musician, mus_rating))
        context['mus_list'] = mus_list

        return context


class MusicianProfileView(LoginRequiredMixin, DetailView):
    model = models.UserProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
    login_url = reverse_lazy('users:login')
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context['profile'].user == self.request.user:
            context['profile_edit'] = 1
        elif self.request.user.is_superuser:
            context['profile_edit'] = 2
        else:
            context['profile_edit'] = 0

        return context


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


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = models.UserProfile
    fields = ('avatar', 'bio', 'instrument', 'music_style', 'equipment', 'is_mobile', 'cut', 'location')
    template_name = 'users/edit_profile.html'
    login_url = reverse_lazy('home:home')
    raise_exception = False
    context_object_name = 'profile'

    def get_success_url(self):
        profile_slug = self.kwargs['slug']
        return reverse_lazy('users:profile_details', kwargs={'slug': profile_slug})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)
