import pytest
from django.urls import reverse


@pytest.mark.views
def test_redirect_from_musicians_list_view_if_not_authenticated(db, client):
    url = reverse('users:musicians_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_musicians_list_view_if_authenticated(db, client, user):
    user_ = user
    client.force_login(user)
    url = reverse('users:musicians_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.views
def test_redirect_from_musicians_profile_view_if_not_authenticated(db, client, get_user_profile):
    user_b = get_user_profile
    url = reverse('users:profile_details', kwargs={'slug': user_b.slug})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_musicians_profile_view_if_authenticated(db, client, user, get_user_profile):
    user_ = user
    user_b = get_user_profile
    client.force_login(user)
    url = reverse('users:profile_details', kwargs={'slug': user_b.slug})
    response = client.get(url)
    assert response.status_code == 200
