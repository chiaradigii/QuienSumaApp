# applications/partidos/models.py
from collections.abc import Iterable
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.conf import settings
from ..jugador.models import Jugador
from ..ubicaciones.models import Ubicacion
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format

class PosicionCupo(models.Model):
    POSICIONES_NECESARIAS_CHOICES = (
        ('Arquero', 'Arquero'),
        ('Defensa', 'Defensa'),
        ('Medio', 'Medio'),
        ('Delantero', 'Delantero')
    )
    partido = models.ForeignKey(
        'Partido', 
        related_name='posiciones_cupos',  
        on_delete=models.CASCADE
    )
    posicion = models.CharField(max_length=100, choices=POSICIONES_NECESARIAS_CHOICES)
    cupos_totales = models.IntegerField(default=1)
    cupos_ocupados = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.partido.update_cupos_disponibles()

    def __str__(self):
        return f"{self.get_posicion_display()} - Disponibles: {self.cupos_totales - self.cupos_ocupados}"

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
    jugadores = models.ManyToManyField(Jugador, through='PartidoJugador')
    gender = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino'),('U', 'Mixto')), default='U')
    
    def update_cupos_disponibles(self):
        total_cupos = sum(pos.cupos_totales - pos.cupos_ocupados for pos in self.posiciones_cupos.all())
        self.cupos_disponibles = total_cupos
        self.save()
    
    def get_lugar(self):
        ubicacion_parts = self.ubicacion.direccion.split(',')
        return ubicacion_parts[0].strip()
        
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
        if self.cupos_disponibles <= 0:
            raise ValidationError("No hay cupos disponibles para unirse a este partido.")
        self.cupos_disponibles -= 1
        self.save()
        PartidoJugador.objects.create(partido=self, jugador=jugador)
        for posicion_cupo in self.posiciones_cupos.all():
            if posicion_cupo.cupos_ocupados < posicion_cupo.cupos_totales:
                posicion_cupo.cupos_ocupados += 1
                posicion_cupo.save()
                break
        self.update_cupos_disponibles()
    
    def abandonar(self, jugador):
        if not PartidoJugador.objects.filter(partido=self, jugador=jugador).exists():
            raise ValidationError("El jugador no está en este partido.")
        for posicion_cupo in self.posiciones_cupos.all():
            if posicion_cupo.cupos_ocupados > 0:
                posicion_cupo.cupos_ocupados -= 1
                posicion_cupo.save()
                break
        PartidoJugador.objects.filter(partido=self, jugador=jugador).delete()
        self.update_cupos_disponibles()

    def delete(self, *args, **kwargs):
        PartidoJugador.objects.filter(partido=self).delete()
        super().delete(*args, **kwargs)
    
    @classmethod
    def eliminar_partidos_anteriores(cls):
        hoy = timezone.now()
        cls.objects.filter(fecha_hora__lt=hoy).delete()

    def __str__(self):
        return f"{self.tipo_futbol} - {self.get_lugar()} - {date_format(self.fecha_hora, 'DATE_FORMAT')}"

class PartidoJugador(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.SET_NULL, null=True, blank=True)
    posicion = models.CharField(max_length=100)  

class SolicitudUnirse(models.Model):
    """ 
    Modelo para la solicitud de un jugador para unirse a un partido
    """
    cupo = models.ForeignKey(PosicionCupo, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="solicitudes_partidos")
    estado = models.CharField(max_length=10, choices=(('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')), default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    @property
    def partido(self):
        return self.cupo.partido
    
    def get_Solicitudes(self):
        return self.partido.solicitudes.all()

    def solicitudesPendientes(self):    
        return self.partido.solicitudes.filter(estado='pendiente')

    def aceptar(self):
        if self.cupo.cupos_ocupados >= self.cupo.cupos_totales:
            raise ValidationError("No hay cupos disponibles para esta posición.")
        self.estado = 'aceptado'
        self.cupo.cupos_ocupados += 1
        self.cupo.save()
        self.save()
        self.partido.update_cupos_disponibles()
    
    def rechazar(self):
        self.estado = 'rechazado'
        self.save()
        self.partido.update_cupos_disponibles()
    
    def __str__(self):
            return f"{self.solicitante.user} - {self.cupo.partido} - {self.cupo.posicion} - {self.estado}"
