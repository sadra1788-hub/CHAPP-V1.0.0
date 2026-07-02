# chatapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # اسم اتاق رو از آدرس می‌گیریم
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # به گروه اتاق می‌پیوندیم
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # از گروه اتاق خارج می‌شیم
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # وقتی پیام از طرف کاربر میاد
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', 'ناشناس')

        # پیام رو برای همه اتاق می‌فرستیم
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # وقتی پیام از گروه رسید، برای کاربر می‌فرستیم
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))