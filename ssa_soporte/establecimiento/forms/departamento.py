from django import forms

from core.validations import validate_exists
from establecimiento.models.departamento import Departamento
from establecimiento.models.establecimiento import Establecimiento


class FormDepartamento(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre del Departamento',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_establecimiento',
                'class': 'form-control',
                'placeholder': 'Nombre del Establecimiento',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(
            attrs={
                'id': 'direccion_establecimiento',
                'class': 'form-control',
                'placeholder': 'Ohiggins 20',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=False
    )
    establecimiento = forms.ModelChoiceField(
        label="Establecimiento",
        empty_label="Selecciona una Establecimiento",
        queryset=Establecimiento.objects.filter(status=True),
        widget=forms.Select(
            attrs={
                'id': 'establecimiento_establecimiento',
                'class': 'form-control select2',
            }),
        required=True
    )

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Establecimiento.objects.filter(nombre__iexact=nombre).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_exists(nombre, exists)

        return nombre

    class Meta:
        model = Departamento
        fields = ['nombre', 'direccion', 'establecimiento']
