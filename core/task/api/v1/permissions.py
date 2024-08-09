from rest_framework import permissions


class IsVerifiedUser(permissions.BasePermission):
    """
    Custom permission to only allow verified users to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and verified
        return (
            request.user and request.user.is_authenticated and request.user.is_verified
        )
