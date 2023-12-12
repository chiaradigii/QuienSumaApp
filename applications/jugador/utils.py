from geopy.geocoders import GoogleV3
from django.conf import settings

def obtener_geolocalizacion(direccion):
    geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
    location = geolocator.geocode(direccion)
    if location:
        return f"{location.longitude},{location.latitude}"
    return None
