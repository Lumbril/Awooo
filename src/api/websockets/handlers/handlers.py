from channels.db import database_sync_to_async

from api.models import Chat, Dog, Participant, Message, User


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
        'chat_id',
        'message',
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
        chat_id = message['chat_id']
        access, author_participant = await check_access(chat_id, int(author))

        if not access:
            await self.consumer.channel_layer.group_send(
                self.consumer.user_id, {
                    'type': 'error',
                    'error': 'Access denied for this chat'
                }
            )

            return

        message = await save_message(chat_id, author_participant, message['message'])
        message = await get_json_from_message(message)
        recipients = [str(participant.user_id)
                      for participant in (await get_participants_in_chat(chat_id))]

        for recipient in recipients:
            await self.consumer.channel_layer.group_send(
                recipient, {
                    'type': 'get_response',
                    'action': 'chat',
                    'message': message
                }
            )


@database_sync_to_async
def check_access(chat_id, user_id):
    participant = Participant.objects.filter(chat_participants__id=chat_id, user__id=user_id)

    if not participant.exists():
        return False, None

    participant = participant.first()

    if Dog.objects.filter(id=participant.dog_id, account__id=participant.user_id).exists():
        return True, participant
    else:
        return False, None


@database_sync_to_async
def save_message(chat_id, author_participant, message_text):
    message = Message()
    message.chat = Chat.objects.get(id=chat_id)
    message.author = author_participant
    message.message = message_text
    message.state = Message.Type.SENT

    Message.save(message)

    return message


@database_sync_to_async
def get_participants_in_chat(chat_id):
    return list(Participant.objects.filter(chat_participants__id=chat_id))


@database_sync_to_async
def get_json_from_message(message):
    participant = Participant.objects.get(chat_participants__id=message.chat_id,
                                          user__id=message.author_id)

    dog = Dog.objects.select_related('account')\
        .get(id=participant.dog.id, account_id=message.author_id)

    return {
        'chat_id': message.chat.id,
        'author': {
            "id": dog.account.id,
            "name": dog.owner
        },
        'message': message.message,
        'state': message.state,
        'date_created': str(message.date_created)
    }
