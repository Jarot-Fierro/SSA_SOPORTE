from django import forms
from django.core.exceptions import ValidationError

from establecimiento.models.establecimiento import Establecimiento
from users.models import Role, User


class FormUsuarioDpto(forms.ModelForm):

    def __init__(self, *args, establecimiento=None, request=None, **kwargs):
        self.establecimiento = establecimiento
        self.request = request
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='Nombre del Departamento',
        widget=forms.TextInput(attrs={
            'id': 'id_username',
            'class': 'form-control',
            'placeholder': 'Departamento',
        }),
        required=True
    )
    roles = forms.ModelChoiceField(
        label='Rol',
        empty_label='Seleccione un Rol',
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        required=True
    )
    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        empty_label='Selecciona un establecimiento',
        queryset=Establecimiento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if self.establecimiento:
            existe = User.objects.filter(username__iexact=username, establecimiento=self.establecimiento)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)

        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        # Verifica contraseñas
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        user = super().save(commit=False)

        # hasheo aquí
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'roles', 'password1', 'password2']
