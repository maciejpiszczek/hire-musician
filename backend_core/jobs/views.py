from django.db.models import Q
from django.views.generic import DetailView
from django_filters.views import FilterView

from . import models

from .filters import JobsFilter


class JobsListView(FilterView):
    model = models.Job
    template_name = 'jobs/jobs_list.html'
    context_object_name = 'jobs'
    filterset_class = JobsFilter
    paginate_by = 20


class JobDetailView(DetailView):
    model = models.Job
    template_name = 'jobs/job_details.html'
    context_object_name = 'job'
