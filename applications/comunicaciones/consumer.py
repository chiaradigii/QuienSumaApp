# applications/comunicaciones/consumer.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"chat_room_{self.scope['url_route']['kwargs']['chat_id']}"
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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        if message:
            user = self.scope['user'].user
            chat_session = await self.get_chat_session(self.scope['url_route']['kwargs']['chat_id'])

            if not chat_session:
                print("Chat session not found.")
                return

            recipient = chat_session.user1 if chat_session.user2 == user else chat_session.user2
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'chat_message', 'message': message, 'user': user}
            )

            await self.create_and_send_notification(recipient, user, message)

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],  
            'time': event.get('time', ''),  
        }))

    @database_sync_to_async
    def get_chat_session(self,chat_id):
        from applications.comunicaciones.models import ChatSession
        return ChatSession.objects.select_related('user1', 'user2').get(id=chat_id)
    
    @database_sync_to_async
    def create_and_send_notification(self, recipient, user, message):
        notification_message = f"{user} sent you a message: {message}"
        from applications.comunicaciones.models import create_notification
        create_notification(recipient, notification_message)