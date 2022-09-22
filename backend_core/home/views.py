from django.views.generic import TemplateView

import jobs
import users.models


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = users.models.UserProfile.objects.count()
        context['jobs_count'] = jobs.models.Job.objects.count()
        return context