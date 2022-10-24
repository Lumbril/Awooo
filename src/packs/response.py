from rest_framework.response import Response
from rest_framework import status


class Successful(Response):

    def __init__(self, data={'status': 'success'}, status=status.HTTP_200_OK):
        super().__init__(data=data, status=status)


class Error(Response):

    def __init__(self, data={'message': 'Неизвестная ошибка', 'exit': True},
                 status=status.HTTP_400_BAD_REQUEST):
        data['status'] = 'error'
        super().__init__(data=data, status=status)
