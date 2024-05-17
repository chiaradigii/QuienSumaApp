# applications/comunicaciones/urls.py
from django.urls import path
from .views import chatPage,start_chat, mark_notification_read, fetch_notifications

app_name = 'comunicaciones_app'

urlpatterns = [
    path('chatPage/<int:chat_id>/', chatPage, name='chatPage'),
    path('startChat/<int:jugador_id>/', start_chat, name='startChat'),
    path('notifications/', fetch_notifications, name='fetch_notifications'),
    path('notifications/mark_read/', mark_notification_read, name='mark_notification_read')

]
