from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    """Permission to allow only Read operation"""

    def has_permission(self, request, view):
        """Returns True if request is one of the safe methods"""

        return request.method in permissions.SAFE_METHODS
