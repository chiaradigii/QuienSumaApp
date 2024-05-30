# applications/comunicaciones/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from applications.jugador.models import Jugador
from applications.comunicaciones.models import ChatSession, Message, Notification
from django.urls import reverse
from django.test import Client

import json
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from applications.comunicaciones.models import ChatSession, Message, Notification
from applications.jugador.models import Jugador
from web_project.asgi import application 

User = get_user_model()

""" tests for the models in the comunicaciones app """
class ChatSessionModelTest(TestCase):
    def setUp(self):
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.user2 = Jugador.objects.create_user(
            user='testuser2', nombre='Test', apellido='User2',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser2@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )

    def test_get_or_create_session(self):
        session, created = ChatSession.get_or_create_session(self.user1, self.user2)
        self.assertTrue(created)
        self.assertEqual(session.user1, self.user1)
        self.assertEqual(session.user2, self.user2)

        # Fetch the same session
        session, created = ChatSession.get_or_create_session(self.user1, self.user2)
        self.assertFalse(created)
        self.assertEqual(session.user1, self.user1)
        self.assertEqual(session.user2, self.user2)

class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.user2 = Jugador.objects.create_user(
            user='testuser2', nombre='Test', apellido='User2',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser2@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.chat_session, _ = ChatSession.get_or_create_session(self.user1, self.user2)

    def test_message_creation(self):
        message = Message.objects.create(chat_session=self.chat_session, sender=self.user1, message="Hello")
        self.assertEqual(message.chat_session, self.chat_session)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.message, "Hello")

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )

    def test_notification_creation(self):
        notification = Notification.objects.create(recipient=self.user1, message="Test notification")
        self.assertEqual(notification.recipient, self.user1)
        self.assertEqual(notification.message, "Test notification")
        self.assertFalse(notification.read)

    def test_notification_read_status(self):
        notification = Notification.objects.create(recipient=self.user1, message="Test notification")
        notification.read = True
        notification.save()
        self.assertTrue(notification.read)

""" tests for the views in the comunicaciones app """

class ChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.user2 = Jugador.objects.create_user(
            user='testuser2', nombre='Test', apellido='User2',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser2@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.client.login(username='testuser1', password='password')

    def test_start_chat(self):
        response = self.client.get(reverse('comunicaciones_app:startChat', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to chatPage
        chat_session = ChatSession.objects.get(user1=self.user1, user2=self.user2)
        self.assertRedirects(response, reverse('comunicaciones_app:chatPage', args=[chat_session.id]))

    def test_chatPage(self):
        chat_session, _ = ChatSession.get_or_create_session(self.user1, self.user2)
        response = self.client.get(reverse('comunicaciones_app:chatPage', args=[chat_session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comunicaciones/chatPage.html')

class NotificationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.client.login(username='testuser1', password='password')

    def test_fetch_notifications(self):
        Notification.objects.create(recipient=self.user1, message="Test notification")
        response = self.client.get(reverse('comunicaciones_app:fetch_notifications'))
        self.assertEqual(response.status_code, 200)
        notifications = response.json().get('notifications')
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]['message'], "Test notification")

    def test_mark_notification_read(self):
        notification = Notification.objects.create(recipient=self.user1, message="Test notification")
        response = self.client.post(reverse('comunicaciones_app:mark_notification_read'), {'notification_id': notification.id})
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.read)

""" Testing WebSocket Consumers"""

class ChatConsumerTest(TransactionTestCase):
    def setUp(self):
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.user2 = Jugador.objects.create_user(
            user='testuser2', nombre='Test', apellido='User2',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser2@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )
        self.chat_session, _ = ChatSession.get_or_create_session(self.user1, self.user2)
        self.room_name = f"chat_room_{self.chat_session.id}"

    async def test_connect(self):
        communicator = WebsocketCommunicator(application, f"/ws/chatPage/{self.chat_session.id}/")
        communicator.scope['user'] = self.user1
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_receive_message(self):
        communicator = WebsocketCommunicator(application, f"/ws/chatPage/{self.chat_session.id}/")
        communicator.scope['user'] = self.user1
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        message = {"message": "Hello"}
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], "Hello")

        await communicator.disconnect()

class NotificationConsumerTest(TransactionTestCase):
    def setUp(self):
        self.user1 = Jugador.objects.create_user(
            user='testuser1', nombre='Test', apellido='User1',
            fecha_nacimiento='1990-01-01', sexo='M',
            correo='testuser1@example.com', posicion='Medio', foto='default_foto',
            password='password'
        )

    async def test_connect(self):
        communicator = WebsocketCommunicator(application, f"/ws/notifications/")
        communicator.scope['user'] = self.user1
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_receive_notification(self):
        communicator = WebsocketCommunicator(application, f"/ws/notifications/")
        communicator.scope['user'] = self.user1
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Simulate sending a notification
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f"notifications_{self.user1.id}",
            {
                'type': 'send_notification',
                'message': "You have a new message",
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], "You have a new message")

        await communicator.disconnect()

if __name__ == "__main__":
    TestCase.main()
