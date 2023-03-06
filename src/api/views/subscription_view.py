from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Subscription, User
from api.serializers import SubscriptionSerializer, SubscriptionCreateSerializer, MySubscriptionSerializer
from packs import Error, Successful


class SubscriberView(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    @swagger_auto_schema(
        tags=['subscriber'],
        responses={
            status.HTTP_200_OK: SubscriptionSerializer,
        },
        operation_id='Получить подписчика по id'
    )
    def retrieve(self, request, pk):
        sub = Subscription.objects.filter(user=pk, subscription=request.user)

        if not sub.exists():
            return Error(data={'message': 'У пользователя нет такого подписчика', 'exit': False})

        sub = sub.first()
        serializer = SubscriptionSerializer(sub)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['subscriber'],
        responses={
            status.HTTP_200_OK: SubscriptionSerializer,
        },
        operation_id='Получить список подписчиков'
    )
    def list(self, request):
        sub_list = Subscription.objects.filter(subscription=request.user)

        serializer = SubscriptionSerializer(sub_list, many=True)

        return Successful(data=serializer.data)


class SubscriptionView(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MySubscriptionSerializer
    queryset = Subscription.objects.all()

    @swagger_auto_schema(
        tags=['subscription'],
        responses={
            status.HTTP_200_OK: MySubscriptionSerializer,
        },
        operation_id='Получить список на кого подписан'
    )
    def list(self, request):
        my_sub = Subscription.objects.filter(user=request.user)
        serializer = MySubscriptionSerializer(my_sub, many=True)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['subscription'],
        responses={
            status.HTTP_200_OK: MySubscriptionSerializer,
        },
        operation_id='Получить на кого подписан по id'
    )
    def retrieve(self, request, pk):
        my_sub = Subscription.objects.filter(user=request.user, subscription=pk)

        if not my_sub.exists():
            return Error(data={'message': 'Вы не подписаны на этого пользователя', 'exit': False})

        my_sub = my_sub.first()
        serializer = MySubscriptionSerializer(my_sub)

        return Successful(data=serializer.data)

    @swagger_auto_schema(
        tags=['subscription'],
        request_body=SubscriptionCreateSerializer,
        responses={
            status.HTTP_200_OK: MySubscriptionSerializer,
        },
        operation_id='Создать подписку'
    )
    def create(self, request):
        serializer = SubscriptionCreateSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Неверные данные', 'exit': False})

        sub_id = serializer.data['subscription']

        if sub_id == request.user.id:
            return Error(data={'message': 'Нельзя подписаться на самого себя', 'exit': False})

        sub_user = User.objects.filter(id=sub_id)

        if not sub_user.exists():
            return Error(data={'message': 'Пользователя с таким id не существует', 'exit': False})

        sub_user = sub_user.first()

        if Subscription.objects.filter(user=request.user, subscription=sub_user).exists():
            return Error(data={'message': 'Вы уже подписаны на этого пользователя', 'exit': False})

        subscription = Subscription()
        subscription.user = request.user
        subscription.subscription = sub_user
        subscription.save()

        return Successful(data=MySubscriptionSerializer(subscription).data)
