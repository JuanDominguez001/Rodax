from django.contrib import admin
from .models import Servicio

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display  = ("vehiculo", "tipo", "estado", "fecha_programada", "fecha_realizado", "costo")
    list_filter   = ("tipo", "estado", "fecha_programada")
    search_fields = ("vehiculo__placa",)
