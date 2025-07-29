from rest_framework.permissions import BasePermission, SAFE_METHODS

class CombustiblePermiso(BasePermission):
    """
    - Lectura (GET/HEAD/OPTIONS): cualquier usuario autenticado.
    - Escritura (POST): ADMIN, FLOTA o CONDUCTOR.
    - Modificar/Borrar: solo ADMIN o FLOTA.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        if request.method == "POST":
            return request.user.role in {"ADMIN", "FLOTA", "CONDUCTOR"}
        return request.user.role in {"ADMIN", "FLOTA"}
