from django.urls import path
from . import views

app_name = 'jugador_app'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.HomeView.as_view(), name='home'),
    path("pagina-principal/",
     views.MainPageView.as_view(),
     name='pagina_principal',
     ),
    path('login/', views.LoginView.as_view(), name='login'),
     path("Felicidades/",
     views.RegistroCorrecto.as_view(),
     name='registroCorrecto',
     ),
]