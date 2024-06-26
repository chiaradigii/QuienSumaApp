# Generated by Django 4.2.7 on 2024-01-31 20:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ubicaciones', '0001_initial'),
        ('auth', '0013_alter_group_id_alter_permission_id_alter_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user', models.CharField(default=' ', max_length=50, verbose_name='username')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=60, verbose_name='apellido')),
                ('fecha_nacimiento', models.DateField(default=datetime.date.today, verbose_name='fecha de nacimiento')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=50, verbose_name='sexo')),
                ('correo', models.EmailField(max_length=254, unique=True, verbose_name='correo')),
                ('posicion', models.CharField(choices=[('Arquero', 'Arquero'), ('Defensa', 'Defensa'), ('Medio', 'Medio'), ('Delantero', 'Delantero')], default='Medio', max_length=100, verbose_name='posicion')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos')),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('ubicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ubicaciones.ubicacion')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jugador.chatroom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
