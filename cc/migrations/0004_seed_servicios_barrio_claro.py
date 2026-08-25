from django.db import migrations


def seed(apps, schema_editor):
    Servicio = apps.get_model('cc', 'Servicio')
    Servicio.objects.get_or_create(
        codigo='BARRIO',
        defaults={
            'nombre': 'Banco del Barrio',
            'descripcion': 'Consulta de puntos, agentes y operaciones del Banco del Barrio.',
            'icono': 'BB',
        },
    )
    Servicio.objects.get_or_create(
        codigo='CLARO',
        defaults={
            'nombre': 'Claro',
            'descripcion': 'Convenios y servicios asociados al aliado Claro.',
            'icono': 'CL',
        },
    )


def unseed(apps, schema_editor):
    Servicio = apps.get_model('cc', 'Servicio')
    Servicio.objects.filter(codigo__in=['BARRIO', 'CLARO']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0003_alter_documento_archivo'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
