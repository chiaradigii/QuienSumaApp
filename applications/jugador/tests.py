# jugador/tests.py
from .models import Jugador
from datetime import date
from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

class JugadorModelTest(TestCase):

    def setUp(self):
        self.jugador = Jugador.objects.create(
            user='testuser',
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(1990, 1, 1),
            sexo='M',
            correo='testuser@example.com',
            posicion='Medio'
        )

    def test_jugador_creation(self):
        self.assertEqual(self.jugador.user, 'testuser')
        self.assertEqual(self.jugador.nombre, 'Test')
        self.assertEqual(self.jugador.apellido, 'User')
        self.assertEqual(self.jugador.fecha_nacimiento, date(1990, 1, 1))
        self.assertEqual(self.jugador.sexo, 'M')
        self.assertEqual(self.jugador.correo, 'testuser@example.com')
        self.assertEqual(self.jugador.posicion, 'Medio')

    def test_calcular_años(self):
        self.assertEqual(self.jugador.calcular_años(), timezone.now().year - 1990)

    def test_str_method(self):
        self.assertEqual(str(self.jugador), 'Test User')

    def tearDown(self):
        self.jugador.delete()

class SignUpViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('jugador_app:signup')  

    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_view_post_valid(self):
        form_data = {
            'user': 'testuser_signup',
            'nombre': 'Test',
            'apellido': 'User',
            'fecha_nacimiento': '01-01-1990', 
            'sexo': 'M',
            'correo': 'testuser_signup@example.com',
            'posicion': 'Medio',
            'password1': 'Password123',
            'password2': 'Password123', 
            'foto': 'default_foto',
            'direccion': 'Valid Address',  
            'is_staff': False,
            'is_superuser': False
        }
        response = self.client.post(self.url, form_data)
        
        if response.status_code == 400:
            print(response.json()) 

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})

    def test_signup_view_post_invalid(self):
        form_data = {
            'user': 'testuser_signup_invalid',
            'nombre': 'Test',
            'apellido': 'User',
            'fecha_nacimiento': '01-01-1990',  
            'sexo': 'M',
            'correo': 'testuser_signup_invalid@example.com',
            'posicion': 'Medio',
            'password1': 'Password123',
            'password2': 'differentpassword',
            'direccion': 'Plaza Olavide 3'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('jugador_app:login')
        self.user = User.objects.create_user(
            user='testuser_login',
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(1990, 1, 1),
            sexo='M',
            correo='testuser_login@example.com',
            posicion='Medio',
            foto='default_foto',
            password='Password123'
        )

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_valid(self):
        form_data = {
            'username': 'testuser_login', 
            'password': 'Password123',
        }
        response = self.client.post(reverse_lazy('jugador_app:login'), form_data)
        self.assertRedirects(response, reverse('main_app:pagina_principal'))

    def test_login_view_post_invalid(self):
        form_data = {
            'username': 'testuser_login',  
            'password': 'wrongpassword',
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def tearDown(self):
        self.user.delete()

class LogOutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('jugador_app:logout')
        self.user = User.objects.create_user(
            user='testuser_logout',
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(2000, 1, 1),
            sexo='M',
            correo='testuser_logout@example.com',
            posicion='Medio',
            foto='default_foto',
            password='Password123'
        )
        self.client.login(user='testuser_logout', password='Password123')

    def test_logout_view(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('main_app:home'))

    def tearDown(self):
        self.user.delete()

class JugadorListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('jugador_app:jugadores_disponibles')
        self.user = User.objects.create_user(
            user='testuser_list',
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(1990, 1, 1),
            sexo='M',
            correo='testuser_list@example.com',
            posicion='Medio',
            foto='default_foto',
            password='Password123'
        )
        self.client.login(user='testuser_list', password='Password123')

    def test_jugador_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jugador/jugadores_disponibles.html')
        self.assertContains(response, 'Jugadores Disponibles')

    def tearDown(self):
        self.user.delete()

class JugadorDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            user='testuser_detail',
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(1990, 1, 1),
            sexo='M',
            correo='testuser_detail@example.com',
            posicion='Medio',
            foto='default_foto',
            password='Password123'
        )
        self.jugador = Jugador.objects.create(
            user='testuser1_detail',
            nombre='Test',
            apellido='User',
            fecha_nacimiento=date(1990, 1, 1),
            sexo='M',
            correo='testuser1_detail@example.com',
            posicion='Medio',
            foto='default_foto',
        )
        self.url = reverse('jugador_app:detalle_jugador', kwargs={'pk': self.jugador.pk})
        self.client.login(user='testuser_detail', password='Password123')

    def test_jugador_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jugador/detalle_jugador.html')
        self.assertContains(response, 'Test User')

    def tearDown(self):
        self.user.delete()
        self.jugador.delete()

if __name__ == "__main__":
    TestCase.main()