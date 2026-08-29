from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        SOPORTE = "SOPORTE", "Soporte técnico"
        COMERCIAL = "COMERCIAL", "Comercial"
    rol = models.CharField(max_length=12, choices=Rol.choices, default=Rol.SOPORTE)
    telefono = models.CharField(max_length=30, blank=True)

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username


class Compania(models.Model):
    nombre = models.CharField(max_length=180, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    web = models.URLField(blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Compañías"

    def __str__(self): return self.nombre


class Cliente(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "ACTIVO", "Activo"
        INACTIVO = "INACTIVO", "Inactivo"
        PROSPECTO = "PROSPECTO", "Prospecto"
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=120, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    compania = models.ForeignKey(Compania, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")
    comercial = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes_asignados", limit_choices_to={"rol": "COMERCIAL"})
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta: ordering = ["nombre", "apellidos"]
    def __str__(self): return f"{self.nombre} {self.apellidos}".strip()
    def get_absolute_url(self): return reverse("cliente_detalle", args=[self.pk])


class Caso(models.Model):
    class Prioridad(models.TextChoices): BAJA="BAJA","Baja"; MEDIA="MEDIA","Media"; ALTA="ALTA","Alta"; CRITICA="CRITICA","Crítica"
    class Estado(models.TextChoices): ABIERTO="ABIERTO","Abierto"; EN_PROGRESO="PROGRESO","En progreso"; RESUELTO="RESUELTO","Resuelto"; CERRADO="CERRADO","Cerrado"
    numero = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="casos")
    asignado_a = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="casos_asignados")
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ABIERTO)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta: ordering = ["-actualizado_en"]
    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo = Caso.objects.order_by("-id").first()
            self.numero = f"CAS-{(ultimo.id if ultimo else 0) + 1:05d}"
        super().save(*args, **kwargs)
    def __str__(self): return f"{self.numero} — {self.asunto}"


class Interaccion(models.Model):
    class Tipo(models.TextChoices): LLAMADA="LLAMADA","Llamada"; EMAIL="EMAIL","Correo"; REUNION="REUNION","Reunión"; NOTA="NOTA","Nota"
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="interacciones")
    caso = models.ForeignKey(Caso, on_delete=models.SET_NULL, null=True, blank=True, related_name="interacciones")
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="interacciones")
    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.NOTA)
    asunto = models.CharField(max_length=180)
    detalle = models.TextField()
    fecha = models.DateTimeField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ["-fecha"]
    def __str__(self): return self.asunto
