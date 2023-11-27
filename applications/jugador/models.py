from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Jugador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nombre = models.CharField("nombre",max_length=50)
    apellido = models.CharField("apellido", max_length=60)
    fecha_nacimiento = models.DateField("fecha de nacimiento", auto_now=False, auto_now_add=False, default=date.today)
    sexo = models.CharField("sexo", max_length=50,choices=(('M', 'Masculino'), ('F', 'Femenino')), default='M')
    direccion = models.CharField("direccion", max_length=255, blank=True, null=True)
    correo = models.EmailField("correo", max_length=254, unique=True, default="example@gmail.com")
    descripcion = models.TextField("descripcion", blank=True, null=True)
    posicion = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            geocode_result = geolocator.geocode(self.direccion)
            if geocode_result:
                self.latitude = geocode_result.latitude
                self.longitude = geocode_result.longitude
        super(Jugador, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)