# Generated by Django 4.2.7 on 2023-11-27 14:37

from django.db import migrations, models
from django.db.migrations import RunPython

def set_default_user(apps, schema_editor):
    Jugador = apps.get_model('jugador', 'Jugador')
    default_user = Jugador.objects.first()
    Jugador.objects.filter(user__isnull=True).update(user=default_user)


class Migration(migrations.Migration):

    dependencies = [
        ('jugador', '0005_remove_jugador_latitud_remove_jugador_longitud_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugador',
            name='nacionalidad',
        ),
        migrations.AlterField(
            model_name='jugador',
            name='posicion',
            field=models.CharField(choices=[('Arquero', 'Arquero'), ('Defensa', 'Defensa'), ('Medio', 'Medio'), ('Delantero', 'Delantero')], default='Medio', max_length=100, verbose_name='posicion'),
        ),
        RunPython(set_default_user),
    ]