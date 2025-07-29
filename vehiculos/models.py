from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    anio = models.PositiveIntegerField()
    odometro_actual = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"{self.placa} – {self.marca} {self.modelo}"

