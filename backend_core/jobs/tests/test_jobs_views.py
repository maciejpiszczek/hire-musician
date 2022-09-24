import pytest
from django.urls import reverse


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
