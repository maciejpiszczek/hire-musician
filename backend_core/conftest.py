import pytest

from users.models import UserProfile


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='testuser',
        email='t@u.pl',
        password='testPass123'
    )


@pytest.fixture
def get_user_profile(user):
    user_ = user
    profile = UserProfile.objects.get(user=user_)
    return profile
