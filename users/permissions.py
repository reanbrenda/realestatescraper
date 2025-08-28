from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated and is admin
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_admin
        )
    
    def has_object_permission(self, request, view, obj):
        # Check if user is admin for object-level permissions
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_admin
        )
