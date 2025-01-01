import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        
        if message_type == 'message':
            message = data['message']
            username = data['username']
            receiver = data.get('receiver')
            
            # 保存消息到数据库
            await self.save_message(username, message, receiver)
            
            # 广播消息
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'receiver': receiver
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'receiver': event.get('receiver')
        }))

    @database_sync_to_async
    def save_message(self, username, content, receiver_username=None):
        sender = User.objects.get(username=username)
        receiver = None
        if receiver_username:
            receiver = User.objects.get(username=receiver_username)
        
        Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            is_private=bool(receiver)
        ) 