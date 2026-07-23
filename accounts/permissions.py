from rest_framework.permissions import BasePermission

from .models import CustomUser


class IsDonor(BasePermission):
    message = "Only donors can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.DONOR)


class IsNGO(BasePermission):
    message = "Only NGOs can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.NGO)


class IsVolunteer(BasePermission):
    message = "Only volunteers can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.VOLUNTEER)


class IsAdminRole(BasePermission):
    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.ADMIN)


class IsOwnerOrReadOnly(BasePermission):
    """
    Anyone authenticated can read (GET/HEAD/OPTIONS).
    Only the object's owner can edit/delete it.
    The view must set `owner_field` to the FK name on the model
    (e.g. 'donor' for FoodDonation).
    """
    owner_field = 'donor'

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        owner_field = getattr(view, 'owner_field', self.owner_field)
        return getattr(obj, owner_field, None) == request.user