from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminOnly(permissions.BasePermission):
    """Класс для доступа к изменению контента.
    Права имеют только администраторы."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.role == 'admin')


class AdminUserOrReadOnly(permissions.BasePermission):
    """Класс для доступа к изменению контента.
    Права имеют только администраторы, и авторизованые пользователи,
    читать контент могут все."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin'
                    or request.user.is_superuser)))


class AdminModeratorAuthorOnly(permissions.BasePermission):
    """Класс для доступа к изменению контента.
    Права имеют только администраторы, модераторы и авторы."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or obj.author == request.user)
