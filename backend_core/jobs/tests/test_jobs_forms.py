import pytest
from jobs.forms import JobAccessForm


@pytest.mark.forms
def test_apply_for_job(db, client, user, job):
    candidate = user
    job_ = job
    form = JobAccessForm(data={
        'candidate': candidate,
        'job': job_,
    })

    assert form.is_valid() is True
