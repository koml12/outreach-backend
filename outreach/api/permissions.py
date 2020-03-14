from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

class isOwner_Person(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_staff) or (request.user == obj):
            return True
        if view.action in ['list', 'create']:
            return True
        return False

class isOwner_Registration(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_staff) or (request.user == obj.candidate):
            return True
        if view.action in ['list', 'create']:
            return True
        return False

class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
