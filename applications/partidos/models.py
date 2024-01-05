"""La app partidos gestionara todo lo relacionado con la creación, visualización y gestión de partidos."""
from collections.abc import Iterable
from django.utils import timezone
from django.db import models
from django.conf import settings
from ..jugador.models import Jugador
from ..ubicaciones.models import Ubicacion


class PosicionCupo(models.Model):
    POSICIONES_NECESARIAS_CHOICES = (
        ('Arquero', 'Arquero'),
        ('Defensa', 'Defensa'),
        ('Medio', 'Medio'),
        ('Delantero', 'Delantero')
    )
    posicion = models.CharField(max_length=100, choices=POSICIONES_NECESARIAS_CHOICES)
    cupos = models.IntegerField(default=1)

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
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='creador',null=True, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True)
    posiciones = models.ForeignKey(PosicionCupo, on_delete=models.CASCADE,null=True, blank=True)
    jugadores = models.ManyToManyField(Jugador, through='PartidoJugador')
   
    def is_today(self):
        return self.fecha_hora.date() == timezone.now().date()
    
    def is_tomorrow(self): 
        return self.fecha_hora.date() == timezone.now().date() + timezone.timedelta(days=1)
    
    def is_this_week(self):
        return self.fecha_hora.date() >= timezone.now().date() and self.fecha_hora.date() <= timezone.now().date() + timezone.timedelta(days=7)

    def get_day_of_week(self):
        return self.fecha_hora.strftime('%A')

    def get_hora(self):
        return self.fecha_hora.strftime('%H:%M')

    def unirse(self, jugador):
        self.cupos_disponibles -= 1
        self.save()
        PartidoJugador.objects.create(partido=self, jugador=jugador)
    
    def abandonar(self, jugador):
        self.cupos_disponibles += 1
        self.save()
        PartidoJugador.objects.filter(partido=self, jugador=jugador).delete()

    def delete(self, *args, **kwargs):
        PartidoJugador.objects.filter(partido=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return '{} - {} - {}'.format(self.tipo_futbol, self.fecha_hora, self.ubicacion)

class PartidoJugador(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.SET_NULL, null=True, blank=True)
