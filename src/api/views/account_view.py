from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from api.serializers import *
from packs import Successful, Error


class AccountView(APIView):

    @swagger_auto_schema(
        tags=['account'],
        request_body=UserRegistrationRequestSerializer,
        responses={
            status.HTTP_200_OK: UserRegistrationResponseSerializer,
        },
        operation_id='Регистрация'
    )
    def post(self, request):
        try:
            serializer = UserRegistrationRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.validated_data
            user = serializer.create(validated_data)

            serializer = UserRegistrationResponseSerializer(user, partial=True)

            return Successful(serializer.data)
        except:
            error = serializer.errors

            if 'email' in error.keys():
                error = error['email'][0]

                if error == 'Значения поля должны быть уникальны.':
                    error = 'Пользователь с таким email существует'

                return Error(data={'message': error, 'exit': False})

            return Error()


class RecoveryView(ViewSet):
    @action(detail=False, methods=['post'], url_path='recovery')
    @swagger_auto_schema(
        tags=['account'],
        request_body=RecoveryRequestCodeSerializer(),
        operation_id='Запрос на получения кода для восстановления'
    )
    def post(self, request):
        return Successful()

    @action(detail=False, methods=['post'], url_path='recovery/verify')
    @swagger_auto_schema(
        tags=['account'],
        request_body=RecoverySerializer(),
        operation_id='Запрос на восстановление'
    )
    def verify(self, request):
        return Successful()


class UserView(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    @swagger_auto_schema(
        tags=['account'],
        operation_id='Информации об аккаунте'
    )
    def me(self, request):
        user = request.user

        return Successful()

    @action(detail=False, methods=['post'], url_path='changePassword')
    @swagger_auto_schema(
        tags=['account'],
        request_body=ChangePasswordSerializer(),
        operation_id='Смена пароля'
    )
    def set_password(self, request):
        return Successful()
