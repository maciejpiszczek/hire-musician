import random

import pytest
import datetime

from decimal import Decimal

from django.contrib.auth.models import Group

from jobs.forms import JobAccessForm
from jobs.models import Job, CutUnit


cut_units = CutUnit.objects.all()


@pytest.fixture
def create_user_and_job(django_user_model):
    user = django_user_model.objects.create(
        username='albic',
        email='a@a.pl',
        password='zaq12wsx',
    )
    user.groups.add(Group.objects.get(name='musicians'))
    now_ = datetime.datetime.now(tz=datetime.timezone.utc)
    job = Job.objects.create(
        owner=user,
        title='Rictusempra',
        instrument='guitar',
        music_style='rock',
        description='loremipsum',
        cut=Decimal(100),
        cut_unit=random.choice(cut_units),
        event_start=now_ + datetime.timedelta(hours=1),
        event_end=now_ + datetime.timedelta(hours=3),
    )
    return user, job


@pytest.mark.django_db
def test_apply_for_job(client, user, create_user_and_job):
    candidate = user
    job_pack = create_user_and_job
    job = job_pack[1]
    form = JobAccessForm(data={
        'candidate': candidate,
        'job': job,
    })

    assert form.is_valid() is True
