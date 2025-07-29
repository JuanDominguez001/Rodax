from django.urls import path
from .views import ReporteVehiculosCSV, ReporteKilometrajePDF

urlpatterns = [
    path("reportes/vehiculos/", ReporteVehiculosCSV.as_view(), name="reporte_vehiculos_csv"),
    path("reportes/kilometraje/", ReporteKilometrajePDF.as_view(), name="reporte_kilometraje_pdf"),
]
