from django import forms

from users.models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            'role_name',
            'mantenedores',
            'organizacion',

            'equipos',

            'usuarios',

            'soporte',

        ]

        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mantenedores': forms.Select(attrs={'class': 'form-control'}),

            'organizacion': forms.Select(attrs={'class': 'form-control'}),

            'equipos': forms.Select(attrs={'class': 'form-control'}),

            'usuarios': forms.Select(attrs={'class': 'form-control'}),
            'soporte': forms.Select(attrs={'class': 'form-control'}),
        }
