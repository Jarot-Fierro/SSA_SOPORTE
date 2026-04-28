from catalogo.models import Marca, Categoria, SubCategoria, Modelo, Propietario, LicenciaOs, MicrosoftOffice, \
    SistemaOperativo, TipoCelular, TipoComputador, TipoImpresora, Toner, JefeTic, Contrato, TipoSoporte, PuestoTrabajo, \
    Ips
from equipo.models.celular import Celular
from equipo.models.equipos import Equipo
from establecimiento.models.departamento import *
from establecimiento.models.establecimiento import *
from establecimiento.models.funcionario import Funcionario
from inventario.models import *
from tickets.models import Ticket, TicketActivo
from users.models import Role, User
from .utils import export_queryset_to_excel


## TERMINO PACIENTE

def export_categoria_inventario(request):
    queryset = CategoriaInventario.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='categorias_inventario')


def export_inventario_mantencion(request):
    queryset = InventarioMantencion.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='inventario_mantencion')


def export_inventario_informatica(request):
    queryset = InventarioInformatica.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='inventario_informatica')


def export_comuna(request):
    queryset = Comuna.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='comunas')


def export_establecimiento(request):
    queryset = Establecimiento.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='establecimientos')


def export_departamento(request):
    queryset = Departamento.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='departamentos')


def export_funcionario(request):
    queryset = Funcionario.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='funcionarios')


def export_celular(request):
    queryset = Celular.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='celulares')


def export_equipo(request):
    queryset = Equipo.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='equipos')


def export_ticket(request):
    queryset = Ticket.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tickets')


def export_ticket_activo(request):
    queryset = TicketActivo.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tickets_activos')


def export_marca(request):
    queryset = Marca.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='marcas')


def export_categoria(request):
    queryset = Categoria.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='categorias')


def export_subcategoria(request):
    queryset = SubCategoria.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='subcategorias')


def export_modelo(request):
    queryset = Modelo.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='modelos')


def export_propietario(request):
    queryset = Propietario.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='propietarios')


def export_licencia_os(request):
    queryset = LicenciaOs.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='licencias_os')


def export_microsoft_office(request):
    queryset = MicrosoftOffice.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='microsoft_office')


def export_sistema_operativo(request):
    queryset = SistemaOperativo.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='sistemas_operativos')


def export_tipo_celular(request):
    queryset = TipoCelular.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tipos_celular')


def export_tipo_computador(request):
    queryset = TipoComputador.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tipos_computador')


def export_tipo_impresora(request):
    queryset = TipoImpresora.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tipos_impresora')


def export_toner(request):
    queryset = Toner.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='toners')


def export_jefe_tic(request):
    queryset = JefeTic.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='jefes_tic')


def export_contrato(request):
    queryset = Contrato.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='contratos')


def export_tipo_soporte(request):
    queryset = TipoSoporte.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='tipos_soporte')


def export_puesto_trabajo(request):
    queryset = PuestoTrabajo.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='puestos_trabajo')


def export_ips(request):
    queryset = Ips.objects.all().order_by('-updated_at')
    return export_queryset_to_excel(queryset, filename='ips')


def export_role(request):
    queryset = Role.objects.all().order_by('-id')
    return export_queryset_to_excel(queryset, filename='roles')


def export_user(request):
    queryset = User.objects.filter(usuario_soporte=False).order_by('-id')
    return export_queryset_to_excel(queryset, filename='usuarios', excluded_fields=['password'])


def export_user_soporte(request):
    queryset = User.objects.filter(usuario_soporte=True).order_by('-id')
    return export_queryset_to_excel(queryset, filename='usuarios_soporte', excluded_fields=['password'])

#
# def export_comuna(request):
#     queryset = Comuna.objects.all().order_by('-updated_at')
#     return export_queryset_to_excel(queryset, filename='comunas')
#
#
# def export_establecimiento(request):
#     queryset = Establecimiento.objects.all().order_by('-updated_at')
#     return export_queryset_to_excel(queryset, filename='establecimientos')
#
#
# ## CSV FICHAS
# def export_ficha_csv(request):
#     queryset = Ficha.objects.filter(
#         establecimiento=request.user.establecimiento
#     )
#     return export_queryset_to_csv_fast(queryset, filename='fichas', fields=fields_ficha_csv)
#
#
# def export_ficha_pasivadas_csv(request):
#     queryset = Ficha.objects.filter(
#         establecimiento=request.user.establecimiento, pasivado=True
#     )
#     return export_queryset_to_csv_fast(queryset, filename='fichas_pasivadas', fields=fields_ficha_csv)
#
#
# ## TERMINO FICHAS
#
# ## CSV MOVIMIENTOS FICHAS
#
# def export_movimiento_ficha_csv(request):
#     queryset = MovimientoFicha.objects.filter(
#         ficha__establecimiento=request.user.establecimiento
#     ).order_by('-updated_at')
#     return export_queryset_to_csv_fast(
#         queryset,
#         filename='movimientos_ficha',
#         fields=fields_movimiento_ficha_csv
#     )
#
#
# def export_movimiento_ficha_envio_csv(request):
#     queryset = MovimientoFicha.objects.filter(
#         ficha__establecimiento=request.user.establecimiento,
#         estado_envio='ENVIADO'
#     ).order_by('-updated_at')
#     return export_queryset_to_csv_fast(
#         queryset,
#         filename='movimientos_ficha_enviadas',
#         fields=fields_movimiento_ficha_csv
#     )
#
#
# def export_movimiento_ficha_recepcion_csv(request):
#     queryset = MovimientoFicha.objects.filter(
#         ficha__establecimiento=request.user.establecimiento,
#         estado_recepcion='RECIBIDO'
#     ).order_by('-updated_at')
#     return export_queryset_to_csv_fast(
#         queryset,
#         filename='movimientos_ficha_recepcionadas',
#         fields=fields_movimiento_ficha_csv
#     )
#
#
# def export_movimiento_ficha_traspaso_csv(request):
#     queryset = MovimientoFicha.objects.filter(
#         ficha__establecimiento=request.user.establecimiento,
#         estado_traspaso='TRASPASADO'
#     ).order_by('-updated_at')
#     return export_queryset_to_csv_fast(
#         queryset,
#         filename='movimientos_ficha_traspasadas',
#         fields=fields_movimiento_ficha_csv
#     )
#
#
# ## TERMINO MOVIMIENTOS FICHAS
#
#
# ## CSV PACIENTE
# def export_paciente_csv(request):
#     queryset = Paciente.objects.all()
#     return export_queryset_to_csv_fast(queryset, filename='pacientes', fields=fields_paciente_csv)
#
#
# def export_paciente_recien_nacido_csv(request):
#     queryset = Paciente.objects.filter(recien_nacido=True)
#     return export_queryset_to_csv_fast(queryset, filename='pacientes_recien_nacidos_csv', fields=fields_paciente_csv)
#
#
# def export_paciente_extranjero_csv(request):
#     queryset = Paciente.objects.filter(extranjero=True)
#     return export_queryset_to_csv_fast(queryset, filename='pacientes_extranjeros_csv', fields=fields_paciente_csv)
#
#
# def export_paciente_fallecido_csv(request):
#     queryset = Paciente.objects.filter(fallecido=True)
#     return export_queryset_to_csv_fast(queryset, filename='pacientes_fallecids_csv', fields=fields_paciente_csv)
#
#
# def export_paciente_pueblo_indigena_csv(request):
#     queryset = Paciente.objects.filter(pueblo_indigena=True)
#     return export_queryset_to_csv_fast(queryset, filename='pacientes_pueblo_indigena_csv', fields=fields_paciente_csv)
