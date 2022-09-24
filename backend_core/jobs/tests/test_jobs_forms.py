import datetime
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from jobs.forms import JobAccessForm
from jobs.models import Job


@pytest.fixture
def create_user():
    User = get_user_model()
    user = User.objects.create(
        username='michal_w',
        email='mi@w.pl',
        password='zaq12wsx'
    )
    user.groups.add(Group.objects.get(name='musicians'))
    return user


@pytest.fixture
def create_user_and_job(django_user_model):
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
    return user, job


@pytest.mark.django_db
def test_apply_for_job(client, create_user, create_user_and_job):
    candidate = create_user
    job_pack = create_user_and_job
    job = job_pack[1]
    form = JobAccessForm(data={
        'candidate': candidate,
        'job': job,
    })

    assert form.is_valid() is True
