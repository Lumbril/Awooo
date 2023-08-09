import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    async def connect(self):
        self.user_id = f"userId_{self.scope['url_route']['kwargs']['user_id']}"

        await self.channel_layer.group_add(self.user_id, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = "text_data_json['message']"

        await self.channel_layer.group_send(
            self.user_id, {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
