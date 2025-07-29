from django.db import models
from django.conf import settings
from django.utils import timezone

class Servicio(models.Model):
    TIPOS = (
        ("PREVENTIVO", "Preventivo"),
        ("CORRECTIVO", "Correctivo"),
    )
    ESTADOS = (
        ("PENDIENTE", "Pendiente"),
        ("COMPLETADO", "Completado"),
    )

    vehiculo = models.ForeignKey(
        "vehiculos.Vehiculo",
        on_delete=models.PROTECT,
        related_name="servicios",
    )
    taller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={"role": "TALLER"},
        related_name="servicios_realizados",
    )
    tipo = models.CharField(max_length=11, choices=TIPOS)
    descripcion = models.TextField()
    fecha_programada = models.DateField()
    fecha_realizado = models.DateField(null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    km_proximo = models.PositiveIntegerField(
        help_text="Kilometraje estimado para el próximo servicio"
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default="PENDIENTE")

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["-fecha_programada"]

    def marcar_completado(self, fecha=None):
        self.estado = "COMPLETADO"
        self.fecha_realizado = fecha or timezone.now().date()
        self.save()

    def __str__(self):
        return f"{self.vehiculo.placa} – {self.tipo} ({self.estado})"
