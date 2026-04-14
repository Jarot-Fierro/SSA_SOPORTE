from django import forms

from establecimiento.models.funcionario import Funcionario
from tickets.models import Ticket


class FormTicket(forms.ModelForm):
    titulo = forms.CharField(
        label='Título del problema',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Problema con impresora'
        }),
        required=True
    )

    descripcion = forms.CharField(
        label='Descripción del problema',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa el problema que está presentando'
        }),
        required=False
    )

    area_soporte = forms.ChoiceField(
        label='Área de soporte',
        choices=[('Mantencion', 'Mantencion'), ('Informatica', 'Informatica')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=True
    )

    funcionario = forms.ModelChoiceField(
        label='Funcionario solicitante',
        queryset=Funcionario.objects.filter(),
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        }),
        required=True
    )

    class Meta:
        model = Ticket
        fields = [
            'titulo',
            'funcionario',
            'area_soporte',
            'descripcion',
        ]
