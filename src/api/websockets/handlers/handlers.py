import datetime

from channels.db import database_sync_to_async


class BaseHandler:
    def __init__(self, consumer):
        self.consumer = consumer

    async def handle_event(self, message):
        raise NotImplementedError

    @staticmethod
    def check_fields(sub, main):
        for i in main:
            if not (i in sub):
                return False

        return True


class ChatHandler(BaseHandler):
    fields = [
        'author_dog',
        'destination',
        'destination_dog',
        'message'
    ]

    def __init__(self, consumer):
        self.consumer = consumer

    async def handle_event(self, message):
        if not self.check_fields(list(message.keys()), self.fields):
            await self.consumer.channel_layer.group_send(
                self.consumer.user_id, {
                    'type': 'error',
                    'error': 'Invalid message for chat'
                }
            )

            return

        author = self.consumer.user_id
        destination = message['destination']
        message['author'] = author
        message['date_created'] = str(datetime.datetime.now())

        await self.consumer.channel_layer.group_send(
            author,
            {
                'type': 'get_response',
                'action': 'chat',
                'message': message
            }
        )
        await self.consumer.channel_layer.group_send(
            destination,
            {
                'type': 'get_response',
                'action': 'chat',
                'message': message
            }
        )


@database_sync_to_async
def smth():
    pass
