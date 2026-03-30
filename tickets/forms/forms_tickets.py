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

    funcionario = forms.ModelChoiceField(
        label='Funcionario solicitante',
        queryset=Funcionario.objects.all(),
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
            'descripcion',
        ]
