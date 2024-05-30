"""La app Ubicaciones integrará la funcionalidad de Google Maps y manejaría las ubicaciones de los partidos."""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_google_maps import fields as map_fields
from .utils import obtener_geolocalizacion
from geopy.exc import GeocoderQueryError

class Ubicacion(models.Model):
    direccion = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.geolocation:
            print(f"Attempting to geolocate address: {self.direccion}")
            try:
                geolocation = obtener_geolocalizacion(self.direccion)
                if geolocation:
                    self.geolocation = geolocation
                else:
                    print(f"Geolocation not found for address: {self.direccion}")
            except GeocoderQueryError as e:
                print(f"Geolocation error for address: {self.direccion}, error: {e}")
        super(Ubicacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.direccion
    