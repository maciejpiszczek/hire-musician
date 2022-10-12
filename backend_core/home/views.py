from itertools import chain

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_filters.views import FilterView
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin

from jobs.models import Job, StudioSession, Concert, Tour
from users.models import UserProfile


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = len(UserProfile.objects.all())
        context['jobs_count'] = len(Job.objects.all())
        return context


def search(request):
    if 'query' in request.GET and request.GET['query']:
        query = request.GET['query']
        musicians = UserProfile.objects.filter(slug__icontains=query)
        studio_sessions = StudioSession.objects.filter(Q(title__icontains=query) | Q(music_style__icontains=query))
        concerts = Concert.objects.filter(Q(title__icontains=query) | Q(music_style__icontains=query))
        tours = Tour.objects.filter(Q(title__icontains=query) | Q(music_style__icontains=query))
        jobs = chain(studio_sessions, concerts, tours)
        no_results = True if len(list(chain(musicians, studio_sessions, concerts, tours))) == 0 else False

        return render(request, 'jobs/search_results.html', {'query': query, 'no_results': no_results,
                                                            'musicians': musicians, 'jobs': jobs})

    else:
        return render(request, 'jobs/search_results.html')


# class SearchView(MultipleObjectMixin, View):
#     paginate_by = 20
#
#     def get(self, request, *args, **kwargs):
#         if 'query' in request.GET and request.GET['query']:
#             query = request.GET['query']
#             musicians = UserProfile.objects.filter(slug__icontains=query)
#             studio_sessions = StudioSession.objects.filter(Q(title__icontains=query) | Q(music_style__icontains=query))
#             concerts = Concert.objects.filter(Q(title__icontains=query) | Q(music_style__icontains=query))
#             tours = Tour.objects.filter(Q(title__icontains=query) | Q(music_style__icontains=query))
#             jobs = chain(studio_sessions, concerts, tours)
#             no_results = True if len(list(chain(musicians, studio_sessions, concerts, tours))) == 0 else False
#
#             return render(request, 'jobs/search_results.html', {'query': query, 'no_results': no_results,
#                                                                 'musicians': musicians,
#                                                                 'studio_sessions': studio_sessions,
#                                                                 'concerts': concerts, 'tours': tours, 'jobs': jobs,
#                                                                 'paginate_by': self.paginate_by})
#         else:
#             return render(request, 'jobs/search_results.html')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         page_size = 20
#         return super().get_context_data()
