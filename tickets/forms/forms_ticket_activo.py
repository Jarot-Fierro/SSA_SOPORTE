from django import forms
from django.contrib.contenttypes.models import ContentType

from equipo.models.celular import Celular
from equipo.models.equipos import Equipo
from tickets.models import TicketActivo


class FormTicketActivo(forms.ModelForm):
    tipo_equipo = forms.ChoiceField(
        label='Tipo de Equipo',
        choices=[
            ('computador', 'Computador'),
            ('impresora', 'Impresora'),
            ('celular', 'Celular'),
        ],
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    equipo_id = forms.ChoiceField(
        label='Equipo',
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = TicketActivo
        fields = ['observacion']
        widgets = {
            'observacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observación opcional'}),
        }

    def __init__(self, *args, **kwargs):
        self.ticket = kwargs.pop('ticket', None)
        super().__init__(*args, **kwargs)

        # Si tenemos un ticket, filtramos por el funcionario del ticket
        funcionario = self.ticket.funcionario if self.ticket else None

        # Opciones para el equipo_id basadas en el tipo_equipo seleccionado (o el inicial)
        tipo = self.data.get('tipo_equipo') or self.initial.get('tipo_equipo') or 'computador'
        self.fields['equipo_id'].choices = self.get_equipo_choices(tipo, funcionario)

    def get_equipo_choices(self, tipo, funcionario):
        choices = [('', '---------')]
        if tipo == 'computador':
            qs = Equipo.objects.filter(asignado=False)
            for item in qs:
                choices.append((item.id, f"PC: {item.serie} - {item.marca} {item.modelo or ''}"))
        elif tipo == 'impresora':
            qs = Equipo.objects.filter(asignado=False)
            for item in qs:
                choices.append((item.id, f"IMP: {item.serie} - {item.marca} {item.modelo or ''}"))
        elif tipo == 'celular':
            qs = Celular.objects.filter(asignado=False)
            for item in qs:
                choices.append((item.id, f"CEL: {item.numero_telefono} - {item.marca} {item.modelo or ''}"))
        return choices

    def clean(self):
        cleaned_data = super().clean()
        tipo_equipo = cleaned_data.get('tipo_equipo')
        equipo_id = cleaned_data.get('equipo_id')

        if tipo_equipo and equipo_id:
            model_map = {
                'equipo': Equipo,
                'celular': Celular,
            }
            model = model_map.get(tipo_equipo)
            try:
                cleaned_data['activo_obj'] = model.objects.get(id=equipo_id)
                cleaned_data['content_type'] = ContentType.objects.get_for_model(model)
            except model.DoesNotExist:
                raise forms.ValidationError("El equipo seleccionado no existe.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ticket = self.ticket
        instance.content_type = self.cleaned_data['content_type']
        instance.object_id = self.cleaned_data['equipo_id']
        if commit:
            instance.save()
        return instance
