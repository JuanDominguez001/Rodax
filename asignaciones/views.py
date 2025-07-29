from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Asignacion
from .serializers import AsignacionSerializer
from .permissions import SoloAdminFlota

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    permission_classes = [SoloAdminFlota]
    ordering = ["-fecha_salida"]

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        """POST /api/asignaciones/{id}/finalizar/  -> marca como finalizada"""
        asignacion = self.get_object()
        km_regreso = request.data.get("km_regreso")
        asignacion.finalizar(km_regreso=km_regreso)
        return Response({"status": "finalizada"}, status=status.HTTP_200_OK)
