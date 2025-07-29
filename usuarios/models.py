from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

ROLES = (
    ("ADMIN", "Administrador"),
    ("FLOTA", "Encargado de flota"),
    ("CONDUCTOR", "Conductor"),
    ("TALLER", "Taller"),
    ("DIRECCION", "Dirección"),
)

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, role="CONDUCTOR", **extra):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("role", "ADMIN")
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "role"]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
