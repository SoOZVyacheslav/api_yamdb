from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

USER_ROLES = [
    (ADMIN, 'ADMIN'),
    (MODERATOR, 'MODERATOR'),
    (USER, 'USER'),
]


class User(AbstractUser):
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
