from django.db import models

# Create your models here.
class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    posicion = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)