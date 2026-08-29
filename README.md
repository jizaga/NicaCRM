# SupportCRM

CRM de soporte técnico desarrollado con Django, inspirado en las áreas funcionales de soluciones CRM como VTiger: panel, compañías, clientes/contactos, comerciales, casos e interacciones.

## Funcionalidades

- Usuarios con roles: administrador, soporte técnico y comercial.
- CRUD de compañías, clientes, casos e interacciones.
- Asignación de cada cliente a una compañía y a un comercial.
- Búsqueda de clientes por nombre, apellidos, correo electrónico o empresa.
- Panel con indicadores de clientes, compañías, casos abiertos, actividad reciente y casos por estado.
- Exportación del listado de clientes a CSV y Excel.
- Administración nativa de Django para la gestión avanzada.

## Puesta en marcha

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abra `http://127.0.0.1:8000/`. Cree usuarios comerciales desde Administración o desde el enlace Usuarios; asigne el rol **Comercial** para que aparezcan al editar clientes.

## Alcance

El diseño y código son propios. No replica la identidad visual ni el código de VTiger; organiza un MVP equivalente para soporte técnico, listo para extenderse con SLA, tickets por correo, automatizaciones, base de conocimientos y permisos por módulo.
