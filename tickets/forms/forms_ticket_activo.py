from django import forms

from equipo.models.equipos import Equipo
from tickets.models import TicketActivo


class FormTicketActivo(forms.ModelForm):
    equipo = forms.ModelChoiceField(
        label='Equipo',
        queryset=Equipo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = TicketActivo
        fields = ['equipo', 'observacion']
        widgets = {
            'observacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observación opcional'}),
        }

    def __init__(self, *args, **kwargs):
        self.ticket = kwargs.pop('ticket', None)
        super().__init__(*args, **kwargs)

        # Filtrar equipos por establecimiento del ticket y que no estén dados de baja
        if self.ticket and self.ticket.establecimiento:
            # Obtener IDs de equipos ya asignados a este ticket
            equipos_asignados_ids = TicketActivo.objects.filter(ticket=self.ticket).values_list('equipo_id', flat=True)

            qs = Equipo.objects.filter(
                establecimiento=self.ticket.establecimiento,
                de_baja=False
            ).exclude(id__in=equipos_asignados_ids).select_related('ip', 'marca', 'modelo')

            self.fields['equipo'].queryset = qs

            # Personalizar la etiqueta de las opciones del select
            self.fields['equipo'].label_from_instance = lambda \
                    obj: f"{obj.ip.ip if obj.ip else 'S/IP'} - {obj.get_tipo_equipo_display()} - {obj.serie} - {obj.marca}"

    def clean_equipo(self):
        equipo = self.cleaned_data.get('equipo')
        if self.ticket and equipo:
            if TicketActivo.objects.filter(ticket=self.ticket, equipo=equipo).exists():
                raise forms.ValidationError("Este equipo ya está asignado a este ticket.")
        return equipo

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ticket = self.ticket
        if commit:
            instance.save()
        return instance
