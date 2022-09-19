import pytest
from django.contrib.auth import get_user_model
from ..models import UserProfile


@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(username='ala123', password='TestPass123')
    profile = UserProfile.objects.create(user=user)
    users = User.objects.all()
    profiles = UserProfile.objects.all()
    assert (len(users) == 2) & (len(profiles) == 2)
