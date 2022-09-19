from .models import *
from random import randint as rn
from random import choice, sample

data_gen = {
    'nicknames': [
        'ala12', 'daria666', 'alan_wake', 'maciupa', 'chris55', 'albin2', 'peter_ev', 'alonso', 'defil3', 'mati_m',
        'jarek_k', 'zbigniew_z', 'igor89', 'malek23', 'ryan_s', 'albert9', 'catnpies', 'xylo', 'mazur5', 'eluwa4',
        'protazy', 'jankiel5', 'marun321', 'arek', 'marcin3', 'fred', 'miszun22', 'ananiasz', 'gamael', 'ezechiel',
        'stu_mck'
    ],
    'instruments': ['guitar', 'keyboard', 'drums', 'saxophone', 'violin', 'vocals', 'trombone'],
    'styles': ['rock', 'metal', 'jazz', 'blues', 'country', 'pop', 'funk', 'disco', 'R&B', 'soul', 'classical']
}


for nick in data_gen['nicknames']:
    musician = CustomUser.objects.create_user(username=nick, password='TestPass123')
    musician.save()
    musician_profile = UserProfile.objects.get(user_id=CustomUser.objects.get(username=nick).id)

    musician_instruments = sample(data_gen['instruments'], rn(1, 3))
    musician_styles = sample(data_gen['styles'], rn(1, 4))

    musician_profile.instrument = ', '.join(musician_instruments)
    musician_profile.music_style = ', '.join(musician_styles)
    musician_profile.is_mobile = choice([True, False])
    musician_profile.rating = rn(300, 490) / 100
    musician_profile.cut = rn(100, 400)

    musician_profile.save()
