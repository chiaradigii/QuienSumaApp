# Generated by Django 4.2.7 on 2024-04-23 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='cupos_disponibles',
            field=models.IntegerField(default=0),
        ),
    ]
