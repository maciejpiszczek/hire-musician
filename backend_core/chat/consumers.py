import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, sender, room_name, message):
        sender = get_user_model().objects.get(id=self.scope['user'].id)
        room = Room.objects.get(room_name=room_name)

        if self.scope['user'].id == room.receiver_id:
            receiver = get_user_model().objects.get(id=room.sender_id)
        else:
            receiver = get_user_model().objects.get(id=room.receiver_id)

        new_message = Message.objects.create(message=message,
                                             sender=sender, receiver=receiver)
        new_message.save()
        return new_message

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        sender = self.scope['user']
        room_name = self.scope['url_route']['kwargs']['room_name']
        message = event['message']

        await self.save_message(sender, room_name, message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender.username,
            'message': message,
        }))
