import random

import pytest

from datetime import datetime, timezone, timedelta
from decimal import Decimal

from jobs.models import Job, StudioSession, Concert, Tour, CutUnit


cut_units = CutUnit.objects.all()


@pytest.mark.django_db
def test_create_job(user, job_datetime):
    job = Job.objects.create(
        owner=user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit=random.choice(cut_units),
        event_start=job_datetime + timedelta(days=1),
        event_end=job_datetime + timedelta(days=1, hours=2),
    )
    jobs = Job.objects.all()
    assert len(jobs) == 1


@pytest.mark.django_db
def test_create_studio_session(user):
    job = StudioSession.objects.create(
        owner=user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit=random.choice(cut_units),
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
        location='Warsaw',
        studio_name='ABC',
    )
    studio_sessions = StudioSession.objects.all()
    assert len(studio_sessions) == 1


@pytest.mark.django_db
def test_create_concert(user):
    job = Concert.objects.create(
        owner=user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit=random.choice(cut_units),
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
def test_create_tour(user):
    job = Tour.objects.create(
        owner=user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit=random.choice(cut_units),
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
        region='Europe',
        concert_amount=30,
        days_off=2,
        rehearsals=True
    )
    tours = Tour.objects.all()
    assert len(tours) == 1
