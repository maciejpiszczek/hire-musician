import pytest
from jobs.models import Job, StudioSession, Concert, Tour, CutUnit


cut_units = CutUnit.objects.all()


@pytest.mark.django_db
def test_create_job(job):
    job_ = job
    assert len(Job.objects.all()) == 1


@pytest.mark.django_db
def test_create_studio_session(user, job):
    job_ = job
    StudioSession.objects.create(
        owner=user,
        title=job_.title,
        slug=job_.title + "_studio_session",
        instrument=job_.instrument,
        music_style=job_.music_style,
        description=job_.description,
        cut=job_.cut,
        cut_unit=job_.cut_unit,
        event_start=job_.event_start,
        event_end=job_.event_end,
        location='Warsaw',
        studio_name='ABC',
    )
    assert len(StudioSession.objects.all()) == 1


@pytest.mark.django_db
def test_create_concert(job):
    job_ = job
    Concert.objects.create(
        owner=job_.owner,
        title=job_.title,
        slug=job_.title + "_concert",
        instrument=job_.instrument,
        music_style=job_.music_style,
        description=job_.description,
        cut=job_.cut,
        cut_unit=job_.cut_unit,
        event_start=job_.event_start,
        event_end=job_.event_end,
        location='Warsaw',
        venue='ABC',
        capacity=200,
        duration=60,
        rehearsals=False,
        includes_transfer=False
    )
    assert len(Concert.objects.all()) == 1


@pytest.mark.django_db
def test_create_tour(job):
    job_ = job
    Tour.objects.create(
        owner=job_.owner,
        title=job_.title,
        slug=job_.title + "_tour",
        instrument=job_.instrument,
        music_style=job_.music_style,
        description=job_.description,
        cut=job_.cut,
        cut_unit=job_.cut_unit,
        event_start=job_.event_start,
        event_end=job_.event_end,
        region='Europe',
        concert_amount=30,
        days_off=2,
        rehearsals=True
    )
    assert len(Tour.objects.all()) == 1
