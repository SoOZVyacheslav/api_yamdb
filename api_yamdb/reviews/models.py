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


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='Категория')
