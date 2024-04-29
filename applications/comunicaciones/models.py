from django.db import models
from django.contrib.auth import get_user_model
from applications.jugador.models import Jugador

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
