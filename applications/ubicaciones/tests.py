# applications/ubicaciones/tests.py

from django.test import TestCase
from unittest.mock import patch
from applications.ubicaciones.models import Ubicacion
from geopy.exc import GeocoderQueryError

class UbicacionModelTest(TestCase):
    @patch('applications.ubicaciones.models.obtener_geolocalizacion')
    def test_save_with_valid_address(self, mock_obtener_geolocalizacion):
        # Mocking a successful geolocation response
        mock_obtener_geolocalizacion.return_value = "40.712776,-74.005974"  # Coordinates for New York City

        ubicacion = Ubicacion.objects.create(direccion="New York, NY")
        self.assertAlmostEqual(float(ubicacion.geolocation.split(',')[0]), 40.712776, places=5)
        self.assertAlmostEqual(float(ubicacion.geolocation.split(',')[1]), -74.005974, places=5)
        mock_obtener_geolocalizacion.assert_called_once_with("New York, NY")

    @patch('applications.ubicaciones.models.obtener_geolocalizacion')
    def test_save_with_invalid_address(self, mock_obtener_geolocalizacion):
        # Mocking a failed geolocation response
        mock_obtener_geolocalizacion.return_value = None

        ubicacion = Ubicacion.objects.create(direccion="Invalid Address")
        self.assertIn(ubicacion.geolocation, [None, ''])
        mock_obtener_geolocalizacion.assert_called_once_with("Invalid Address")

    @patch('applications.ubicaciones.models.obtener_geolocalizacion')
    def test_save_with_existing_geolocation(self, mock_obtener_geolocalizacion):
        # When geolocation is already provided, obtener_geolocalizacion should not be called
        ubicacion = Ubicacion.objects.create(direccion="Existing Location", geolocation="34.052235,-118.243683")
        self.assertEqual(ubicacion.geolocation, "34.052235,-118.243683")
        mock_obtener_geolocalizacion.assert_not_called()

    @patch('applications.ubicaciones.models.obtener_geolocalizacion')
    def test_save_with_no_geolocation_and_exception(self, mock_obtener_geolocalizacion):
        # Mocking a geolocation request that raises an exception
        mock_obtener_geolocalizacion.side_effect = GeocoderQueryError("Test error")

        ubicacion = Ubicacion.objects.create(direccion="Exception Address")
        self.assertIn(ubicacion.geolocation, [None, ''])
        mock_obtener_geolocalizacion.assert_called_once_with("Exception Address")

if __name__ == "__main__":
    TestCase.main()
