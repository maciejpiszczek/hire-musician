import datetime
from decimal import Decimal

import pytest
from django.contrib.auth.models import Group
from django.urls import reverse

from jobs.models import StudioSession, Concert, Tour, Job


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


@pytest.mark.django_db
def test_concert_creation_view_if_authorized(client, django_user_model):
    user = django_user_model.objects.create(username='peter123', email='p@p.pl', password='zaq12wsx')
    user.groups.add(Group.objects.get(name='musicians'))
    client.force_login(user)
    url = reverse('jobs:new_concert')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_tour_creation_view_if_authorized(client, django_user_model):
    user = django_user_model.objects.create(username='peter123', email='p@p.pl', password='zaq12wsx')
    user.groups.add(Group.objects.get(name='musicians'))
    client.force_login(user)
    url = reverse('jobs:new_tour')
    response = client.get(url)
    assert response.status_code == 200


@pytest.fixture
def create_user_and_jobs(django_user_model):
    user = django_user_model.objects.create(
        username='albic',
        email='a@a.pl',
        password='zaq12wsx',
    )
    user.groups.add(Group.objects.get(name='musicians'))
    job = Job.objects.create(
        owner=user,
        title='Rictusempra',
        instrument='guitar',
        music_style='rock',
        description='loremipsum',
        cut=Decimal(100),
        cut_unit='song',
        event_start=datetime.datetime(2022, 12, 1, 18, 0, 0, tzinfo=datetime.timezone.utc),
        event_end=datetime.datetime(2022, 12, 3, 18, 0, 0, tzinfo=datetime.timezone.utc),
    )
    ssession = StudioSession.objects.create(
        owner=user,
        title='Lorem ipsum',
        instrument='guitar',
        music_style='rock',
        description='loremipsum',
        cut=Decimal(100),
        cut_unit='song',
        event_start=datetime.datetime(2022, 12, 1, 18, 0, 0, tzinfo=datetime.timezone.utc),
        event_end=datetime.datetime(2022, 12, 3, 18, 0, 0, tzinfo=datetime.timezone.utc),
        location='Warsaw',
        studio_name='ABC',
    )
    concert = Concert.objects.create(
        owner=user,
        title='Expecto patronum',
        instrument='guitar',
        music_style='rock',
        description='loremipsum',
        cut=Decimal(100),
        cut_unit='song',
        event_start=datetime.datetime(2022, 12, 1, 18, 0, 0, tzinfo=datetime.timezone.utc),
        event_end=datetime.datetime(2022, 12, 3, 18, 0, 0, tzinfo=datetime.timezone.utc),
        location='Warsaw',
        venue='Potok',
        capacity=100,
        duration=60,
    )
    tour = Tour.objects.create(
        owner=user,
        title='Petrificus totalus',
        instrument='guitar',
        music_style='rock',
        description='loremipsum',
        cut=Decimal(100),
        cut_unit='song',
        event_start=datetime.datetime(2022, 12, 1, 18, 0, 0, tzinfo=datetime.timezone.utc),
        event_end=datetime.datetime(2022, 12, 3, 18, 0, 0, tzinfo=datetime.timezone.utc),
        region='Europe',
        concert_amount=100,
        days_off=2
    )
    return user, job, ssession, concert, tour


@pytest.mark.django_db
def test_studio_session_edit_view(client, create_user_and_jobs):
    test_dataset = create_user_and_jobs
    user = test_dataset[0]
    ssession = test_dataset[2]
    client.force_login(user)
    url = reverse('jobs:edit_session', kwargs={'slug': ssession.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_concert_edit_view(client, create_user_and_jobs):
    test_dataset = create_user_and_jobs
    user = test_dataset[0]
    concert = test_dataset[3]
    client.force_login(user)
    url = reverse('jobs:edit_concert', kwargs={'slug': concert.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_tour_edit_view(client, create_user_and_jobs):
    test_dataset = create_user_and_jobs
    user = test_dataset[0]
    tour = test_dataset[4]
    client.force_login(user)
    url = reverse('jobs:edit_tour', kwargs={'slug': tour.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_job_view(client, create_user_and_jobs):
    test_dataset = create_user_and_jobs
    user = test_dataset[0]
    job = test_dataset[1]
    client.force_login(user)
    url = reverse('jobs:delete-job', kwargs={'slug': job.slug})
    response = client.get(url)
    assert response.status_code == 200
