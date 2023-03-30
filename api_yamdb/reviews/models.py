from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    role = models.CharField(
        choices=USER_ROLES,
        default=USER,
        blank=False,
        max_length=20,
        verbose_name='Роль'
    )
    bio = models.CharField(
        blank=True,
        max_length=1000,
        verbose_name='Биография'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    confirmation_code = models.CharField(
        blank=True,
        max_length=5
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self) -> str:
        return self.username
