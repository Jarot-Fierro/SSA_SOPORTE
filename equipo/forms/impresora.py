from django import forms

from catalogo.models import TipoImpresora, Marca, Modelo, Contrato, JefeTic, Propietario
from core.validations import validate_exists
from equipo.models.impresora import Impresora, Toner
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario


class FormImpresora(forms.ModelForm):
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

    hh = forms.CharField(
        label='HH',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese código HH',
            }
        ),
        required=False
    )

    ip = forms.CharField(
        label='Dirección IP',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 192.168.1.50',
            }
        ),
        required=False
    )

    tipo = forms.ModelChoiceField(
        label='Tipo de Impresora',
        queryset=TipoImpresora.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control select2'
            }
        )
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

    toner = forms.ModelChoiceField(
        label='Tóner / Tinta',
        queryset=Toner.objects.all(),
        required=True,
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

    def clean_serie(self):
        serie = self.cleaned_data['serie'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Impresora.objects.filter(serie__iexact=serie).exclude(
            pk=current_instance.pk if current_instance else None
        ).exists()

        validate_exists(serie, exists)
        return serie

    class Meta:
        model = Impresora
        fields = [
            'serie',
            'hh',
            'ip',
            'tipo',
            'marca',
            'modelo',
            'toner',
            'propietario',
            'departamento',
            'jefe_entrega',
            'responsable',
            'contrato',
            'de_baja',
            'motivo_baja',
            'observaciones',
        ]
