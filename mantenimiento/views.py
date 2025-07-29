from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Servicio
from .serializers import ServicioSerializer
from .permissions import ServicioPermiso

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.select_related("vehiculo", "taller")
    serializer_class = ServicioSerializer
    permission_classes = [ServicioPermiso]
    ordering = ["-fecha_programada"]

    @action(detail=True, methods=["post"])
    def completar(self, request, pk=None):
        """
        POST /api/mantenimientos/{id}/completar/
        Marca el servicio como COMPLETADO y fija la fecha_realizado.
        """
        servicio = self.get_object()
        servicio.marcar_completado()
        return Response({"status": "completado"}, status=status.HTTP_200_OK)
