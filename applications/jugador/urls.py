from django.urls import path
from . import views

app_name = 'jugador_app'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('jugadores-disponibles/',
    views.JugadorListView.as_view(),
    name='jugadores_disponibles',
    ),
    path('detalle-jugador/<pk>/',
    views.JugadorDetailView.as_view(),
    name='detalle_jugador',
    ),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('edit-password/', views.EditPasswordView.as_view(), name='edit_password'),
]