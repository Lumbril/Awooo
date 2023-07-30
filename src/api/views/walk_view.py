from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Walk
from api.serializers import WalkDetailSerializer
from packs import Successful, Error


class WalkView(mixins.RetrieveModelMixin,
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
        walk = Walk.objects.select_related('dog__account').filter(id=pk, dog__account=request.user)

        if not walk.exists():
            return Error({'message': 'У вас нет данной прогулки', 'exit': False})

        walk = walk.first()

        serializer = WalkDetailSerializer(walk)

        return Successful(data=serializer.data)
