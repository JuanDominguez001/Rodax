from rest_framework import viewsets
from .models import CargaCombustible
from .serializers import CargaCombustibleSerializer
from .permissions import CombustiblePermiso

class CombustibleViewSet(viewsets.ModelViewSet):
    queryset = CargaCombustible.objects.select_related("vehiculo", "conductor")
    serializer_class = CargaCombustibleSerializer
    permission_classes = [CombustiblePermiso]
    ordering = ["-fecha"]
    filterset_fields = ["vehiculo__placa", "conductor__email"]  # si luego instalas django-filter
