from django.urls import path
from . import views

app_name = 'jugador_app'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
     path("Felicidades/",
     views.RegistroCorrecto.as_view(),
     name='registroCorrecto',
     ),
    path('jugadores-disponibles/',
    views.JugadorListView.as_view(),
    name='jugadores_disponibles',
    ),
    path('detalle-jugador/<pk>/',
    views.JugadorDetailView.as_view(),
    name='detalle_jugador',
    ),
]