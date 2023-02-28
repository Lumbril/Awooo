from io import StringIO

from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers, mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from api.models import Breed
from api.serializers import FileUploadSerializer
from packs import Successful, Error

import pandas as pd
import xlrd


class UploadFileView(mixins.CreateModelMixin,
                     GenericViewSet):
    serializer_class = FileUploadSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(
        tags=['admin'],
        operation_id='Загрузить файл с породами собак'
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)

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
