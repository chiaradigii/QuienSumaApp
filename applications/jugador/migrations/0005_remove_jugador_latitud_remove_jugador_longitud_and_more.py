# Generated by Django 4.2.7 on 2023-11-27 13:40

from django.db import migrations, models
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jugador', '0004_jugador_latitud_jugador_longitud_jugador_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugador',
            name='latitud',
        ),
        migrations.RemoveField(
            model_name='jugador',
            name='longitud',
        ),
        migrations.AddField(
            model_name='jugador',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(default='-74.806981,10.987807', max_length=100),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='direccion',
            field=django_google_maps.fields.AddressField(default='Calle 1 # 1-1', max_length=200),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='user',
            field=models.CharField(default='example', max_length=50, verbose_name='username'),
        ),
    ]
