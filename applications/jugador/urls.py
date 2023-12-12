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
]