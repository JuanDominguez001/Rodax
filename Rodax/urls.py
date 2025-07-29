from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Rodax/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT global (si aquí manejas tokens)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # DRF login navegable (opcional)
    path("api/auth/", include("rest_framework.urls")),

    # Módulos
    path("api/", include("usuarios.urls")),
    path("api/", include("vehiculos.urls")),
    path("api/", include("asignaciones.urls")),
    path("api/", include("combustible.urls")),
    path("api/", include("mantenimiento.urls")),
    path("api/", include("reportes.urls")),
]
