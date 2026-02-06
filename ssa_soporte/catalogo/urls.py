from django.urls import path

from catalogo.views.licencia_os import *
from catalogo.views.marca import *
from catalogo.views.microsoft_office import *
from catalogo.views.modelo import *
from catalogo.views.propietario import *
from catalogo.views.sistema_operativo import *
from catalogo.views.subcategoria import *
from catalogo.views.tipo_celular import *
from catalogo.views.tipo_computador import *
from catalogo.views.tipo_impresora import *
from establecimiento.views.comuna import *

urlpatterns = [
    # COMUNAS
    path('lista-comunas/', ComunaListView.as_view(), name='list_comunas'),
    path('detalle-comunas/<int:pk>/detalle/', ComunaDetailView.as_view(), name='detail_comunas'),
    path('crear-comunas/', ComunaCreateView.as_view(), name='create_comunas'),
    path('actualizar-comunas/<int:pk>/detalle/', ComunaUpdateView.as_view(), name='update_comunas'),
    path('historial-comunas/', ComunaHistoryListView.as_view(), name='historical_comunas'),

    # LICENCIA OS
    path('lista-licencia_os/', LicenciaOsListView.as_view(), name='list_licencia_os'),
    path('detalle-licencia_os/<int:pk>/detalle/', LicenciaOsDetailView.as_view(), name='detail_licencia_os'),
    path('crear-licencia_os/', LicenciaOsCreateView.as_view(), name='create_licencia_os'),
    path('actualizar-licencia_os/<int:pk>/detalle/', LicenciaOsUpdateView.as_view(), name='update_licencia_os'),
    path('historial-licencia_os/', LicenciaOsHistoryListView.as_view(), name='historical_licencia_os'),

    # MARCAS
    path('lista-marcas/', MarcaListView.as_view(), name='list_marcas'),
    path('detalle-marcas/<int:pk>/detalle/', MarcaDetailView.as_view(), name='detail_marcas'),
    path('crear-marcas/', MarcaCreateView.as_view(), name='create_marcas'),
    path('actualizar-marcas/<int:pk>/detalle/', MarcaUpdateView.as_view(), name='update_marcas'),
    path('historial-marcas/', MarcaHistoryListView.as_view(), name='historical_marcas'),

    # MICROSOFT OFFICE
    path('lista-microsoft_office/', MicrosoftOfficeListView.as_view(), name='list_microsoft_office'),
    path('detalle-microsoft_office/<int:pk>/detalle/', MicrosoftOfficeDetailView.as_view(),
         name='detail_microsoft_office'),
    path('crear-microsoft_office/', MicrosoftOfficeCreateView.as_view(), name='create_microsoft_office'),
    path('actualizar-microsoft_office/<int:pk>/detalle/', MicrosoftOfficeUpdateView.as_view(),
         name='update_microsoft_office'),
    path('historial-microsoft_office/', MicrosoftOfficeHistoryListView.as_view(), name='historical_microsoft_office'),

    # MODELOS
    path('lista-modelos/', ModeloListView.as_view(), name='list_modelos'),
    path('detalle-modelos/<int:pk>/detalle/', ModeloDetailView.as_view(), name='detail_modelos'),
    path('crear-modelos/', ModeloCreateView.as_view(), name='create_modelos'),
    path('actualizar-modelos/<int:pk>/detalle/', ModeloUpdateView.as_view(), name='update_modelos'),
    path('historial-modelos/', ModeloHistoryListView.as_view(), name='historical_modelos'),

    # PROPIETARIOS
    path('lista-propietarios/', PropietarioListView.as_view(), name='list_propietarios'),
    path('detalle-propietarios/<int:pk>/detalle/', PropietarioDetailView.as_view(), name='detail_propietarios'),
    path('crear-propietarios/', PropietarioCreateView.as_view(), name='create_propietarios'),
    path('actualizar-propietarios/<int:pk>/detalle/', PropietarioUpdateView.as_view(), name='update_propietarios'),
    path('historial-propietarios/', PropietarioHistoryListView.as_view(), name='historical_propietarios'),

    # SISTEMAS OPERATIVOS
    path('lista-sistemas_operativos/', SistemaOperativoListView.as_view(), name='list_sistemas_operativos'),
    path('detalle-sistemas_operativos/<int:pk>/detalle/', SistemaOperativoDetailView.as_view(),
         name='detail_sistemas_operativos'),
    path('crear-sistemas_operativos/', SistemaOperativoCreateView.as_view(), name='create_sistemas_operativos'),
    path('actualizar-sistemas_operativos/<int:pk>/detalle/', SistemaOperativoUpdateView.as_view(),
         name='update_sistemas_operativos'),
    path('historial-sistemas_operativos/', SistemaOperativoHistoryListView.as_view(),
         name='historical_sistemas_operativos'),

    # SUBCATEGORIAS
    path('lista-subcategorias/', SubCategoriaListView.as_view(), name='list_subcategorias'),
    path('detalle-subcategorias/<int:pk>/detalle/', SubCategoriaDetailView.as_view(), name='detail_subcategorias'),
    path('crear-subcategorias/', SubCategoriaCreateView.as_view(), name='create_subcategorias'),
    path('actualizar-subcategorias/<int:pk>/detalle/', SubCategoriaUpdateView.as_view(), name='update_subcategorias'),
    path('historial-subcategorias/', SubCategoriaHistoryListView.as_view(), name='historical_subcategorias'),

    # TIPO CELULAR
    path('lista-tipo_celular/', TipoCelularListView.as_view(), name='list_tipo_celular'),
    path('detalle-tipo_celular/<int:pk>/detalle/', TipoCelularDetailView.as_view(), name='detail_tipo_celular'),
    path('crear-tipo_celular/', TipoCelularCreateView.as_view(), name='create_tipo_celular'),
    path('actualizar-tipo_celular/<int:pk>/detalle/', TipoCelularUpdateView.as_view(), name='update_tipo_celular'),
    path('historial-tipo_celular/', TipoCelularHistoryListView.as_view(), name='historical_tipo_celular'),

    # TIPO COMPUTADOR
    path('lista-tipo_computador/', TipoComputadorListView.as_view(), name='list_tipo_computador'),
    path('detalle-tipo_computador/<int:pk>/detalle/', TipoComputadorDetailView.as_view(),
         name='detail_tipo_computador'),
    path('crear-tipo_computador/', TipoComputadorCreateView.as_view(), name='create_tipo_computador'),
    path('actualizar-tipo_computador/<int:pk>/detalle/', TipoComputadorUpdateView.as_view(),
         name='update_tipo_computador'),
    path('historial-tipo_computador/', TipoComputadorHistoryListView.as_view(), name='historical_tipo_computador'),

    # TIPO IMPRESORA
    path('lista-tipo_impresora/', TipoImpresoraListView.as_view(), name='list_tipo_impresora'),
    path('detalle-tipo_impresora/<int:pk>/detalle/', TipoImpresoraDetailView.as_view(), name='detail_tipo_impresora'),
    path('crear-tipo_impresora/', TipoImpresoraCreateView.as_view(), name='create_tipo_impresora'),
    path('actualizar-tipo_impresora/<int:pk>/detalle/', TipoImpresoraUpdateView.as_view(),
         name='update_tipo_impresora'),
    path('historial-tipo_impresora/', TipoImpresoraHistoryListView.as_view(), name='historical_tipo_impresora'),

]
