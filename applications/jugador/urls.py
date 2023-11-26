from django.urls import path
from . import views

app_name = 'jugador_app'

urlpatterns = [
    path('registro/', views.SignUpView.as_view(), name='registro'),
    path('registro-correcto/', views.JugadorRegistroCorrecto.as_view(), name='registro_correcto'),
    path('', views.HomeView.as_view(), name='home'),
]