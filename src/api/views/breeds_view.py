from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.models import Breed
from api.serializers import FileUploadSerializer, BreedSerializer
from packs import Successful, Error

import pandas as pd


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_id="Получить список пород"))
class UploadFileView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=['breeds'],
        request_body=FileUploadSerializer,
        operation_id='Загрузить файл с породами собак'
    )
    @permission_classes([IsAdminUser])
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
