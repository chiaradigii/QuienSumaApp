from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse_lazy
from .models import Partido, PosicionCupo
from ..ubicaciones.utils import obtener_geolocalizacion
from ..ubicaciones.models import Ubicacion
from .forms import PartidoForm
from django.views.generic import CreateView, ListView

class PartidoCreateView(CreateView):
    """Vista para crear un nuevo partido"""
    model = Partido
    form_class = PartidoForm
    template_name = 'partidos/partido_form.html'
    success_url= reverse_lazy('partidos_app:listar_partidos')

    def get_context_data(self, **kwargs):
        context = super(PartidoCreateView, self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context
    
    def form_valid(self, form):
        # Save the object Partido
        partido = form.save(commit=False)
        direccion = form.cleaned_data.get('direccion')
        geolocation = obtener_geolocalizacion(direccion)
        ubicacion, created = Ubicacion.objects.update_or_create(
        direccion=direccion,
        defaults={'geolocation': geolocation} if geolocation else {}
            )
        partido.ubicacion = ubicacion
        partido.cupos_disponibles = sum([
            form.cleaned_data.get('arqueros', 0),
            form.cleaned_data.get('defensas', 0),
            form.cleaned_data.get('medios', 0),
            form.cleaned_data.get('delanteros', 0)
        ])
        partido.save()

        self.crear_posiciones_cupo(partido, form.cleaned_data)
        return redirect(self.get_success_url())


    def crear_posiciones_cupo(self, partido, cleaned_data):
        for posicion in ['arqueros', 'defensas', 'medios', 'delanteros']:
            cupos = cleaned_data.get(posicion, 0)
            if cupos > 0:
                PosicionCupo.objects.create(
                    partido=partido, 
                    posicion=posicion.capitalize()[:-1],  # Esto convertirá, por ejemplo, 'arqueros' en 'Arquero'
                    cupos=cupos
                )

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    


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
        return context