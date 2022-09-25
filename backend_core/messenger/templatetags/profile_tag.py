from users.models import UserProfile

from django import template
register = template.Library()


@register.filter(name='get_user_avatar_url')
def get_user_avatar_url(value):
    if not UserProfile.objects.get(user=value):
        raise ValueError('Profile not found!')
    profile = UserProfile.objects.get(user=value)
    return profile.avatar, profile.avatar.url
