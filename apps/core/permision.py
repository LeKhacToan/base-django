from rest_framework.permissions import BasePermission
from apps.account.models import User


class IsAdminGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.auth_group_id == User.AuthGroup.ADMIN.value
        )
