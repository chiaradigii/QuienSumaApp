# Generated by Django 4.2.7 on 2023-12-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jugador', '0009_alter_jugador_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='correo',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='correo'),
        ),
    ]
