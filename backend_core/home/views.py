from itertools import chain

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from chat.models import Message
from jobs.models import Job, StudioSession, Concert, Tour
from users.models import UserProfile
from datetime import datetime, timezone
from utils.calculate_timedelta import calculate_timedelta


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            dt_now = datetime.now(timezone.utc)

            jobs = Job.objects.all()
            if jobs:
                last_job_update = jobs[0].updated
                context['job_tdelta'] = calculate_timedelta(dt_now, last_job_update)
            else:
                context['job_tdelta'] = ''

            users = get_user_model().objects.all()
            if users:
                last_user_update = users.order_by('-date_joined')[0].date_joined
                context['user_tdelta'] = calculate_timedelta(dt_now, last_user_update)
            else:
                context['user_tdelta'] = ''

            msgs = Message.objects.all()
            if msgs:
                last_inbox_msg = msgs.order_by('-date_added')[0].date_added
                context['inbox_tdelta'] = calculate_timedelta(dt_now, last_inbox_msg)
            else:
                context['inbox_tdelta'] = ''

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
