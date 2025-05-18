from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.user_type == 'admin'

class IsAdminOrReviewer(permissions.BasePermission):
    """
    Custom permission to only allow admins or reviewers to access views.
    """
    def has_permission(self, request, view):
        return request.user and request.user.user_type in ['admin', 'reviewer']

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.user_type in ['admin', 'reviewer']:
            return True
            
        # Instance must have a user attribute that refers to the requesting user
        return obj.user == request.user