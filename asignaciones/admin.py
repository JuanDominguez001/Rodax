from django.contrib import admin
from .models import Asignacion

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display  = ("vehiculo", "conductor", "fecha_salida", "estado")
    list_filter   = ("estado", "fecha_salida")
    search_fields = ("vehiculo__placa", "conductor__email")
