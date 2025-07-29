from django.contrib import admin
from .models import CargaCombustible

@admin.register(CargaCombustible)
class CargaCombustibleAdmin(admin.ModelAdmin):
    list_display  = ("vehiculo", "conductor", "litros", "costo", "odometro", "fecha")
    list_filter   = ("vehiculo", "conductor")
    search_fields = ("vehiculo__placa",)
    date_hierarchy = "fecha"