from datetime import datetime, timezone
from decimal import Decimal

import pytest
from ..models import Job, StudioSession, Concert, Tour


@pytest.mark.django_db
def test_create_job():
    jobs_count = Job.objects.count()
    job = Job.objects.create(
        owner='testAdmin',
        title='Test event',
        instrument='drums',
        music_style='jazz',
        description='job description...',
        cut=Decimal(100),
        cut_unit='hour',
        event_start=datetime(2023, 4, 1, 19, 0, 0, tzinfo=timezone.utc),
        event_end=datetime(2023, 4, 1, 21, 0, 0, tzinfo=timezone.utc),
    )
    assert Job.objects.count() - jobs_count == 1
