import base64
import json

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from Awooo import settings
from Awooo.settings import DOMAIN_NAME
from api.models import Code
from api.serializers import *
from packs import Successful, Error, EmailSendThread, generate_code


class EmailActivation(View):
    def get(self, request, token):
        payload = json.loads(base64.b64decode(token.encode(errors='strict')))

        user_email = payload['email']
        user_code = payload['code']

        user = UserModel.objects.filter(email=user_email)

        if not user.exists():
            return HttpResponse(content='Пользователь не найден', status=400)

        user = user.first()

        if user.is_active:
            return HttpResponse(content='Пользователь уже активен', status=400)

        code = Code.objects.filter(email=user_email, type=Code.Type.REGISTRATION)

        if not code.exists():
            return HttpResponse(content='Код больше не действителен, запросите новый', status=400)

        code = code.first()

        if code.code != user_code:
            code.number_of_attempts += 1
            code.save()

            if code.number_of_attempts == 5:
                code.delete()

            return HttpResponse(content='Код неверный', status=400)

        user.is_active = True
        user.save()

        return HttpResponse(content='Почта подтверждена, повторите авторизацию в приложении', status=200)


class AccountView(ViewSet):
    @action(detail=False, methods=['post'], url_path='registration')
    @swagger_auto_schema(
        tags=['account'],
        request_body=UserRegistrationRequestSerializer,
        operation_id='Регистрация'
    )
    def registration(self, request):
        user_email = request.data['email']

        if UserModel.objects.filter(email=user_email).exists():
            return Error(data={'message': 'Пользователь с таким email существует',
                               'exit': False, 'exist': True})

        try:
            serializer = UserRegistrationRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.validated_data

            user_code = Code()
            user_code.email = validated_data['email']
            user_code.code = generate_code()
            user_code.type = Code.Type.REGISTRATION
            user_code.save()

            user = serializer.create(validated_data)
            serializer = UserRegistrationResponseSerializer(user, partial=True)

            payload = {
                'email': user_email,
                'code': user_code.code,
            }

            token = base64.b64encode(json.dumps(payload).encode(errors='strict')).decode(errors='strict')

            message = render_to_string('activation_message.html', {
                'code': user_code.code,
                'url': f'https://{DOMAIN_NAME}/activate/{token}',
                'img': f'https://{DOMAIN_NAME}/static/img',
            })

            email_message = EmailMessage(
                'Активация аккаунта в приложении Awooo',
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email_message.content_subtype = 'html'  # тип текста в письме

            EmailSendThread(email_message).start()

            return Successful()
        except:
            error = serializer.errors

            if 'email' in error.keys():
                error = error['email'][0]

                return Error(data={'message': error, 'exit': False})

            return Error()

    @action(detail=False, methods=['post'], url_path='confirm')
    @swagger_auto_schema(
        tags=['account'],
        request_body=ConfirmCodeRequestSerializer,
        responses={
            status.HTTP_200_OK: UserRegistrationResponseSerializer,
        },
        operation_id='Подтверждение аккаунта'
    )
    def confirm(self, request):
        serializer = ConfirmCodeRequestSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Почта введена неверно', 'exit': False})

        validated_data = serializer.validated_data
        email = validated_data['email']
        code_req = validated_data['code']

        user = UserModel.objects.filter(email=email)

        if not user.exists():
            return Error(data={'message': 'Пользователь не найден', 'exit': False})

        user = user.first()

        if user.is_active:
            return Error(data={'message': 'Пользователь уже активен', 'exit': False})

        code = Code.objects.filter(email=email, type=Code.Type.REGISTRATION)

        if not code.exists():
            return Error(data={'message': 'Код больше не действителен, запросите новый', 'exit': False})

        code = code.first()

        if code.code != code_req:
            code.number_of_attempts += 1
            code.save()

            if code.number_of_attempts == 5:
                code.delete()

            return Error(data={'message': 'Код неверный', 'exit': False})

        user.is_active = True
        user.save()
        code.delete()

        serializer = UserRegistrationResponseSerializer(instance=user)

        return Successful(serializer.data)

    @action(detail=False, methods=['post'], url_path='activation_code')
    @swagger_auto_schema(
        tags=['account'],
        request_body=RecoveryRequestCodeSerializer,
        operation_id='Запросить новый код на подтверждение аккаунта'
    )
    def create_new_code(self, request):
        serializer = RecoveryRequestCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            pass
        except:
            return Error(data={'message': 'Почта введена неверно', 'exit': False})

        validated_data = serializer.validated_data
        email = validated_data['email']

        user = UserModel.objects.filter(email=email)

        if not user.exists():
            return Error(data={'message': 'Такого пользователя не существует', 'exit': False})

        user = user.first()

        if user.is_active:
            return Error(data={'message': 'Пользователь уже активен', 'exit': False})

        code = Code.objects.filter(email=email, type=Code.Type.REGISTRATION)

        if code.exists():
            code = code.first()
            code.delete()

        code = Code()
        code.email = email
        code.code = generate_code()
        code.type = Code.Type.REGISTRATION
        code.save()

        payload = {
            'email': user.email,
            'code': code.code,
        }

        token = base64.b64encode(json.dumps(payload).encode(errors='strict')).decode(errors='strict')

        message = render_to_string('activation_message.html', {
            'code': code.code,
            'url': f'https://{DOMAIN_NAME}/activate/{token}',
            'img': f'https://{DOMAIN_NAME}/static/img',
        })

        email_message = EmailMessage(
            'Активация аккаунта в приложении Awooo',
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email_message.content_subtype = 'html'

        EmailSendThread(email_message).start()

        return Successful()


class RecoveryView(ViewSet):
    @action(detail=False, methods=['post'], url_path='recovery')
    @swagger_auto_schema(
        tags=['account'],
        request_body=RecoveryRequestCodeSerializer(),
        operation_id='Запрос на получения кода для восстановления'
    )
    def post(self, request):
        serializer = RecoveryRequestCodeSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Почта введена неверно', 'exit': False})

        validated_data = serializer.validated_data
        email = validated_data['email']

        user = UserModel.objects.filter(email=email)

        if not user.exists():
            return Error(data={'message': 'Пользователь не найден', 'exit': False})

        user = user.first()

        if not user.is_active:
            return Error(data={
                'message': 'На вашу почту выслан код подтверждения. Подтвердите почту по ссылке из '
                           'письма или введите в приложении',
                'confirm': False,
                'exit': False
            })

        user_code = Code.objects.filter(email=email, type=Code.Type.CHANGE_PASSWORD)

        if user_code.exists():
            user_code.delete()

        code = generate_code()

        code_user = Code()
        code_user.email = email
        code_user.code = code
        code_user.type = Code.Type.CHANGE_PASSWORD
        code_user.save()

        email_message = EmailMessage(
            'Смена пароля',
            code,
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        EmailSendThread(email_message).start()

        return Successful()

    @action(detail=False, methods=['post'], url_path='recovery/verify/code')
    @swagger_auto_schema(
        tags=['account'],
        request_body=RecoveryCodeSerializer(),
        operation_id='Запрос на проверку кода'
    )
    def verify_code(self, request):
        serializer = RecoveryCodeSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Почта введена неверно', 'exit': False})

        validated_data = serializer.validated_data
        email = validated_data['email']
        code = validated_data['code']

        user = UserModel.objects.filter(email=email)

        if not user.exists():
            return Error(data={'message': 'Пользователь не найден', 'exit': False})

        user = user.first()

        if not user.is_active:
            return Error(data={
                'message': 'На вашу почту выслан код подтверждения. Подтвердите почту по ссылке из '
                           'письма или введите в приложении',
                'confirm': False,
                'exit': False
            })

        code_user = Code.objects.filter(email=email, type=Code.Type.CHANGE_PASSWORD)

        if not code_user.exists():
            return Error(data={'message': 'Код больше не действителен, запросите новый', 'exit': False})

        code_user = code_user.first()

        if code_user.code != code:
            code_user.number_of_attempts += 1
            code_user.save()

            if code_user.number_of_attempts == 5:
                code_user.delete()

            return Error(data={'message': 'Код неверный', 'exit': False})

        return Successful()

    @action(detail=False, methods=['post'], url_path='recovery/verify')
    @swagger_auto_schema(
        tags=['account'],
        request_body=RecoverySerializer(),
        operation_id='Запрос на смену пароля'
    )
    def verify(self, request):
        serializer = RecoverySerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Почта введена неверно', 'exit': False})

        validated_data = serializer.validated_data
        email = validated_data['email']
        code = validated_data['code']
        password = validated_data['password']

        user = UserModel.objects.filter(email=email)

        if not user.exists():
            return Error(data={'message': 'Пользователь не найден', 'exit': False})

        user = user.first()

        if not user.is_active:
            return Error(data={
                'message': 'На вашу почту выслан код подтверждения. Подтвердите почту по ссылке из '
                           'письма или введите в приложении',
                'confirm': False,
                'exit': False
            })

        code_user = Code.objects.filter(email=email, type=Code.Type.CHANGE_PASSWORD)

        if not code_user.exists():
            return Error(data={'message': 'Код больше не действителен, запросите новый', 'exit': False})

        code_user = code_user.first()

        if code_user.code != code:
            code_user.number_of_attempts += 1
            code_user.save()

            if code_user.number_of_attempts == 5:
                code_user.delete()

            return Error(data={'message': 'Код неверный', 'exit': False})

        user.set_password(password)
        user.save()

        code_user.delete()

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
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        old_pass = validated_data['old_password']
        new_pass = validated_data['new_password']

        try:
            pass
        except Exception as e:
            return Error(data={'message': e, 'exit': False})

        if not user.check_password(old_pass):
            return Error(data={'message': 'Старый пароль введен неправильно', 'exit': False})

        user.set_password(new_pass)
        user.save()

        return Successful()
