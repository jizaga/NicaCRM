from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("companias/", views.compania_lista, name="compania_lista"),
    path("companias/nueva/", views.compania_form, name="compania_nueva"),
    path("companias/<int:pk>/editar/", views.compania_form, name="compania_editar"),
    path("clientes/", views.cliente_lista, name="cliente_lista"),
    path("clientes/nuevo/", views.cliente_form, name="cliente_nuevo"),
    path("clientes/<int:pk>/", views.cliente_detalle, name="cliente_detalle"),
    path("clientes/<int:pk>/editar/", views.cliente_form, name="cliente_editar"),
    path("casos/", views.caso_lista, name="caso_lista"), path("casos/nuevo/", views.caso_form, name="caso_nuevo"),
    path("casos/<int:pk>/editar/", views.caso_form, name="caso_editar"),
    path("interacciones/", views.interaccion_lista, name="interaccion_lista"),
    path("interacciones/nueva/", views.interaccion_form, name="interaccion_nueva"),
    path("interacciones/<int:pk>/editar/", views.interaccion_form, name="interaccion_editar"),
    path("usuarios/nuevo/", views.usuario_nuevo, name="usuario_nuevo"),
    path("exportar/clientes.<str:formato>", views.exportar_clientes, name="exportar_clientes"),
] + debug_toolbar_urls()
