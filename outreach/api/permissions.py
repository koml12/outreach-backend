from rest_framework import permissions

class isOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_staff) or (request.user == obj):
            return True
        if view.action in ['list', 'create']:
            return True
        return False