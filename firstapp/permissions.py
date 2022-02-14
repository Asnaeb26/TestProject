from rest_framework.permissions import BasePermission


class IsAuthenticatedAndAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method == 'PUT':
            return bool(request.user and request.user.is_staff)
        else:
            return bool(request.user and request.user.is_authenticated)
