import datetime
import json
from json import JSONDecodeError

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .handlers import *


class WebSocketConsumer(AsyncWebsocketConsumer):
    event_handlers = {
        'chat': ChatHandler,
    }

    fields = [
        'action',
        'message'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_field = ['destination', 'message']
        self.user_id = None

    async def connect(self):
        if isinstance(self.scope['user'], AnonymousUser):
            return await self.close()

        self.user_id = f'{self.scope["user"].id}'

        await self.channel_layer.group_add(self.user_id, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.user_id, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)

            if not self.check_fields(text_data_json, self.fields):
                await self.channel_layer.group_send(
                    self.user_id, {
                        'type': 'error',
                        'error': 'Wrong format'
                    }
                )
                return

            action = text_data_json['action']
            message = text_data_json['message']

            if not (action in self.event_handlers):
                await self.channel_layer.group_send(
                    self.user_id, {
                        'type': 'error',
                        'error': 'Not supported action type'
                    }
                )
                return

            handler = self.event_handlers[action](self)
            await handler.handle_event(message)
        except JSONDecodeError:
            await self.channel_layer.group_send(
                self.user_id, {
                    'type': 'error',
                    'error': 'Error in body, body must contain json'
                }
            )

    async def get_response(self, event):
        await self.send(text_data=json.dumps(
            {
                'action': event['action'],
                'message': event['message']
            }
        ))

    async def error(self, event):
        await self.send(text_data=json.dumps(
            {
                'error': event['error']
            }
        ))

    @staticmethod
    def check_fields(sub, main):
        for i in main:
            if not (i in sub):
                return False

        return True
