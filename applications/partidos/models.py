"""La app partidos gestionara todo lo relacionado con la creación, visualización y gestión de partidos."""
from django.db import models
from django.conf import settings

from applications.ubicaciones.models import Ubicacion


class Partido(models.Model):
    """Modelo para la creación de partido"""
    TIPO_FUTBOL_CHOICES = (
        ('5', 'Futbol 5'),
        ('7', 'Futbol 7'),
        ('11', 'Futbol 11'),
    )
    tipo_futbol = models.CharField(max_length=2, choices=TIPO_FUTBOL_CHOICES, default='7')
    cupos_disponibles = models.IntegerField(default=0)
    fecha_hora = models.DateTimeField(auto_now=False, auto_now_add=False)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creador')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    
    def unirse(self, jugador):
        self.cupos_disponibles -= 1
        self.save()
        self.jugadores.add(jugador)


class PosicionCupo(models.Model):
    POSICIONES_NECESARIAS_CHOICES = (
        ('Arquero', 'Arquero'),
        ('Defensa', 'Defensa'),
        ('Medio', 'Medio'),
        ('Delantero', 'Delantero')
    )
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    posicion = models.CharField(max_length=100, choices=POSICIONES_NECESARIAS_CHOICES)
    cupos = models.IntegerField(default=1)