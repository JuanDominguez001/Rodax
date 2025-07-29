from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class CargaCombustible(models.Model):
    vehiculo = models.ForeignKey(
        "vehiculos.Vehiculo",
        on_delete=models.PROTECT,
        related_name="cargas_combustible",
    )
    conductor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={"role": "CONDUCTOR"},
        related_name="cargas_combustible",
    )
    litros = models.DecimalField(max_digits=6, decimal_places=2)
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    odometro = models.PositiveIntegerField(help_text="Lectura de odómetro al cargar")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Carga de Combustible"
        verbose_name_plural = "Cargas de Combustible"
        ordering = ["-fecha"]

    def clean(self):
        """Evita registrar un odómetro menor o igual al último."""
        ultimo = (
            CargaCombustible.objects.filter(vehiculo=self.vehiculo)
            .order_by("-fecha")
            .first()
        )
        if ultimo and self.odometro <= ultimo.odometro:
            raise ValidationError("El odómetro debe ser mayor al último registrado.")

    def __str__(self):
        return f"{self.vehiculo.placa} – {self.litros} L @ {self.fecha:%Y-%m-%d}"
