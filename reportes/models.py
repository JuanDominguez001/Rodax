from django.db import models
from django.contrib.auth import get_user_model

class Exportacion(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=30)                   # p.e. "vehiculos", "kilometraje"
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to="reportes/")        # se guarda el PDF/CSV generado

    def __str__(self):
        return f"{self.tipo} - {self.fecha:%Y-%m-%d %H:%M}"
