import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message
from channels.exceptions import StopConsumer

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_group_name = 'chat'
            logger.info(f"WebSocket 连接建立: {self.channel_name}")
            
            # 将通道添加到群组
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"WebSocket 连接已接受: {self.channel_name}")
        except Exception as e:
            logger.error(f"WebSocket 连接失败: {str(e)}")
            raise StopConsumer()

    async def disconnect(self, close_code):
        try:
            logger.info(f"WebSocket 连接断开: {self.channel_name}, code: {close_code}")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            logger.error(f"WebSocket 断开连接失败: {str(e)}")

    async def receive(self, text_data):
        try:
            logger.info(f"收到消息: {text_data}")
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
                logger.info(f"消息已广播: {message}")
        except Exception as e:
            logger.error(f"处理消息失败: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': '消息处理失败'
            }))

    async def chat_message(self, event):
        try:
            logger.info(f"发送消息到客户端: {event}")
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'username': event['username'],
                'receiver': event.get('receiver')
            }))
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")

    @database_sync_to_async
    def save_message(self, username, content, receiver_username=None):
        try:
            sender = User.objects.get(username=username)
            receiver = None
            if receiver_username:
                receiver = User.objects.get(username=receiver_username)
            
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                is_private=bool(receiver)
            )
            logger.info(f"消息已保存到数据库: {message}")
            return message
        except Exception as e:
            logger.error(f"保存消息失败: {str(e)}")
            raise 