from rest_framework import serializers
from .models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"
        read_only_fields = ["estado", "fecha_realizado"]

    # Validación opcional: la fecha programada no puede estar en el pasado
    def validate_fecha_programada(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("La fecha programada no puede estar en el pasado.")
        return value
