from django.urls import path
from . import views

app_name = 'jugador_app'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('registro/', views.SignUpView.as_view(), name='registro'),
    path('registro-correcto/', views.JugadorRegistroCorrecto.as_view(), name='registro_correcto'),
]