# Generated by Django 4.2.7 on 2023-12-22 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jugador', '0008_alter_jugador_managers_remove_jugador_direccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='correo',
            field=models.EmailField(max_length=254, unique=True, verbose_name='correo'),
        ),
    ]
