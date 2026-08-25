from django.db import migrations


def seed_empresa(apps, schema_editor):
    Servicio = apps.get_model('cc', 'Servicio')
    Servicio.objects.get_or_create(
        codigo='EMPRESA',
        defaults={
            'nombre': 'Banca Empresa',
            'descripcion': 'Información y gestión de clientes de banca empresarial.',
            'icono': 'BE',
        },
    )


def unseed_empresa(apps, schema_editor):
    Servicio = apps.get_model('cc', 'Servicio')
    Servicio.objects.filter(codigo='EMPRESA').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_empresa, unseed_empresa),
    ]
