from rest_framework.permissions import BasePermission, SAFE_METHODS

class ServicioPermiso(BasePermission):
    """
    - Lectura: cualquiera autenticado.
    - Alta: ADMIN, FLOTA, TALLER.
    - Modificación / Borrado: ADMIN o FLOTA.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        if request.method == "POST":
            return request.user.role in {"ADMIN", "FLOTA", "TALLER"}
        return request.user.role in {"ADMIN", "FLOTA"}
