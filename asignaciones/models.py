from django.db import models
from django.conf import settings
from django.utils import timezone

class Asignacion(models.Model):
    ESTADOS = (
        ("ACTIVA", "Activa"),
        ("FINALIZADA", "Finalizada"),
    )

    vehiculo = models.ForeignKey(
        "vehiculos.Vehiculo",
        on_delete=models.PROTECT,
        related_name="asignaciones",
    )
    conductor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={"role": "CONDUCTOR"},
        related_name="asignaciones",
    )
    fecha_salida = models.DateTimeField(default=timezone.now)
    km_salida = models.PositiveIntegerField()
    fecha_regreso = models.DateTimeField(null=True, blank=True)
    km_regreso = models.PositiveIntegerField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="ACTIVA")

    class Meta:
        verbose_name = "Asignación"
        verbose_name_plural = "Asignaciones"
        ordering = ["-fecha_salida"]

    def finalizar(self, km_regreso=None):
        """Marca la asignación como finalizada."""
        self.fecha_regreso = timezone.now()
        if km_regreso is not None:
            self.km_regreso = km_regreso
        self.estado = "FINALIZADA"
        self.save()

    def __str__(self):
        return f"{self.vehiculo.placa} → {self.conductor.email} ({self.estado})"
