from django import forms
from django.core.exceptions import ValidationError

from core.validations import validate_rut, format_rut, validate_spaces, validate_email
from establecimiento.models.departamento import Departamento
from establecimiento.models.funcionario import Funcionario


class FormFuncionario(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Capturamos request para usar el establecimiento del usuario
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    rut = forms.CharField(
        label='R.U.T.',
        widget=forms.TextInput(attrs={
            'class': 'form-control id_rut',
            'placeholder': 'Ingrese el RUT del profesional',
        }),
        required=True
    )

    nombres = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del profesional',
            'id': 'nombres_profesional'
        }),
        required=True
    )

    correo = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.cl',
            'id': 'correo_profesional'
        }),
        required=False
    )

    jefatura = forms.BooleanField(
        label='¿Es Jefatura?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mx-5'})
    )

    departamento = forms.ModelChoiceField(
        required=True,
        label='Departamento',
        queryset=Departamento.objects.filter(status=True),
        empty_label='Seleccione un Departamento',
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            return rut

        rut = rut.strip()

        # Validar que no contenga espacios
        if " " in rut:
            raise ValidationError("El RUT no debe contener espacios.")

        rut_sin_formato = rut.replace(".", "").replace("-", "").upper()

        if not validate_rut(rut_sin_formato):
            raise ValidationError("El RUT ingresado no es válido.")

        # Si ya existe otro profesional con el mismo RUT
        if Funcionario.objects.filter(rut=format_rut(rut_sin_formato)).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un funcionario con este RUT.")

        return format_rut(rut_sin_formato)

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres', '').strip()

        validate_spaces(nombres)
        return nombres

    def clean_correo(self):
        correo = self.cleaned_data.get('correo', '').strip()
        validate_email(correo)

        # Evitar correos duplicados
        if Funcionario.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un funcionario con este correo electrónico.")
        return correo

    class Meta:
        model = Funcionario
        fields = [
            'rut',
            'nombres',
            'correo',
            'departamento',
            'jefatura',
        ]
