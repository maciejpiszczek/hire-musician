from django.http import request
from django_filters.views import FilterView

from . import models
from django.views.generic import DetailView

from .filters import MusicianFilter


class MusiciansProfilesListView(FilterView):
    model = models.UserProfile
    template_name = 'users/users_profiles_list.html'
    context_object_name = 'musicians'
    filterset_class = MusicianFilter
    paginate_by = 10


class MusicianProfileView(DetailView):
    model = models.UserProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
