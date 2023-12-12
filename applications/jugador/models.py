"""
La app jugador (users) Manejaría el registro, el perfil, 
y la autenticación de los usuarios. Incluiría modelos para el Usuario y la Autenticación
"""
from django.db import models
from datetime import date
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from .utils import obtener_geolocalizacion
from django_google_maps import fields as map_fields
from managers import UserManager

# Create your models here.
class Jugador(AbstractBaseUser,PermissionsMixin):
    objects = UserManager()
    posicion_choices = (
        ('Arquero', 'Arquero'),
        ('Defensa', 'Defensa'),
        ('Medio', 'Medio'),
        ('Delantero', 'Delantero'),
    )
    user = models.CharField("username", max_length=50, default="example")
    nombre = models.CharField("nombre",max_length=50)
    apellido = models.CharField("apellido", max_length=60)
    fecha_nacimiento = models.DateField("fecha de nacimiento", auto_now=False, auto_now_add=False, default=date.today)
    sexo = models.CharField("sexo", max_length=50,choices=(('M', 'Masculino'), ('F', 'Femenino')), default='M')
    correo = models.EmailField("correo", max_length=254, unique=True, default="example@gmail.com")
    descripcion = models.TextField("descripcion", blank=True, null=True)
    posicion = models.CharField("posicion", max_length=100, choices=posicion_choices, default='Medio')
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    #address field and geolocation field
    direccion = map_fields.AddressField(max_length=200,default="Calle 1 # 1-1")
    geolocation = map_fields.GeoLocationField(max_length=100, default="-74.806981,10.987807")
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'user'
    def save(self, *args, **kwargs):
        if not self.geolocation:
            if not self.geolocation:
                geolocation = obtener_geolocalizacion(self.direccion)
                if geolocation:
                    self.geolocation = geolocation
        super(Jugador, self).save(*args, **kwargs)

    def calcular_años(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)