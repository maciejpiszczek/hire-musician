import pytest

from chat.models import Room, Message


@pytest.mark.models
def test_create_room(db):
    Room.objects.create(name='abc')
    assert len(Room.objects.all()) == 1


@pytest.mark.models
def test_create_message(db, room, user):
    Message.objects.create(
        room=room,
        user=user,
        message='Lorem ipsum',
    )
    assert len(Message.objects.all()) == 1
