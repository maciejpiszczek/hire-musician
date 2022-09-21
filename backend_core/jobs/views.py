from itertools import chain

from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView
from django_filters.views import FilterView

from . import models, forms

from .filters import JobsFilter
from users.models import UserProfile


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


class CreateStudioSessionView(GroupRequiredMixin, FormView):
    model = models.StudioSession
    form_class = forms.CreateStudioSessionForm
    template_name = 'jobs/create_studio_session.html'
    login_url = reverse_lazy('users:login')
    group_required = "musicians"
    raise_exception = False
    success_url = reverse_lazy('jobs:jobs_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
