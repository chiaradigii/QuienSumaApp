# Generated by Django 5.0.4 on 2024-05-13 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jugador', '0002_remove_message_room_remove_message_sender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugador',
            name='user',
            field=models.CharField(default=' ', max_length=50, unique=True, verbose_name='username'),
        ),
    ]
