from rest_framework import serializers
from .models import CargaCombustible

class CargaCombustibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaCombustible
        fields = "__all__"
        read_only_fields = ["fecha"]

    # Valida que el odómetro crezca (segunda capa, además del clean() del modelo)
    def validate(self, data):
        vehiculo = data["vehiculo"]
        ultimo = (
            CargaCombustible.objects.filter(vehiculo=vehiculo)
            .order_by("-fecha")
            .first()
        )
        if ultimo and data["odometro"] <= ultimo.odometro:
            raise serializers.ValidationError("El odómetro debe ser mayor al último registrado.")
        return data
