from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import NameChat
from api.serializers.chat_serializer import NameChatResponseSerializer
from packs import Successful, Error


class ChatView(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = NameChat.objects.all()

    @swagger_auto_schema(
        tags=['chat'],
        responses={
            status.HTTP_200_OK: NameChatResponseSerializer
        },
        operation_id='Получить чат пользователя по id'
    )
    def retrieve(self, request, pk):
        chat = NameChat.objects.select_related('chat')\
            .select_related('participant').filter(chat__id=pk, participant__user__id=request.user.id)

        if not chat.exists():
            return Error(data={'message': 'У пользователя нет такого чата', 'exit': False})

        chat = chat.first()

        serializer = NameChatResponseSerializer(chat)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['chat'],
        responses={
            status.HTTP_200_OK: NameChatResponseSerializer
        },
        operation_id='Получить список чатов пользователя'
    )
    def list(self, request):
        chat_list = NameChat.objects.select_related('chat')\
            .select_related('participant').filter(participant__user__id=request.user.id)
        serializer = NameChatResponseSerializer(chat_list, many=True)

        return Successful(data=serializer.data)
