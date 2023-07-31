import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Walk, Dog
from api.serializers import WalkDetailSerializer, WalkSerializer, WalkCreateSerializer, WalkPartialUpdateSerializer
from packs import Successful, Error


class WalkView(mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WalkDetailSerializer
    queryset = Walk.objects.all()

    @swagger_auto_schema(
        tags=['walks'],
        responses={
            status.HTTP_200_OK: WalkDetailSerializer,
        },
        operation_id='Получить информацию о прогулке'
    )
    def retrieve(self, request, pk):
        walk = Walk.objects.select_related('dog__account').filter(id=pk, dog__account=request.user,
                                                                  date_deleted__isnull=True)

        if not walk.exists():
            return Error({'message': 'У вас нет данной прогулки', 'exit': False})

        walk = walk.first()

        serializer = WalkDetailSerializer(walk)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['walks'],
        request_body=WalkCreateSerializer,
        responses={
            status.HTTP_200_OK: WalkSerializer,
        },
        operation_id='Начать прогулку'
    )
    def create(self, request):
        serializer = WalkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Dog.objects.filter(id=serializer.validated_data['dog'].id, account=request.user).exists():
            return Error(data={'message': 'У вас нет такой собаки', 'exit': False})

        walk = serializer.save()

        return Successful(data=WalkSerializer(walk).data)

    @swagger_auto_schema(
        tags=['walks'],
        request_body=WalkPartialUpdateSerializer,
        responses={
            status.HTTP_200_OK: WalkSerializer,
        },
        operation_id='Обновить прогулку (завершение)'
    )
    def partial_update(self, request, pk):
        walk = Walk.objects.select_related('dog__account').filter(id=pk, dog__account=request.user,
                                                                  date_deleted__isnull=True)

        if not walk.exists():
            return Error(data={'message': 'У вас нет такой прогулки', 'exit': False})

        walk = walk.first()

        serializer = WalkPartialUpdateSerializer(data=request.data, instance=walk, partial=True)
        serializer.is_valid(raise_exception=True)

        walk = serializer.save()

        return Successful(data=WalkSerializer(walk).data)

    @swagger_auto_schema(
        tags=['walks'],
        responses={
            status.HTTP_200_OK: WalkSerializer,
        },
        operation_id='Удалить прогулку'
    )
    def destroy(self, request, pk):
        walk = Walk.objects.select_related('dog__account').filter(id=pk, dog__account=request.user,
                                                                  date_deleted__isnull=True)

        if not walk.exists():
            return Error(data={'message': 'У вас нет такой прогулки', 'exit': False})

        walk = walk.first()

        walk.date_deleted = datetime.datetime.now()
        walk.save()

        return Successful()
