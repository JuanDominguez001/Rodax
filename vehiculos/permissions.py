from rest_framework.permissions import BasePermission, SAFE_METHODS

class SoloLecturaOAdminFlota(BasePermission):
    """
    - GET/HEAD/OPTIONS → todos los usuarios autenticados.
    - POST/PUT/PATCH/DELETE → solo ADMIN o FLOTA.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in {"ADMIN", "FLOTA"}
