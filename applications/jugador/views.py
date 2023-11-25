from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Jugador

class HomePageView(ListView):
    """Vista para mostrar la lista de jugadores"""
    model = Jugador
    template_name = 'jugador/home.html'
    context_object_name = 'jugadores'

class SignUpView(CreateView):
    """Vista para crear un nuevo jugador"""
    model = Jugador
    template_name = 'registration/signup.html'
    fields = ['nombre', 'apellido', 'edad', 'posicion', 'nacionalidad', 'foto']
    success_url = '/jugadores/registro-correcto'

class JugadorRegistroCorrecto(TemplateView):
    template_name = 'registration/jugador_registro_correcto.html'