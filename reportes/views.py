# reportes/views.py
from io import StringIO, BytesIO
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from vehiculos.models import Vehiculo
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import csv

class ReporteVehiculosCSV(APIView):
    """Exporta inventario completo de vehículos en CSV."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Placa", "Marca", "Modelo", "Año", "Odómetro", "Disponible"])
        for v in Vehiculo.objects.all():
            writer.writerow([v.placa, v.marca, v.modelo, v.anio, v.odometro_actual, v.disponible])
        filename = f"vehiculos_{timezone.now():%Y%m%d_%H%M}.csv"
        return HttpResponse(buffer.getvalue(),
                            content_type="text/csv",
                            headers={"Content-Disposition": f'attachment; filename=\"{filename}\"'})

class ReporteKilometrajePDF(APIView):
    """PDF con tabla de kilometraje actual por vehículo."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buf = BytesIO()
        p = canvas.Canvas(buf, pagesize=letter)
        width, height = letter

        # Título
        p.setFont("Helvetica-Bold", 14)
        p.drawString(1 * inch, height - 1 * inch, "Reporte de Kilometraje")
        p.setFont("Helvetica", 10)
        p.drawString(1 * inch, height - 1.3 * inch,
                     f"Generado por Rodax – {timezone.now():%d/%m/%Y %H:%M}")

        # Encabezados
        y = height - 2 * inch
        p.setFont("Helvetica-Bold", 10)
        p.drawString(1 * inch, y, "Placa")
        p.drawString(2.2 * inch, y, "Marca")
        p.drawString(3.7 * inch, y, "Modelo")
        p.drawString(5.2 * inch, y, "Km actual")
        y -= 0.2 * inch
        p.line(1 * inch, y, 7.5 * inch, y)

        # Filas
        p.setFont("Helvetica", 10)
        for v in Vehiculo.objects.all():
            y -= 0.3 * inch
            if y < 1 * inch:                  # salto de página
                p.showPage()
                y = height - 1 * inch
            p.drawString(1 * inch, y, v.placa)
            p.drawString(2.2 * inch, y, v.marca)
            p.drawString(3.7 * inch, y, v.modelo)
            p.drawRightString(6.7 * inch, y, str(v.odometro_actual))

        p.showPage()
        p.save()
        buf.seek(0)
        filename = f"kilometraje_{timezone.now():%Y%m%d_%H%M}.pdf"
        return HttpResponse(buf, content_type="application/pdf",
                            headers={"Content-Disposition": f'attachment; filename=\"{filename}\"'})
