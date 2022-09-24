import pytest
from django.contrib.auth import get_user_model

from users.forms import RegistrationForm, LoginForm


@pytest.fixture
def create_user(name, mail, passw):
    User = get_user_model()
    user = User.objects.create(
        username=name,
        email=mail,
        password=passw
    )
    return user


@pytest.mark.parametrize(
    'username, email, password, password_confirmation, valid',
    [('albicc', 'a@a.pl', 'zaq12wsx', 'zaq12wsx', True),
     ('', 'a@a.pl', 'zaq12wsx', 'zaq12wsx', False),
     ('albicc', 'a@a.pl', 'zaq12wsx', '', False),
     ('albicc', 'a.pl', 'zaq12wsx', 'zaq12wsx', False),
     ('albicc', 'a@a.pl', 'zax', 'zax', True),
     ])
@pytest.mark.django_db
def test_user_registration_form(username, email, password, password_confirmation, valid):
    form = RegistrationForm(data={
        'username': username,
        'email': email,
        'password': password,
        'password_confirmation': password_confirmation,
        'valid': valid,
    })

    assert form.is_valid() is valid


@pytest.mark.parametrize(
    'username, password, valid',
    [('albicc', 'zaq12wsx', True),
     ('albicc', 'zaq12', False),
     ('albic', 'zaq12wsx', False),
     ])
@pytest.mark.django_db
def test_user_login_form(username, password, valid, django_user_model):
    user = django_user_model.objects.create(username=username, email='p@p.pl', password=password)
    form = LoginForm(data={
        'username': username,
        'password': password,
        'valid': valid,
    })

    assert form.is_valid() is valid
