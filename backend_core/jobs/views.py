from itertools import chain

from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django_filters.views import FilterView

from . import models, forms

from .filters import JobsFilter
from users.models import UserProfile
from .permissions import AuthorManageMixin


class JobsListView(FilterView):
    template_name = 'jobs/jobs_list.html'
    context_object_name = 'jobs'
    filterset_class = JobsFilter
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = list(chain(models.StudioSession.objects.all(), models.Concert.objects.all(),
                                     models.Tour.objects.all()))
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
        if context['job'].owner == self.request.user or self.request.user.is_superuser:
            context['job_owner'] = True
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
