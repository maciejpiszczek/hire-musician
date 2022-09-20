from itertools import chain

from django.views.generic import DetailView
from django_filters.views import FilterView

from . import models

from .filters import JobsFilter


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
