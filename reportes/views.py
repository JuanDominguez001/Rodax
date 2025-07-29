from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import csv
from io import StringIO
from vehiculos.models import Vehiculo

class ReporteVehiculosCSV(APIView):
    """
    Devuelve un CSV con el inventario de vehículos.
    Permisos: cualquier usuario autenticado (ajusta según tu necesidad).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buffer = StringIO()
        writer = csv.writer(buffer)
        # encabezados
        writer.writerow(["Placa", "Marca", "Modelo", "Año", "Odómetro", "Disponible"])
        # datos
        for v in Vehiculo.objects.all():
            writer.writerow([v.placa, v.marca, v.modelo, v.anio, v.odometro_actual, v.disponible])

        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        filename = f"vehiculos_{timezone.now():%Y%m%d_%H%M}.csv"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class ReporteKilometrajePDF(APIView):
    """
    Placeholder para PDF de kilometraje. Devuelve un PDF “Hello World”.
    Luego podrás reemplazarlo con ReportLab, WeasyPrint, etc.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from reportlab.pdfgen import canvas
        from io import BytesIO

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Reporte de Kilometraje")
        p.drawString(100, 730, "— Generado por Rodax —")
        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        filename = f"kilometraje_{timezone.now():%Y%m%d_%H%M}.pdf"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
