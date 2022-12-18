from django.utils import timezone
from itertools import chain

from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from . import models, forms

from .filters import JobsFilter
from users.models import UserProfile
from .permissions import AuthorManageMixin


class JobsListView(LoginRequiredMixin, FilterView):
    model = models.Job
    template_name = 'list_view.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    context_object_name = 'object_list'
    filterset_class = JobsFilter
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = models.Job.objects.all().order_by('event_start')
        context['header'] = 'Job offers'
        context['jobs_view'] = True
        context['filter_type'] = 'Job'
        context['no_results_message'] = "There are no job offers meeting your criteria."

        return context


class MyJobsListView(JobsListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = models.Job.objects.filter(owner=self.request.user).order_by('event_start')
        context['header'] = 'My job offers'
        context['jobs_view'] = True
        context['my_jobs'] = True
        context['no_results_message'] = "You have no active job offers at the moment."
        return context


class JobDetailView(DetailView):
    model = models.Job
    template_name = 'jobs/job_details.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = list(chain(models.StudioSession.objects.all(), models.Concert.objects.all(), models.Tour.objects.all()))
        context['job_detailed'] = [job for job in jobs if job.title == context['job'].title][0]
        context['owner_profile'] = UserProfile.objects.get(user_id=context['job'].owner_id)
        accesses = models.JobAccess.objects.filter(job=context['job'].id)
        context['hired'] = True if accesses.filter(approved=True) else False
        if context['hired']:
            context['hired_agent'] = UserProfile.objects.get(user_id=accesses.get(approved=True).candidate.id)
        context['candidates'] = [access.candidate for access in accesses]
        context['access_count'] = len(accesses)
        context['job_owner'] = True if (context['job'].owner == self.request.user or self.request.user.is_superuser) \
            else False
        context['applied'] = True if models.JobAccess.objects.filter(candidate=self.request.user, job=self.object) \
            else False
        return context


class CreateJobView(GroupRequiredMixin, FormView):
    template_name = 'jobs/job_form.html'
    group_required = 'musicians'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    success_url = reverse_lazy('jobs:jobs_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
        context['is_new'] = True
        context['dt_now'] = timezone.now().strftime("%Y-%m-%d" + "T" + "%H:%M")
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)


class CreateStudioSessionView(CreateJobView):
    model = models.StudioSession
    form_class = forms.CreateStudioSessionForm


class CreateConcertView(CreateJobView):
    model = models.Concert
    form_class = forms.CreateConcertForm


class CreateTourView(CreateJobView):
    model = models.Tour
    form_class = forms.CreateTourForm


class EditJobView(GroupRequiredMixin, AuthorManageMixin, UpdateView):
    template_name = 'jobs/job_form.html'
    login_url = reverse_lazy('users:login')
    group_required = 'musicians'
    raise_exception = False
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
        context['is_new'] = False
        return context

    def get_success_url(self):
        job_slug = self.kwargs['slug']
        return reverse_lazy('jobs:job_details', kwargs={'slug': job_slug})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)


class EditStudioSessionView(EditJobView):
    model = models.StudioSession
    fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
              'location', 'studio_name')


class EditConcertView(EditJobView):
    model = models.Concert
    fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
              'location', 'venue', 'capacity', 'duration', 'rehearsals', 'includes_transfer')


class EditTourView(EditJobView):
    model = models.Tour
    fields = ('title', 'instrument', 'music_style', 'description', 'cut', 'cut_unit', 'event_start', 'event_end',
              'region', 'concert_amount', 'days_off', 'rehearsals')


class JobDeleteView(GroupRequiredMixin, AuthorManageMixin, DeleteView):
    model = models.Job
    template_name = 'jobs/confirm.html'
    login_url = reverse_lazy('users:login')
    group_required = 'musicians'
    success_url = reverse_lazy('jobs:jobs_list')
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
        context['activity'] = f'delete {self.object.title}'
        context['url_route'] = f'/jobs/delete/{self.object.slug}/'
        return context


class JobAccessView(LoginRequiredMixin, FormMixin, DetailView):
    model = models.Job
    template_name = 'jobs/confirm.html'
    form_class = forms.JobAccessForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        form.instance.job = self.object
        form.save()
        return HttpResponseRedirect('/jobs/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
        context['activity'] = f'apply for {self.object.title}'
        context['url_route'] = f'/jobs/apply/{self.object.slug}/'
        return context


class MyJobAccessesListView(JobsListView):
    template_name = 'list_view.html'
    filterset_class = JobsFilter
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accesses'] = models.JobAccess.objects.filter(candidate=self.request.user)
        jobs = []
        for access in context['accesses']:
            jobs.append(models.Job.objects.get(id=access.job_id))
        context['object_list'] = jobs
        context['header'] = 'My job accesses'
        context['my_jobs'] = True
        context['jobs_view'] = True
        context['no_results_message'] = "You have no job accesses."
        return context
