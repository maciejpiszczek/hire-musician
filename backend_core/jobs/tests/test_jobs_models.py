from datetime import datetime, timezone
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from jobs.models import Job, StudioSession, Concert, Tour


@pytest.fixture
def create_user():
    User = get_user_model()
    user = User.objects.create(
        username='michal_w',
        email='mi@w.pl',
        password='zaq12wsx'
    )
    return user


@pytest.mark.django_db
def test_create_job(create_user):
    job = Job.objects.create(
        owner=create_user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit='hour',
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
    )
    jobs = Job.objects.all()
    assert len(jobs) == 1


@pytest.mark.django_db
def test_create_studio_session(create_user):
    job = StudioSession.objects.create(
        owner=create_user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit='hour',
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
        location='Warsaw',
        studio_name='ABC',
    )
    studio_sessions = StudioSession.objects.all()
    assert len(studio_sessions) == 1


@pytest.mark.django_db
def test_create_concert(create_user):
    job = Concert.objects.create(
        owner=create_user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit='hour',
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
        location='Warsaw',
        venue='ABC',
        capacity=200,
        duration=60,
        rehearsals=False,
        includes_transfer=False
    )
    concerts = Concert.objects.all()
    assert len(concerts) == 1


@pytest.mark.django_db
def test_create_tour(create_user):
    job = Tour.objects.create(
        owner=create_user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit='hour',
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
        region='Europe',
        concert_amount=30,
        days_off=2,
        rehearsals=True
    )
    tours = Tour.objects.all()
    assert len(tours) == 1
