import pytest
from django.urls import reverse


@pytest.mark.views
def test_redirect_from_jobs_list_view_if_not_authenticated(db, client):
    url = reverse('jobs:jobs_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_jobs_list_view_if_authenticated(db, client, user):
    user_ = user
    client.force_login(user_)
    url = reverse('jobs:jobs_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.views
def test_studio_session_creation_view_if_unauthorized(db, client):
    url = reverse('jobs:new_session')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_concert_creation_view_if_unauthorized(db, client):
    url = reverse('jobs:new_concert')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_tour_creation_view_if_unauthorized(db, client):
    url = reverse('jobs:new_tour')
    response = client.get(url)
    assert response.status_code == 302
