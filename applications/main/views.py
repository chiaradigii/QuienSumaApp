from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View
)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'home/home.html'

class MainPageView(LoginRequiredMixin,TemplateView):
    """Vista que carga la pagina principal cuando alguien ya esta logueado"""
    template_name = "home/pagina_principal.html"
