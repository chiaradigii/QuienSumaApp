# applications/comunicaciones/models.py
from django.db import models
from django.contrib.auth import get_user_model
from applications.jugador.models import Jugador
from asgiref.sync import sync_to_async


User = get_user_model()

class ChatSession(models.Model):
    user1 = models.ForeignKey(Jugador, related_name='chat_sessions_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Jugador, related_name='chat_sessions_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_or_create_session(cls, user1, user2):
        if user1.id > user2.id:
            user1, user2 = user2, user1
        session, created = cls.objects.get_or_create(user1=user1, user2=user2)
        return session, created

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

class Notification(models.Model):
    recipient = models.ForeignKey(Jugador, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.recipient.user} - {'Read' if self.read else 'Unread'}"

def create_notification(recipient, message):
    try:
        Notification.objects.create(recipient=recipient, message=message)
    except Exception as e:
        print("Failed to create notification:", e)