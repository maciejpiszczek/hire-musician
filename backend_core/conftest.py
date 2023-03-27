import datetime
import random

import pytest
from _decimal import Decimal
from django.contrib.auth.models import Group

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
def create_user_and_job(user):
    user_ = user
    user_.groups.add(Group.objects.get(name='musicians'))
    now_ = datetime.datetime.now(tz=datetime.timezone.utc)
    job = Job.objects.create(
        owner=user_,
        title='Rictusempra',
        instrument='guitar',
        music_style='rock',
        description='loremipsum',
        cut=Decimal(100),
        cut_unit=random.choice(CutUnit.objects.all()),
        event_start=now_ + datetime.timedelta(hours=1),
        event_end=now_ + datetime.timedelta(hours=3),
    )
    return user_, job


@pytest.fixture
def room(db):
    return Room.objects.create(name='test_room')
