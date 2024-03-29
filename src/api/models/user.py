from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        extra_fields.setdefault('is_active', False)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='Номер телефона')
    hide_phone = models.BooleanField(default=True, verbose_name='Скрыть номер')
    date_created = models.DateTimeField(null=True, auto_now_add=True, verbose_name='Дата создания')
    date_edited = models.DateTimeField(null=True, auto_now=True, verbose_name='Изменено')
    date_deleted = models.DateTimeField(null=True, blank=True, verbose_name='Дата удаления')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Code(models.Model):
    class Type(models.TextChoices):
        REGISTRATION = 'REGISTRATION', _('Для регистрации')
        CHANGE_PASSWORD = 'CHANGE_PASSWORD', _('Для смены пароля')

    email = models.EmailField(blank=False, null=False, verbose_name="Почта")
    code = models.CharField(validators=[MinLengthValidator(6)], max_length=6,
                            blank=False, null=False, verbose_name="Код")
    type = models.CharField(max_length=32, null=True, choices=Type.choices, verbose_name='Тип кода')
    number_of_attempts = models.PositiveIntegerField(default=0, verbose_name="Использованные попытки")

    class Meta:
        db_table = 'one-time_codes'
        verbose_name = 'Одноразовый код'
        verbose_name_plural = 'Одноразовые коды'
