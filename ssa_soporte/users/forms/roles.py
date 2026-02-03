from django import forms

from establecimiento.models.establecimiento import Establecimiento
from users.models import Role


class RoleForm(forms.ModelForm):
    establecimiento = forms.ModelChoiceField(
        queryset=Establecimiento.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Role
        fields = [
            'role_name',
            'mantenedores',

            'establecimientos',
            'organizacion',

            'plan',
            'chip',
            'celular',
            'computador',
            'toner',
            'impresora',

            'transacciones',
            'usuarios',

            'establecimiento',
        ]

        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mantenedores': forms.Select(attrs={'class': 'form-control'}),

            'establecimientos': forms.Select(attrs={'class': 'form-control'}),
            'organizacion': forms.Select(attrs={'class': 'form-control'}),

            'plan': forms.Select(attrs={'class': 'form-control'}),
            'chip': forms.Select(attrs={'class': 'form-control'}),
            'celular': forms.Select(attrs={'class': 'form-control'}),
            'computador': forms.Select(attrs={'class': 'form-control'}),
            'toner': forms.Select(attrs={'class': 'form-control'}),
            'impresora': forms.Select(attrs={'class': 'form-control'}),

            'transacciones': forms.Select(attrs={'class': 'form-control'}),
            'usuarios': forms.Select(attrs={'class': 'form-control'}),
        }
