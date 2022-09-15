from . import models
from django.views.generic import DetailView, ListView


class MusiciansProfilesListView(ListView):
    model = models.UserProfile
    template_name = 'users/users_profiles_list.html'
    context_object_name = 'musicians'


class MusicianProfileView(DetailView):
    model = models.UserProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
