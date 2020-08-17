"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Permiso si el usuario es propietario de la cuenta."""

    def has_object_permission(self, request, view, obj):
        """Comprueba si usuario y obj son iguales"""
        return request.user == obj
