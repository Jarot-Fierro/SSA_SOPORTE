from django import forms

from core.validations import validate_exists
from equipo.models.impresora import JefeTic


class FormJefeTic(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'id': 'nombre_categoria',
                'class': 'form-control',
                'placeholder': 'Nombre de la Jefatura',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = JefeTic.objects.filter(nombre__iexact=nombre).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_exists(nombre, exists)
        return nombre

    class Meta:
        model = JefeTic
        fields = ['nombre']
