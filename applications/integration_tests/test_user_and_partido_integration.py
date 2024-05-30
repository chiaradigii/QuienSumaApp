# applications/integration_tests/test_user_and_partido_integration.py
from django.test import TestCase, Client
from django.urls import reverse
from applications.jugador.models import Jugador
from applications.partidos.models import Partido, PosicionCupo
from applications.ubicaciones.models import Ubicacion
from django.utils import timezone

class UserAndPartidoIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('jugador_app:signup')
        self.login_url = reverse('jugador_app:login')
        self.create_partido_url = reverse('partidos_app:crear_partido')

        # Create a user
        self.user_data = {
            'user': 'testuser_signup',
            'nombre': 'Test',
            'apellido': 'User',
            'fecha_nacimiento': '01-01-1990',
            'sexo': 'M',
            'correo': 'testuser_signup@example.com',
            'posicion': 'Medio',
            'password1': 'Password123',
            'password2': 'Password123',
            'direccion': 'Valid Address',
            'is_staff': False,
            'is_superuser': False
        }

        self.client.post(self.signup_url, self.user_data)
        self.client.post(self.login_url, {'username': 'testuser_signup', 'password': 'Password123'})

    def test_user_registration_and_partido_creation(self):
        # User is now logged in, create a partido
        partido_data = {
            'tipo_futbol': '7',
            'fecha_hora': (timezone.now() + timezone.timedelta(days=1)).strftime('%d-%m-%Y %H:%M'),
            'arqueros': 1,
            'defensas': 2,
            'medios': 3,
            'delanteros': 2,
            'gender': 'M',
            'direccion': 'Test Address'
        }
        response = self.client.post(self.create_partido_url, partido_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Partido.objects.exists())

        partido = Partido.objects.first()
        self.assertEqual(partido.creador.user, 'testuser_signup')
        self.assertEqual(partido.tipo_futbol, '7')
        self.assertEqual(partido.ubicacion.direccion, 'Test Address')
        self.assertEqual(partido.cupos_disponibles, 8)

if __name__ == "__main__":
    TestCase.main()
