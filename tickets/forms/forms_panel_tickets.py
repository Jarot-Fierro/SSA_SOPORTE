from django import forms
from django.contrib.auth import get_user_model

from catalogo.models import TipoSoporte

User = get_user_model()

from establecimiento.models.funcionario import Funcionario
from tickets.models import Ticket


class FormPanelTicket(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['asignado_a'].label_from_instance = lambda obj: obj.nombre_completo

        if self.instance and self.instance.departamento:
            self.initial['departamento'] = str(self.instance.departamento)

    numero_ticket = forms.CharField(
        label='Número de ticket',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True
        }),
        required=False
    )

    departamento = forms.CharField(
        label='Departamento',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Departamento del solicitante',
            'readonly': True
        }),
        required=False
    )

    funcionario = forms.ModelChoiceField(
        label='Funcionario solicitante',
        queryset=Funcionario.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'readonly': True,
        }),
        required=True
    )

    asignado_a = forms.ModelChoiceField(
        label='Asignado a',
        empty_label='Asignar Soporte a',
        queryset=User.objects.filter(usuario_soporte=True),
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        }),
        required=False
    )

    estado = forms.ChoiceField(
        label='Estado',
        choices=Ticket.ESTADOS,
        widget=forms.Select(attrs={
            'class': 'form-control select2-status'
        }),
        required=True
    )

    titulo = forms.CharField(
        label='Título del problema',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Problema con impresora',
            'readonly': True
        }),
        required=True
    )

    descripcion = forms.CharField(
        label='Descripción del problema',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa el problema que está presentando',
            'readonly': True
        }),
        required=True
    )
    solucion = forms.CharField(
        label='Solución del problema',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa la solución empleada'
        }),
        required=True
    )
    tipo_soporte = forms.ModelChoiceField(
        label='Tipo Soporte',
        empty_label='Selecciona el Tipo Soporte',
        queryset=TipoSoporte.objects.filter(status=True),
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        }),
        required=False
    )

    fecha_cierre = forms.DateTimeField(
        label='Fecha de cierre',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=False
    )

    class Meta:
        model = Ticket
        fields = [
            'numero_ticket',
            'departamento',
            'funcionario',
            'asignado_a',
            'estado',
            'titulo',
            'descripcion',
            'solucion',
            'fecha_cierre',
            'tipo_soporte',
        ]
