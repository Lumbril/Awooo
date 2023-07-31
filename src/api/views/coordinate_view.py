from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Coordinate, Walk
from api.serializers import CoordinateSerializer, CoordinateCreateSerializer
from packs import Successful, Error


class CoordinateView(mixins.CreateModelMixin,
                     GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CoordinateSerializer
    queryset = Coordinate.objects.all()

    @swagger_auto_schema(
        tags=['coords'],
        request_body=CoordinateCreateSerializer,
        responses={
            status.HTTP_200_OK: CoordinateSerializer
        },
        operation_id='Добавить geo точку к прогулке'
    )
    def create(self, request):
        serializer = CoordinateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Walk.objects.select_related('dog__account') \
                .filter(id=serializer.validated_data['walk'].id, dog__account=request.user,
                        date_deleted__isnull=True).exists():
            return Error(data={'message': 'У вас нет такой прогулки', 'exit': False})

        coordinate = serializer.save()

        return Successful(data=CoordinateSerializer(coordinate).data)
