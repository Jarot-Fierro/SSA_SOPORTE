from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from establecimiento.models.departamento import Departamento
from establecimiento.models.establecimiento import Establecimiento
from users.models import Role, User


class LoginFormDepto(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={
            'id': 'id_username',
            'class': 'form-control',
            'placeholder': 'Nombre de Usuario'
        }),
        required=True
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        required=True
    )

    error_messages = {
        'invalid_login': 'Nombre de usuario o contraseña incorrectos',
        'inactive': 'Este usuario se encuentra inactivo',
    }

    class Meta:
        model = User


class FormUsuarioDpto(forms.ModelForm):

    def __init__(self, *args, establecimiento=None, request=None, **kwargs):
        self.establecimiento = establecimiento
        self.request = request
        super().__init__(*args, **kwargs)

    username = forms.ModelChoiceField(
        label='Departamento',
        queryset=Departamento.objects.all(),
        empty_label='Seleccione un departamento',
        widget=forms.Select(attrs={
            'class': 'form-control select2'
        }),
        required=True
    )
    rol = forms.ModelChoiceField(
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
    usuario_soporte = forms.BooleanField(
        label='Usuario de Soporte',
        initial=True,
        required=False
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

        user.usuario_soporte = True
        # hasheo aquí
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'rol', 'password1', 'password2', 'usuario_soporte']


class FormUsuarioDptoUpdate(forms.ModelForm):

    def __init__(self, *args, establecimiento=None, request=None, **kwargs):
        self.establecimiento = establecimiento
        self.request = request
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='Departamento',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        required=True
    )
    rol = forms.ModelChoiceField(
        label='Rol',
        empty_label='Seleccione un Rol',
        queryset=Role.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    establecimiento = forms.ModelChoiceField(
        label='Establecimiento',
        empty_label='Selecciona un establecimiento',
        queryset=Establecimiento.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    usuario_soporte = forms.BooleanField(
        label='Usuario de Soporte',
        initial=True,
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if self.establecimiento:
            existe = User.objects.filter(username__iexact=username, establecimiento=self.establecimiento)
            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)

        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        user.usuario_soporte = True

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'rol', 'establecimiento', 'usuario_soporte']
