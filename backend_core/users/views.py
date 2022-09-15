from . import models
from django.views.generic import DetailView


class UserProfileView(DetailView):
    model = models.UserProfile
    template_name = 'users/user_profile.html'
    context_object_name = 'profile'
