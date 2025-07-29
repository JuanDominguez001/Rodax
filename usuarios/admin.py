from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    ordering       = ("email",)
    list_display   = ("email", "nombre", "role", "is_active", "is_staff")
    list_filter    = ("role", "is_active", "is_staff")
    search_fields  = ("email", "nombre")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Datos personales", {"fields": ("nombre", "role")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre", "role", "password1", "password2"),
        }),
    )

    # usar email como credencial
    add_form_template   = None
    change_password_form = None
