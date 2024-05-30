# applications/partidos/tests.py
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone
from applications.partidos.models import Partido, PosicionCupo, PartidoJugador, SolicitudUnirse
from applications.jugador.models import Jugador
from applications.ubicaciones.models import Ubicacion
from django.contrib.auth import get_user_model

User = get_user_model()

class PartidoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            user='testuser1',
            nombre='Test',
            apellido='User',
            fecha_nacimiento='1990-01-01',
            sexo='M',
            correo='testuser1@example.com',
            posicion='Medio',
            foto='default_foto',
            password='password'
        )
        self.ubicacion = Ubicacion.objects.create(direccion='Test Address', geolocation="0,0")

        self.partido = Partido.objects.create(
            tipo_futbol='7',
            fecha_hora=timezone.now() + timezone.timedelta(days=1),
            creador=self.user,
            ubicacion=self.ubicacion,
            gender='M'
        )
        self.posicion_cupo = PosicionCupo.objects.create(
            partido=self.partido,
            posicion='Medio',
            cupos_totales=5,
            cupos_ocupados=2
        )
        self.partido.update_cupos_disponibles()

    def test_update_cupos_disponibles(self):
        self.partido.update_cupos_disponibles()
        self.assertEqual(self.partido.cupos_disponibles, 3)

    def test_unirse(self):
        print(f"Before joining: {self.partido.cupos_disponibles}")
        self.partido.unirse(self.user)
        print(f"After joining: {self.partido.cupos_disponibles}")
        self.assertEqual(self.partido.cupos_disponibles, 2)
        self.assertTrue(PartidoJugador.objects.filter(partido=self.partido, jugador=self.user).exists())

    def test_abandonar(self):
        self.partido.unirse(self.user)
        print(f"Before leaving: {self.partido.cupos_disponibles}")
        self.partido.abandonar(self.user)
        print(f"After leaving: {self.partido.cupos_disponibles}")
        self.assertEqual(self.partido.cupos_disponibles, 3)
        self.assertFalse(PartidoJugador.objects.filter(partido=self.partido, jugador=self.user).exists())

    def test_aceptar_solicitud(self):
        solicitud = SolicitudUnirse.objects.create(cupo=self.posicion_cupo, solicitante=self.user)
        solicitud.aceptar()
        self.assertEqual(solicitud.estado, 'aceptado')
        self.assertEqual(self.posicion_cupo.cupos_ocupados, 3)

    def test_rechazar_solicitud(self):
        solicitud = SolicitudUnirse.objects.create(cupo=self.posicion_cupo, solicitante=self.user)
        solicitud.rechazar()
        self.assertEqual(solicitud.estado, 'rechazado')
    
    def tearDown(self):
        self.user.delete()
        self.ubicacion.delete()
        self.partido.delete()
        self.posicion_cupo.delete()


class PosicionCupoModelTest(TestCase):

    def setUp(self):
        self.jugador = Jugador.objects.create(
            user='testuser2', nombre='Test', apellido='User',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.ubicacion = Ubicacion.objects.create(direccion='Test Address',geolocation="0,0")

        self.partido = Partido.objects.create(
            tipo_futbol='7',
            fecha_hora=timezone.now() + timezone.timedelta(days=1),
            creador=self.jugador,
            ubicacion=self.ubicacion,
            gender='M'
        )
        self.posicion_cupo = PosicionCupo.objects.create(
            partido=self.partido,
            posicion='Medio',
            cupos_totales=5,
            cupos_ocupados=2
        )

    def test_str_method(self):
        self.assertEqual(str(self.posicion_cupo), 'Medio - Disponibles: 3')


class PartidoCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            user='testuser3',
            nombre='Test',
            apellido='User',
            fecha_nacimiento='1990-01-01',
            sexo='M',
            correo='testuser3@example.com',
            posicion='Medio',
            foto='default_foto',
            password='password'
        )
        self.client.login(username='testuser3', password='password')

    def test_get_create_partido(self):
        response = self.client.get(reverse_lazy('partidos_app:crear_partido'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partidos/partido_form.html')

    def test_post_create_partido(self):
        form_data = {
            'tipo_futbol': '7',
            'fecha_hora': '20-12-2025 20:00',
            'arqueros': 1,
            'defensas': 2,
            'medios': 3,
            'delanteros': 2,
            'gender': 'M',
            'direccion': 'Test Address'
        }
        response = self.client.post(reverse_lazy('partidos_app:crear_partido'), data=form_data)
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Partido.objects.exists())
    
    def tearDown(self):
        self.user.delete()

class PartidoListViewTest(TestCase):
    def setUp(self):
        self.jugador = Jugador.objects.create(
            user='testuser4', nombre='Test', apellido='User',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.ubicacion = Ubicacion.objects.create(direccion='Test Address', geolocation="0,0")

        self.partido = Partido.objects.create(
            tipo_futbol='7',
            fecha_hora=timezone.now() + timezone.timedelta(days=1),
            creador=self.jugador,
            ubicacion=self.ubicacion,
            gender='M'
        )

    def test_get_partido_list(self):
        response = self.client.get(reverse_lazy('partidos_app:listar_partidos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partidos/partido_list.html')
        self.assertContains(response, self.partido.tipo_futbol)

    def tearDown(self):
        self.jugador.delete()
        self.ubicacion.delete()
        self.partido.delete()

class MiPartidoDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            user='testuser5',
            nombre='Test',
            apellido='User',
            fecha_nacimiento='1990-01-01',
            sexo='M',
            correo='testuser5@example.com',
            posicion='Medio',
            foto='default_foto',
            password='password'
        )
        self.ubicacion = Ubicacion.objects.create(direccion='Test Address', geolocation="0,0")

        self.partido = Partido.objects.create(
            tipo_futbol='7',
            fecha_hora=timezone.now() + timezone.timedelta(days=1),
            creador=self.user,
            ubicacion=self.ubicacion,
            gender='M'
        )
        self.client.login(username='testuser5', password='password')

    def test_get_mi_partido_detail(self):
        response = self.client.get(reverse_lazy('partidos_app:mi_partido', kwargs={'pk': self.partido.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partidos/mi_partido_detalle.html')
        self.assertContains(response, self.partido.tipo_futbol)
    
    def tearDown(self):
        self.user.delete()
        self.ubicacion.delete()
        self.partido.delete()
