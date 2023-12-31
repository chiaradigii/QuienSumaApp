# Generated by Django 4.2.7 on 2023-12-14 11:38

from django.db import migrations, models
import django.db.models.deletion
import managers


class Migration(migrations.Migration):

    dependencies = [
        ('ubicaciones', '0001_initial'),
        ('jugador', '0007_jugador_groups_jugador_is_staff_jugador_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='jugador',
            managers=[
                ('objects', managers.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='jugador',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='jugador',
            name='geolocation',
        ),
        migrations.AddField(
            model_name='jugador',
            name='ubicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ubicaciones.ubicacion'),
        ),
    ]
