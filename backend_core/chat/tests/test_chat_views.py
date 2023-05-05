import pytest
from django.urls import reverse


@pytest.mark.views
def test_chat_index_view_if_not_authenticated(db, client):
    url = reverse('chat:chat-index')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_chat_index_view_if_authenticated(db, client, user):
    url = reverse('chat:chat-index')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.views
def test_chat_room_view_if_not_authenticated(db, client, user):
    user_ = user
    url = reverse('chat:chat-view', kwargs={'pk': user_.id})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.views
def test_chat_room_view_if_authenticated(db, client, user):
    user_ = user
    url = reverse('chat:chat-view', kwargs={'pk': user_.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
