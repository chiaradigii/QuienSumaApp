# Generated by Django 4.2.7 on 2024-04-22 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ubicaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_futbol', models.CharField(choices=[('5', 'Futbol 5'), ('7', 'Futbol 7'), ('11', 'Futbol 11')], default='7', max_length=2)),
                ('fecha_hora', models.DateTimeField()),
                ('gender', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('U', 'Mixto')], default='U', max_length=1)),
                ('creador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creador', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PosicionCupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion', models.CharField(choices=[('Arquero', 'Arquero'), ('Defensa', 'Defensa'), ('Medio', 'Medio'), ('Delantero', 'Delantero')], max_length=100)),
                ('cupos_totales', models.IntegerField(default=1)),
                ('cupos_ocupados', models.IntegerField(default=0)),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posiciones_cupos', to='partidos.partido')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudUnirse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=10)),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('cupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partidos.posicioncupo')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_partidos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartidoJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('partido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partidos.partido')),
            ],
        ),
        migrations.AddField(
            model_name='partido',
            name='jugadores',
            field=models.ManyToManyField(through='partidos.PartidoJugador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partido',
            name='ubicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ubicaciones.ubicacion'),
        ),
    ]
