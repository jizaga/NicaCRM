from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Caso, Cliente, Compania, Interaccion, Usuario


class EstiloFormulario:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # Bootstrap uses a distinct class for checkbox controls.
            field.widget.attrs["class"] = (
                "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            )

class CompaniaForm(EstiloFormulario, forms.ModelForm):
    class Meta: model=Compania; fields=["nombre","email","telefono","web","direccion","activo"]

class ClienteForm(EstiloFormulario, forms.ModelForm):
    class Meta: model=Cliente; fields=["nombre","apellidos","email","telefono","cargo","compania","comercial","estado","notas"]

class CasoForm(EstiloFormulario, forms.ModelForm):
    class Meta: model=Caso; fields=["asunto","descripcion","cliente","asignado_a","prioridad","estado"]

class InteraccionForm(EstiloFormulario, forms.ModelForm):
    class Meta:
        model=Interaccion; fields=["cliente","caso","tipo","asunto","detalle","fecha"]
        widgets={"fecha": forms.DateTimeInput(attrs={"type":"datetime-local"}, format="%Y-%m-%dT%H:%M")}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha"].input_formats=["%Y-%m-%dT%H:%M"]

class UsuarioForm(EstiloFormulario, UserCreationForm):
    class Meta(UserCreationForm.Meta): model=Usuario; fields=["username","first_name","last_name","email","rol","telefono"]
