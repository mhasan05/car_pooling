import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message, MessageImage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        sender_id = data['sender']
        image_ids = data.get('image_ids', [])

        await self.save_message(self.room_id, sender_id, message, image_ids)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_id,
                'image_ids': image_ids,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'image_ids': event['image_ids'],
        }))

    @database_sync_to_async
    def save_message(self, room_id, sender_id, message, image_ids):
        room = ChatRoom.objects.get(id=room_id)
        sender = User.objects.get(id=sender_id)
        msg = Message.objects.create(room=room, sender=sender, content=message)

        for image_id in image_ids:
            image = MessageImage.objects.get(id=image_id)
            msg.images.add(image)
        msg.save()
