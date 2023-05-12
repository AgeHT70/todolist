from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS: list = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
