# Urls de la app comunicaciones
from django.urls import path
from .views import chatPage,start_chat

app_name = 'comunicaciones_app'

urlpatterns = [
    path('chatPage/<int:chat_id>/', chatPage, name='chatPage'),
    path('startChat/<int:jugador_id>/', start_chat, name='startChat'),

]
