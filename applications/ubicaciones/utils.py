from geopy.geocoders import GoogleV3
from django.conf import settings
from geopy.exc import GeocoderQueryError

def obtener_geolocalizacion(direccion):
    geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
    try:
        location = geolocator.geocode(direccion)
        if location:
            return f"{location.longitude},{location.latitude}"
    except GeocoderQueryError:
        print(f"An error occurred when trying to geocode the address: {direccion}")
    return None
