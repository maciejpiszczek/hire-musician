import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_view(client):
    url = reverse('home:home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_view(client):
    url = reverse('home:search')
    response = client.get(url)
    assert response.status_code == 200
