from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class ListUserPermission(permissions.BasePermission):
    """
    permissions for only superusers can make safe method requests
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and not request.user.is_superuser:
            return False
        return True
