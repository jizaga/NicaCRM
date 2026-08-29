from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Caso, Cliente, Compania, Interaccion, Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("CRM", {"fields": ("rol", "telefono")}),)
    list_display = ("username", "email", "first_name", "last_name", "rol")

admin.site.register([Compania, Cliente, Caso, Interaccion])
