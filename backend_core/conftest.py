import random
from datetime import timezone, datetime, timedelta

import pytest
from _decimal import Decimal

from chat.models import Room
from jobs.models import Job, CutUnit
from users.models import UserProfile


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='testuser',
        email='t@u.pl',
        password='testPass123'
    )


@pytest.fixture
def get_user_profile(user):
    user_ = user
    profile = UserProfile.objects.get(user=user_)
    return profile


@pytest.fixture
def room(db):
    return Room.objects.create(name='test_room')


@pytest.fixture
def job_datetime():
    return datetime(datetime.now().year + 1, 4, 1, 19, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def job(db, user, job_datetime):
    return Job.objects.create(
        owner=user,
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit=random.choice(CutUnit.objects.all()),
        event_start=job_datetime + timedelta(days=1),
        event_end=job_datetime + timedelta(days=1, hours=2),
    )
