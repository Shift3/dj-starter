from rest_framework import permissions
from .models import User


def IsAnyRole(role_list):
    class PermissionClass(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                return False
            return request.user.role in role_list

    return PermissionClass


IsAdmin = IsAnyRole([User.ADMIN])


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Only designed to be used on a `User` object
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == User.ADMIN:
            return True
        if obj == request.user:
            return True

        return False
