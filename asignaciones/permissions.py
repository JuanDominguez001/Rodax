from rest_framework.permissions import BasePermission, SAFE_METHODS

class SoloAdminFlota(BasePermission):
    """
    GET → quien sea autenticado.
    POST/PUT/PATCH/DELETE → solo roles ADMIN o FLOTA.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in {"ADMIN", "FLOTA"}
