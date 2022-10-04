from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.serializers.user_serializers import UserRegistrationRequestSerializer, UserRegistrationResponseSerializer
from packs import Successful


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
        serializer = UserRegistrationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        serializer.create(validated_data)

        return Successful()
