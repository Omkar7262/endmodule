from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class JwtCustomAuthentication(JWTAuthentication):

    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        add = request.META['REMOTE_ADDR']
        if user_auth_tuple is None:
            return
        (user, token) = user_auth_tuple
        if user.user_type not in [1, 2, 3]:
            if user.dwip == add or user.pwip == add or user.sdwip == add or user.spwip == add:
                pass
            else:
                raise PermissionDenied({'message': 'Permission Denied'})

        return user, token


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise NotAuthenticated("Please! Login")
        if request.user.user_type not in [1, 2, 3]:
            raise PermissionDenied(f"You are not authorized")
        return bool(request.user and request.user.is_authenticated)
