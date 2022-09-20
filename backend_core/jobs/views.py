from itertools import chain

from django.views.generic import DetailView
from django_filters.views import FilterView

from . import models

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
        jobs = list(chain(models.StudioSession.objects.all(), models.Concert.objects.all(),
                                     models.Tour.objects.all()))
        context['job_detailed'] = [job for job in jobs if job.title == context['job'].title][0]
        context['owner_profile'] = UserProfile.objects.get(user_id=context['job'].owner_id)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     # if not models.StudioSession.objects.get(job_ptr_id=context['job'].id):
    #     #     if not models.Concert.objects.get(job_ptr_id=context['job'].id):
    #     #         if not models.Tour.objects.get(job_ptr_id=context['job'].id):
    #     #             raise ValueError('No matching item!')
    #     #         else:
    #     #             context['job_detailed'] = models.Tour.objects.get(job_ptr_id=context['job'].id)
    #     #     else:
    #     #         context['job_detailed'] = models.Concert.objects.get(job_ptr_id=context['job'].id)
    #     # else:
    #     #     context['job_detailed'] = models.StudioSession.objects.get(job_ptr_id=context['job'].id)
    #     if models.StudioSession.objects.get(job_ptr_id=context['job'].id):
    #         context['job_detailed'] = models.StudioSession.objects.get(job_ptr_id=context['job'].id)
    #     elif models.Concert.objects.get(job_ptr_id=context['job'].id):
    #         context['job_detailed'] = models.Concert.objects.get(job_ptr_id=context['job'].id)
    #
    #     return context
