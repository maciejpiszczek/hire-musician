import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.models import UserProfile


@pytest.fixture
def create_user():
    User = get_user_model()
    user = User.objects.create(
        username='michal_w',
        email='mi@w.pl',
        password='zaq12wsx'
    )
    return user


@pytest.fixture
def get_user_profile(create_user):
    user = create_user
    profile = UserProfile.objects.get(user=user)
    return profile


@pytest.mark.django_db
def test_redirect_from_musicians_list_view_if_not_authenticated(client):
    url = reverse('users:musicians_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_musicians_list_view_if_authenticated(client, create_user):
    user = create_user
    client.force_login(user)
    url = reverse('users:musicians_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_redirect_from_musicians_profile_view_if_not_authenticated(client, get_user_profile):
    user_b = get_user_profile
    url = reverse('users:profile_details', kwargs={'slug': user_b.slug})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_musicians_profile_view_if_authenticated(client, create_user, get_user_profile):
    user = create_user
    user_b = get_user_profile
    client.force_login(user)
    url = reverse('users:profile_details', kwargs={'slug': user_b.slug})
    response = client.get(url)
    assert response.status_code == 200
