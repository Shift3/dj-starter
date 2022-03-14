from rest_framework import permissions
from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == User.ADMIN


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
