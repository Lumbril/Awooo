from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, GenericViewSet

from api.models import Dog
from api.serializers import DogSerializer
from packs import Successful, Error


class DogView(mixins.RetrieveModelMixin,
              mixins.ListModelMixin,
              GenericViewSet):
    permission_classes = [IsAuthenticated]

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
