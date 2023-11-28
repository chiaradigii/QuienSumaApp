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
from .models import Jugador
import googlemaps
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from .forms import SignUpForm, LoginForm, PasswordChangeForm
from django.urls import reverse_lazy
import os
from geopy.geocoders import GoogleV3
from django.http import HttpResponseRedirect

class HomeView(TemplateView):
    template_name = 'home/home.html'
    

class SignUpView(FormView):
    """Vista para crear un nuevo jugador"""
    model = Jugador
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url= reverse_lazy('jugador_app:home')

    def form_valid(self, form):
        user = Jugador.objects.create_user(
            user=form.cleaned_data['user'],
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
            fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
            sexo=form.cleaned_data['sexo'],
            correo=form.cleaned_data['correo'],
            descripcion=form.cleaned_data['descripcion'],
            posicion=form.cleaned_data['posicion'],
            foto=form.cleaned_data['foto'],
            direccion=form.cleaned_data['direccion'],
            geolocation=form.cleaned_data['geolocation'],
            password=form.cleaned_data['password1']
        )
        return super(SignUpView,self).form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = os.environ.get('GOOGLE_API_KEY', '')
        return context

class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm 
    success_url = reverse_lazy('jugador_app:pagina_principal')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginView,self).form_valid(form)


class MainPageView(LoginRequiredMixin,TemplateView):
    """Vista que carga la pagina principal cuando alguien ya esta logueado"""
    template_name = "home/pagina_principal.html"


class RegistroCorrecto(TemplateView):
    template_name = "jugador/registro_correcto.html"

class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home/home.html'))

class UpdatePasswordView(FormView):
    template_name = 'registration/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('registration/login.html')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.user,
            password=usuario.password
        )
        if user:
            user.set_password(form.cleaned_data['password1'])
            user.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
    