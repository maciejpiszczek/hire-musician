import pytest

from jobs.forms import JobAccessForm


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
