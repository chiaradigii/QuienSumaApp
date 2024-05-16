
# applications/comunicaciones/routing.py
from django.urls import path, include
from django.urls import re_path
from .consumer import NotificationConsumer, ChatConsumer

app_name = 'comunicaciones_app'

websocket_urlpatterns = [
    re_path(r'ws/chatPage/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]