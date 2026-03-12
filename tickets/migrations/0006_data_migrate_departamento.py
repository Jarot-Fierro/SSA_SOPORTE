from django.db import migrations


def migrate_departamento_alias_to_id(apps, schema_editor):
    Ticket = apps.get_model('tickets', 'Ticket')
    HistoricalTicket = apps.get_model('tickets', 'HistoricalTicket')
    Departamento = apps.get_model('establecimiento', 'Departamento')

    alias_map = {d.alias: d.id for d in Departamento.objects.all()}

    for ticket in Ticket.objects.all():
        if isinstance(ticket.departamento, str):
            dep_id = alias_map.get(ticket.departamento)
            if dep_id:
                ticket.departamento = str(dep_id)
                ticket.save()
            else:
                ticket.departamento = None
                ticket.save()

    for h_ticket in HistoricalTicket.objects.all():
        if isinstance(h_ticket.departamento, str):
            dep_id = alias_map.get(h_ticket.departamento)
            if dep_id:
                h_ticket.departamento = str(dep_id)
                h_ticket.save()
            else:
                # Si no hay match, le asignamos TIC por defecto (ID 1) para evitar fallos de NOT NULL
                h_ticket.departamento = "1"
                h_ticket.save()


def reverse_migrate_departamento_id_to_alias(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0005_historicalticket_solucion_ticket_solucion'),
        ('establecimiento', '0005_departamento_alias_historicaldepartamento_alias_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_departamento_alias_to_id, reverse_migrate_departamento_id_to_alias),
    ]
