from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse_lazy
from .models import Partido, PosicionCupo
from ..ubicaciones.models import Ubicacion
from .forms import PartidoForm
from django.views.generic import CreateView, ListView, DetailView
from datetime import datetime, timedelta, timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

class PartidoCreateView(CreateView):
    """Vista para crear un nuevo partido"""
    model = Partido
    form_class = PartidoForm
    template_name = 'partidos/partido_form.html'
    success_url= reverse_lazy('partidos_app:listar_partidos')

    def form_valid(self, form):     
        cleaned_data = form.cleaned_data
        direccion = cleaned_data.get('direccion')
        cupos = sum([
            form.cleaned_data.get('arqueros', 0),
            form.cleaned_data.get('defensas', 0),
            form.cleaned_data.get('medios', 0),
            form.cleaned_data.get('delanteros', 0)
        ])
        fecha_hora = cleaned_data.get('fecha_hora')
        tipo_futbol=cleaned_data.get('tipo_futbol')
        gender=cleaned_data.get('gender') 
        ubicacion, _ = Ubicacion.objects.get_or_create(direccion=direccion)

        partido = form.save(commit=False)
        partido.tipo_futbol = tipo_futbol
        partido.fecha_hora = fecha_hora
        partido.creador = self.request.user
        partido.ubicacion = ubicacion
        partido.cupos_disponibles = cupos
        partido.gender = gender
        partido.save()
        posiciones = self.crear_posiciones_cupo(partido, cleaned_data)
        partido.posiciones = posiciones
        return super().form_valid(form)


    def crear_posiciones_cupo(self, partido, cleaned_data):
        for posicion in ['arqueros', 'defensas', 'medios', 'delanteros']:
            cupos = cleaned_data.get(posicion, 0)
            if cupos > 0:
                pos = PosicionCupo.objects.create(
                    partido=partido, 
                    posicion=posicion.capitalize()[:-1],  
                    cupos=cupos
                )
        return pos

    def form_invalid(self, form):
        errors = form.errors.as_data()
        for field, error_list in errors.items():
            for error in error_list:
                print(f"Error in field '{field}': {error}")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super(PartidoCreateView,self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class PartidoListView(ListView):
    """Vista para listar los partidos"""
    model = Partido
    template_name = 'partidos/partido_list.html'
    context_object_name = 'partidos'
    paginate_by = 10
    ordering = ['-fecha_hora']
    
    def get_context_data(self, **kwargs):
        context = super(PartidoListView,self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        partidos = Partido.objects.all().order_by('-fecha_hora')
        hoy = datetime.now(timezone.utc).date()
        context['partidos_hoy'] = partidos.filter(fecha_hora__date=hoy)
        context['partidos_manana'] = partidos.filter(fecha_hora__date=hoy + timedelta(days=1))
        context['partidos_semana'] = partidos.filter(fecha_hora__date__range=(hoy + timedelta(days=1), hoy + timedelta(days=7)))
        context['partidos_otros'] = partidos.exclude(fecha_hora__date__in=[hoy, hoy + timedelta(days=1)]).exclude(fecha_hora__date__range=(hoy, hoy + timedelta(days=7))).order_by('-fecha_hora')
        context['partidos'] = [
            {
                'partido': partido,
                'jugadores': partido.jugadores.all()  # get queryset iterable
            }
            for
             partido in context['partidos']
        ]
        
        return context

class PartidoDetailView(LoginRequiredMixin,DetailView):
    template_name = 'partidos/detalle_partido.html'
    model = Partido
    context_object_name = "partido"
    def get_context_data(self, **kwargs):
        context = super(PartidoDetailView, self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context