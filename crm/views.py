import csv
from datetime import timedelta
from io import BytesIO

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from openpyxl import Workbook

from .forms import CasoForm, ClienteForm, CompaniaForm, InteraccionForm, UsuarioForm
from .models import Caso, Cliente, Compania, Interaccion


def acceso(request):
    if request.user.is_authenticated: return redirect("dashboard")
    return render(request, "registration/login.html")

@login_required
def dashboard(request):
    desde = timezone.now() - timedelta(days=30)
    context = {
        "clientes": Cliente.objects.count(), "companias": Compania.objects.count(),
        "casos_abiertos": Caso.objects.exclude(estado__in=[Caso.Estado.RESUELTO, Caso.Estado.CERRADO]).count(),
        "interacciones_mes": Interaccion.objects.filter(fecha__gte=desde).count(),
        "por_estado": Caso.objects.values("estado").annotate(total=Count("id")).order_by("estado"),
        "casos_recientes": Caso.objects.select_related("cliente", "asignado_a")[:7],
        "interacciones_recientes": Interaccion.objects.select_related("cliente", "usuario")[:7],
    }
    return render(request, "crm/dashboard.html", context)

@login_required
def compania_lista(request):
    return render(request, "crm/compania_lista.html", {"companias": Compania.objects.annotate(total_clientes=Count("clientes"))})

@login_required
def compania_form(request, pk=None):
    obj = get_object_or_404(Compania, pk=pk) if pk else None
    form = CompaniaForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid(): form.save(); return redirect("compania_lista")
    return render(request, "crm/form.html", {"form": form, "titulo": "Editar compañía" if obj else "Nueva compañía", "volver": "compania_lista"})

@login_required
def cliente_lista(request):
    termino = request.GET.get("q", "").strip()
    clientes = Cliente.objects.select_related("compania", "comercial")
    if termino:
        clientes = clientes.filter(Q(nombre__icontains=termino)|Q(apellidos__icontains=termino)|Q(email__icontains=termino)|Q(compania__nombre__icontains=termino))
    return render(request, "crm/cliente_lista.html", {"clientes": clientes, "q": termino})

@login_required
def cliente_detalle(request, pk):
    cliente = get_object_or_404(Cliente.objects.select_related("compania", "comercial"), pk=pk)
    return render(request, "crm/cliente_detalle.html", {"cliente": cliente, "casos": cliente.casos.select_related("asignado_a")[:10], "interacciones": cliente.interacciones.select_related("usuario", "caso")[:10]})

@login_required
def cliente_form(request, pk=None):
    obj = get_object_or_404(Cliente, pk=pk) if pk else None
    form = ClienteForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid(): return redirect(form.save())
    return render(request, "crm/form.html", {"form": form, "titulo": "Editar cliente" if obj else "Nuevo cliente", "volver": "cliente_lista"})

@login_required
def caso_lista(request):
    return render(request, "crm/caso_lista.html", {"casos": Caso.objects.select_related("cliente", "asignado_a")})

@login_required
def caso_form(request, pk=None):
    obj = get_object_or_404(Caso, pk=pk) if pk else None
    form = CasoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid(): form.save(); return redirect("caso_lista")
    return render(request, "crm/form.html", {"form": form, "titulo": "Editar caso" if obj else "Nuevo caso", "volver": "caso_lista"})

@login_required
def interaccion_lista(request):
    return render(request, "crm/interaccion_lista.html", {"interacciones": Interaccion.objects.select_related("cliente", "caso", "usuario")})

@login_required
def interaccion_form(request, pk=None):
    obj = get_object_or_404(Interaccion, pk=pk) if pk else None
    form = InteraccionForm(request.POST or None, instance=obj, initial={"fecha": timezone.localtime().strftime("%Y-%m-%dT%H:%M")})
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False); item.usuario = request.user; item.save(); return redirect("interaccion_lista")
    return render(request, "crm/form.html", {"form": form, "titulo": "Editar interacción" if obj else "Nueva interacción", "volver": "interaccion_lista"})

@login_required
def usuario_nuevo(request):
    form = UsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user=form.save(); login(request, user); return redirect("dashboard")
    return render(request, "crm/form.html", {"form": form, "titulo": "Nuevo usuario", "volver": "dashboard"})

@login_required
def exportar_clientes(request, formato):
    filas = Cliente.objects.select_related("compania", "comercial")
    encabezado = ["Nombre", "Apellidos", "Email", "Teléfono", "Empresa", "Comercial", "Estado"]
    datos = [[c.nombre,c.apellidos,c.email,c.telefono,c.compania.nombre if c.compania else "",c.comercial.nombre_completo if c.comercial else "",c.get_estado_display()] for c in filas]
    if formato == "csv":
        response=HttpResponse(content_type="text/csv; charset=utf-8"); response["Content-Disposition"]='attachment; filename="clientes.csv"'
        response.write("\ufeff"); writer=csv.writer(response); writer.writerow(encabezado); writer.writerows(datos); return response
    libro=Workbook(); hoja=libro.active; hoja.title="Clientes"; hoja.append(encabezado)
    for fila in datos: hoja.append(fila)
    for columna in hoja.columns:
        hoja.column_dimensions[columna[0].column_letter].width = min(max(len(str(c.value or "")) for c in columna)+2, 35)
    buffer=BytesIO(); libro.save(buffer)
    response=HttpResponse(buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"]='attachment; filename="clientes.xlsx"'; return response
