import star_ratings.models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_filters.views import FilterView
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from jobs.models import JobAccess, Job
from . import forms
from . import models
from django.views.generic import DetailView, UpdateView

from .filters import MusicianFilter
from .forms import ChangePasswordForm, ResetPasswordForm


class MusiciansProfilesListView(LoginRequiredMixin, FilterView):
    model = models.UserProfile
    template_name = 'list_view.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    context_object_name = 'musicians'
    filterset_class = MusicianFilter
    paginate_by = 20

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
        context['object_list'] = mus_list
        context['no_results_message'] = "There are no agents meeting your criteria."

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

        user_jobs = Job.objects.filter(owner=context['profile'].user)
        user_accesses = JobAccess.objects.filter(candidate=context['profile'].user)
        try:
            context['user_rating'] = star_ratings.models.Rating.objects.get(object_id=context['profile'].id).average
        except ObjectDoesNotExist:
            context['user_rating'] = None

        jobaccess = JobAccess.objects.filter(candidate_id=context['profile'].user.id)
        for a in jobaccess:
            if (a.job.owner == self.request.user) & a.approved:
                context['performed'] = True
                break

        context['jobs'] = [job for job in user_jobs]
        context['events'] = [access.job for access in user_accesses if access.approved]

        return context


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST or None, request.FILES or None)
        return render(request, 'users/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.groups.add(Group.objects.get(name='musicians'))
            return HttpResponseRedirect('/users/login/' + '?Status=' + 'True')


class SignInView(LoginView):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        signup_success = request.GET.get('Status')

        if signup_success == 'True':
            messages.success(request, 'Account succesfully created. You can sign in now.')

        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request, request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
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


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'users/password_change_form.html'


class ChangePasswordDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class ResetPasswordView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = ResetPasswordForm


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
