from django import forms

from catalogo.models import (
    Marca,
    Modelo,
    TipoComputador,
    SistemaOperativo,
    MicrosoftOffice, Propietario, JefeTic, Contrato
)
from equipo.models.computador import Computador
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario


class FormComputador(forms.ModelForm):
    serie = forms.CharField(
        label='Número de Serie',
        widget=forms.TextInput(
            attrs={
                'id': 'serie',
                'class': 'form-control',
                'placeholder': 'Ingrese número de serie',
            }
        ),
        required=True
    )

    mac = forms.CharField(
        label='Dirección MAC',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 00:1A:2B:3C:4D:5E',
            }
        ),
        required=False
    )

    ip = forms.CharField(
        label='Dirección IP',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 192.168.1.10',
            }
        ),
        required=False
    )

    marca = forms.ModelChoiceField(
        label='Marca',
        queryset=Marca.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
    )

    modelo = forms.ModelChoiceField(
        label='Modelo',
        queryset=Modelo.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
    )

    tipo = forms.ModelChoiceField(
        label='Tipo de Computador',
        queryset=TipoComputador.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
    )

    sistema_operativo = forms.ModelChoiceField(
        label='Sistema Operativo',
        queryset=SistemaOperativo.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
    )

    microsoft_office = forms.ModelChoiceField(
        label='Microsoft Office',
        queryset=MicrosoftOffice.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
    )

    propietario = forms.ModelChoiceField(
        label='Propietario',
        queryset=Propietario.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        })
    )

    departamento = forms.ModelChoiceField(
        label='Departamento',
        queryset=Departamento.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        })
    )

    jefe_entrega = forms.ModelChoiceField(
        label='Jefe que Entrega',
        queryset=JefeTic.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        })
    )

    responsable = forms.ModelChoiceField(
        label='Responsable',
        queryset=Funcionario.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        })
    )

    contrato = forms.ModelChoiceField(
        label='Contrato',
        queryset=Contrato.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        })
    )

    de_baja = forms.BooleanField(
        label='¿Equipo dado de baja?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    observaciones = forms.CharField(
        label='Observaciones',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
        required=False
    )

    motivo_baja = forms.CharField(
        label='Motivo de Baja',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
        required=False
    )

    class Meta:
        model = Computador
        fields = [
            'serie',
            'mac',
            'ip',
            'marca',
            'modelo',
            'tipo',
            'sistema_operativo',
            'microsoft_office',
            'propietario',
            'departamento',
            'jefe_entrega',
            'responsable',
            'contrato',
            'de_baja',
            'motivo_baja',
            'observaciones',
        ]
