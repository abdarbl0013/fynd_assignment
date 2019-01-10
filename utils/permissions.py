from rest_framework import permissions


class ReadOnlyAuthenticated(permissions.BasePermission):
    """Permission to allow only Read operation to Authenticated user"""

    def has_permission(self, request, view):
        """
        Returns True if user is authenticated and request is one of the safe
        methods
        """

        is_authenticated = request.user.is_authenticated()
        safe_request = request.method in permissions.SAFE_METHODS
        return is_authenticated and safe_request
