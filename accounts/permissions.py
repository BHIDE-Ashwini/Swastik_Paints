from rest_framework.permissions import BasePermission


class IsAdminProfile(BasePermission):
    message = "An active admin profile is required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            admin = request.user.admin_profile
        except AttributeError:
            return False

        return admin.is_active


class IsSuperAdmin(IsAdminProfile):
    message = "Super Admin access required."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.admin_profile.role == "SUPER_ADMIN"


class IsManager(IsAdminProfile):
    message = "Manager access required."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.admin_profile.role == "MANAGER"


class IsStaff(IsAdminProfile):
    message = "Staff access required."

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.admin_profile.role == "STAFF"