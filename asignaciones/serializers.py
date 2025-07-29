from rest_framework import serializers
from .models import Asignacion
from vehiculos.models import Vehiculo

class AsignacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = "__all__"
        read_only_fields = ["estado", "fecha_regreso", "km_regreso"]

    # valida que el vehículo esté disponible cuando se crea
    def validate(self, data):
        vehiculo = data["vehiculo"]
        if self.instance is None and not vehiculo.disponible:
            raise serializers.ValidationError("El vehículo no está disponible.")
        return data
