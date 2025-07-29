from rest_framework import viewsets
from .models import Vehiculo
from .serializers import VehiculoSerializer
from .permissions import SoloLecturaOAdminFlota

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [SoloLecturaOAdminFlota]

    # ordena por placa por default
    ordering = ["placa"]
    search_fields = ["placa", "marca", "modelo"]   # si luego añades SearchFilter
