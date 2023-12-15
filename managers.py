from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    use_in_migrations = True

    def _create_user(self, user,nombre,apellido,fecha_nacimiento,sexo, correo, descripcion, posicion, foto, password, is_staff, is_superuser, **extra_fields):
        user = self.model(user=user,nombre=nombre,apellido=apellido,fecha_nacimiento=fecha_nacimiento,sexo=sexo, correo=correo, descripcion=descripcion, posicion=posicion, foto=foto, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, user,nombre,apellido,fecha_nacimiento,sexo, correo, descripcion, posicion, foto, password=None, **extra_fields):
        return self._create_user(user,nombre,apellido,fecha_nacimiento,sexo, correo, descripcion, posicion, foto, password, False, False, **extra_fields)
 
    def create_superuser(self, user, password=None, **extra_fields):
        extra_fields.setdefault('nombre', 'default_nombre')
        extra_fields.setdefault('apellido', 'default_apellido')
        extra_fields.setdefault('fecha_nacimiento', '2000-01-01')
        extra_fields.setdefault('sexo', 'default_sexo')
        extra_fields.setdefault('correo', 'default_correo@example.com')
        extra_fields.setdefault('descripcion', 'default_descripcion')
        extra_fields.setdefault('posicion', 'default_posicion')
        extra_fields.setdefault('foto', 'default_foto')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(user=user, password=password, **extra_fields)
