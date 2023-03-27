from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    message="Only admin has access to this page...."
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser==1:
                return True
        return False

