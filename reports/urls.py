from django.urls import path

from . import views

urlpatterns = [
    # =========================
    # INVENTARIO
    # =========================
    path('export/categoria_inventario/', views.export_categoria_inventario, name='export_categoria_inventario'),
    path('export/inventario_mantencion/', views.export_inventario_mantencion, name='export_inventario_mantencion'),
    path('export/inventario_informatica/', views.export_inventario_informatica, name='export_inventario_informatica'),

    # =========================
    # ESTABLECIMIENTO
    # =========================
    path('export/establecimiento/', views.export_establecimiento, name='export_establecimiento'),
    path('export/departamento/', views.export_departamento, name='export_departamento'),
    path('export/funcionario/', views.export_funcionario, name='export_funcionario'),

    # =========================
    # EQUIPOS
    # =========================
    path('export/celular/', views.export_celular, name='export_celular'),
    path('export/computador/', views.export_equipo, name='export_equipo'),

    # =========================
    # TICKETS
    # =========================
    path('export/ticket/', views.export_ticket, name='export_ticket'),
    path('export/ticket_activo/', views.export_ticket_activo, name='export_ticket_activo'),

    # =========================
    # CATALOGO
    # =========================
    path('export/comuna/', views.export_comuna, name='export_comuna'),
    path('export/marca/', views.export_marca, name='export_marca'),
    path('export/categoria/', views.export_categoria, name='export_categoria'),
    path('export/subcategoria/', views.export_subcategoria, name='export_subcategoria'),
    path('export/modelo/', views.export_modelo, name='export_modelo'),
    path('export/propietario/', views.export_propietario, name='export_propietario'),
    path('export/licencia_os/', views.export_licencia_os, name='export_licencia_os'),
    path('export/microsoft_office/', views.export_microsoft_office, name='export_microsoft_office'),
    path('export/sistema_operativo/', views.export_sistema_operativo, name='export_sistema_operativo'),
    path('export/tipo_celular/', views.export_tipo_celular, name='export_tipo_celular'),
    path('export/tipo_computador/', views.export_tipo_computador, name='export_tipo_computador'),
    path('export/tipo_impresora/', views.export_tipo_impresora, name='export_tipo_impresora'),
    path('export/toner/', views.export_toner, name='export_toner'),
    path('export/jefe_tic/', views.export_jefe_tic, name='export_jefe_tic'),
    path('export/contrato/', views.export_contrato, name='export_contrato'),
    path('export/tipo_soporte/', views.export_tipo_soporte, name='export_tipo_soporte'),
    path('export/puesto_trabajo/', views.export_puesto_trabajo, name='export_puesto_trabajo'),
    path('export/ips/', views.export_ips, name='export_ips'),

    # =========================
    # USERS
    # =========================
    path('export/role/', views.export_role, name='export_role'),
    path('export/user/', views.export_user, name='export_user'),
    path('export/user-soporte/', views.export_user_soporte, name='export_user_soporte'),
]
