from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    """
    Allows access only to authenticated authors.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Author')


class IsRedactor(permissions.BasePermission):
    """
    Allows access only to authenticated redactors.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Redactor')
    

class IsReviewer(permissions.BasePermission):
    """
    Allows access only to authenticated reviewer.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Reviewer')