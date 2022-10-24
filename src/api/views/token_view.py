from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.serializers import *
from packs import Error


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        tags=['account'],
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
        operation_id='Создать access и refresh токены'
    )
    def post(self, request, *args, **kwargs):
        try:
            data = super().post(request, *args, **kwargs)

            data.data['jwtToken'] = data.data.pop('access')
            data.data['refreshToken'] = data.data.pop('refresh')

            return data
        except Exception as e:
            return Error(data={
                            'message': 'Данные некорректны',
                            'exit': False,
                            })


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    @swagger_auto_schema(
        tags=['account'],
        request_body=CustomTokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
        operation_id='Обновить токен'
    )
    def post(self, request, *args, **kwargs):
        try:
            data = super().post(request, *args, **kwargs)

            return data
        except:
            return Error(data={
                'errors': [
                    'Incorrect password.',
                ]
            })
