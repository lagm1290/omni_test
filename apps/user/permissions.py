from rest_framework.permissions import BasePermission

class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.has_perm('user.client')
        return False

