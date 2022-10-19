from rest_framework.response import Response
from rest_framework import status


class Successful(Response):

    def __init__(self, data={'successful': True}, status=status.HTTP_200_OK):
        super().__init__(data=data, status=status)


class Error(Response):

    def __init__(self, data={'error': True}, status=status.HTTP_400_BAD_REQUEST):
        super().__init__(data=data, status=status)
