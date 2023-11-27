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
import googlemaps
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SingUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm



class SignUpView(CreateView):
    """Vista para crear un nuevo jugador"""
    model = Jugador
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Aquí puedes agregar la lógica para guardar los detalles del jugador, como la integración de Google Maps
            # Puedes acceder a los datos del formulario a través de form.cleaned_data
            return redirect('home/home.html')
        return render(request, self.template_name, {'form':form})
        
class MainPageView(LoginRequiredMixin,TemplateView):
    """Vista que carga la pagina principal cuando alguien ya esta logueado"""
    template_name = "pagina_principal.html"