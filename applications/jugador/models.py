"""
La app jugador (users) Manejaría el registro, el perfil, 
y la autenticación de los usuarios. Incluiría modelos para el Usuario y la Autenticación
"""
from django.db import models
from datetime import date
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from managers import UserManager
from ..ubicaciones.models import Ubicacion

# Create your models here.
class Jugador(AbstractBaseUser,PermissionsMixin):
    objects = UserManager()
    posicion_choices = (
        ('Arquero', 'Arquero'),
        ('Defensa', 'Defensa'),
        ('Medio', 'Medio'),
        ('Delantero', 'Delantero'),
    )

    user = models.CharField("username", max_length=50, default=" ")
    nombre = models.CharField("nombre",max_length=50)
    apellido = models.CharField("apellido", max_length=60)
    fecha_nacimiento = models.DateField("fecha de nacimiento", auto_now=False, auto_now_add=False, default=date.today)
    sexo = models.CharField("sexo", max_length=50,choices=(('M', 'Masculino'), ('F', 'Femenino')), default='M')
    correo = models.EmailField("correo", max_length=254, unique=True, )
    posicion = models.CharField("posicion", max_length=100, choices=posicion_choices, default='Medio')
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    #address field and geolocation field
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'user'
    def save(self, *args, **kwargs):
        super(Jugador, self).save(*args, **kwargs)

    def calcular_años(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)
    
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content