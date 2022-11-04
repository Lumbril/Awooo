from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Dog
from api.serializers import DogSerializer, DogCreateSerializer
from packs import Successful, Error


class DogView(mixins.RetrieveModelMixin,
              mixins.ListModelMixin,
              mixins.CreateModelMixin,
              GenericViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        tags=['dogs'],
        responses={
            status.HTTP_200_OK: DogSerializer,
        },
        operation_id='Получить список собак пользователя'
    )
    def list(self, request):
        dog_list = Dog.objects.filter(account=request.user)

        serializer = DogSerializer(dog_list, many=True)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['dogs'],
        responses={
            status.HTTP_200_OK: DogSerializer,
        },
        operation_id='Получить информацию о собаке'
    )
    def retrieve(self, request, pk):
        dog = Dog.objects.filter(id=pk, account=request.user)

        if not dog.exists():
            return Error(data={'message': 'У пользователя нет такой собаки', 'exit': False})

        dog = dog.first()

        serializer = DogSerializer(dog)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['dogs'],
        request_body=DogCreateSerializer,
        responses={
            status.HTTP_200_OK: DogSerializer,
        },
        operation_id='Создать запись о собаке'
    )
    def create(self, request):
        user = request.user
        serializer = DogCreateSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Неверный формат данных', 'exit': False})

        validated_data = serializer.validated_data

        dog = Dog()
        dog.account = user

        for x in validated_data:
            setattr(dog, x, validated_data.get(x))

        dog.has_avatar = True if dog.avatar else False

        dog.save()

        return Successful(data=DogSerializer(dog).data)
