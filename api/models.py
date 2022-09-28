from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class User(AbstractUser):

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
