import logging
from geopy.geocoders import GoogleV3
from django.conf import settings
from geopy.exc import GeocoderQueryError

logger = logging.getLogger(__name__)

def obtener_geolocalizacion(direccion):
    geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
    try:
        location = geolocator.geocode(direccion)
        if location:
            return f"{location.latitude},{location.longitude}"
        else:
            logger.error(f"No se encontró la ubicación para la dirección: {direccion}")
    except GeocoderQueryError as e:
        logger.error(f"Ocurrió un error al intentar geolocalizar la dirección: {direccion}, Error: {e}")
    return None