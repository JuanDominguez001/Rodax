from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ("placa", "marca", "modelo", "anio", "odometro_actual", "disponible")
    list_filter   = ("marca", "disponible")
    search_fields = ("placa", "marca", "modelo")
