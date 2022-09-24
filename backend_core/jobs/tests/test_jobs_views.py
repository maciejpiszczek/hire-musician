import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from jobs.views import CreateStudioSessionView, CreateConcertView, CreateTourView


@pytest.mark.django_db
def test_redirect_from_jobs_list_view_if_not_authenticated(client):
    url = reverse('jobs:jobs_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_jobs_list_view_if_authenticated(client, django_user_model):
    user = django_user_model.objects.create(username='peter123', email='p@p.pl', password='zaq12wsx')
    client.force_login(user)
    url = reverse('jobs:jobs_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_studio_session_creation_view_if_unauthorized(client):
    url = reverse('jobs:new_session')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_concert_creation_view_if_unauthorized(client):
    url = reverse('jobs:new_concert')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_tour_creation_view_if_unauthorized(client):
    url = reverse('jobs:new_tour')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_studio_session_creation_view_if_authorized(client, django_user_model):
    user = django_user_model.objects.create(username='peter123', email='p@p.pl', password='zaq12wsx')
    user.groups.add(Group.objects.get(name='musicians'))
    client.force_login(user)
    url = reverse('jobs:new_session')
    response = client.get(url)
    assert response.status_code == 200
