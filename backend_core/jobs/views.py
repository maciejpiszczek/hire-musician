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
    template_name = 'jobs/jobs_list.html'
    login_url = reverse_lazy('users:login')
    raise_exception = False
    context_object_name = 'jobs'
    filterset_class = JobsFilter
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_results_message'] = "There are no job offers meeting your criteria."
        return context


class MyJobsListView(JobsListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = chain(models.StudioSession.objects.filter(owner_id=self.request.user.id),
                                models.Concert.objects.filter(owner_id=self.request.user.id),
                                models.Tour.objects.filter(owner_id=self.request.user.id))
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
        context['candidates'] = [access.candidate for access in accesses]
        context['access_count'] = len(accesses)
        context['job_owner'] = True if (context['job'].owner == self.request.user or self.request.user.is_superuser) \
            else False
        context['applied'] = True if models.JobAccess.objects.filter(candidate=self.request.user, job=self.object) \
            else False
        return context


class CreateJobView(GroupRequiredMixin, FormView):
    template_name = 'jobs/new_job.html'
    login_url = reverse_lazy('users:login')
    group_required = "musicians"
    raise_exception = False
    success_url = reverse_lazy('jobs:jobs_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
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
    template_name = 'jobs/edit_job.html'
    login_url = reverse_lazy('users:login')
    group_required = 'musicians'
    raise_exception = False
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
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
    template_name = 'jobs/delete_job.html'
    login_url = reverse_lazy('users:login')
    group_required = 'musicians'
    success_url = reverse_lazy('jobs:jobs_list')
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_type'] = self.model.__name__
        return context


class JobAccessView(GroupRequiredMixin, FormMixin, DetailView):
    model = models.Job
    template_name = 'jobs/apply.html'
    form_class = forms.JobAccessForm
    group_required = 'musicians'

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


class MyJobAccessesListView(LoginRequiredMixin, FilterView):
    model = models.JobAccess
    template_name = 'jobs/jobs_list.html'
    context_object_name = 'jobs'
    filterset_fields = ['job']
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accesses'] = models.JobAccess.objects.filter(candidate=self.request.user)
        context['jobs'] = []

        for access in context['accesses']:
            studio = models.StudioSession.objects.filter(job_ptr_id=access.job.id)
            concerts = models.Concert.objects.filter(job_ptr_id=access.job.id)
            tours = models.Tour.objects.filter(job_ptr_id=access.job.id)

            if not context['jobs']:
                context['jobs'] = list(chain(studio, concerts, tours))
            else:
                context['jobs'] += list(chain(studio, concerts, tours))

        context['no_results_message'] = "You have no job accesses."
        return context
