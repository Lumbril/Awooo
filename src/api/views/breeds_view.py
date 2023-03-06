from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, mixins
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet

from api.models import Breed
from api.serializers import FileUploadSerializer, BreedSerializer
from packs import Successful, Error

import pandas as pd


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action in ['list', 'retrieve']:
            return obj == request.user
        else:
            return request.user.is_superuser


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_id='Получить список пород'))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_id='Получить породу по id'
                  ))
class UploadFileView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    permission_classes = (IsAdminOrReadOnly, )

    @swagger_auto_schema(
        tags=['breeds'],
        request_body=FileUploadSerializer,
        operation_id='Загрузить файл с породами собак'
    )
    def create(self, request):
        serializer = FileUploadSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Error(data={'message': 'Ошибка', 'exit': False})

        file = serializer.validated_data['file']

        if not file.name.endswith('.xlsx'):
            return Error(data={'message': 'Файл должен быть формата xlsx', 'exit': False})

        breeds_from_file = self.__get_breeds_set(file)

        breeds_from_db = {breed.name for breed in Breed.objects.all()}

        breeds_upd = breeds_from_file - breeds_from_db

        for breed in breeds_upd:
            breed_save = Breed(name=breed)
            breed_save.save()

        return Successful()

    @staticmethod
    def __get_breeds_set(file):
        df = pd.read_excel(file, names=['breeds'], header=None)
        names = set(df.breeds)

        return names
