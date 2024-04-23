from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.urls import reverse_lazy
from .models import Partido, PosicionCupo, SolicitudUnirse
from ..ubicaciones.models import Ubicacion
from .forms import PartidoForm
from django.views.generic import CreateView, ListView, DetailView
from datetime import datetime, timedelta, timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import messages


class PartidoCreateView(CreateView):
    """Vista para crear un nuevo partido"""
    model = Partido
    form_class = PartidoForm
    template_name = 'partidos/partido_form.html'
    success_url= reverse_lazy('partidos_app:listar_partidos')
    
    def form_valid(self, form):     
        cleaned_data = form.cleaned_data
        direccion = cleaned_data.get('direccion')
        fecha_hora = cleaned_data.get('fecha_hora')
        tipo_futbol=cleaned_data.get('tipo_futbol')
        gender=cleaned_data.get('gender') 
        ubicacion, _ = Ubicacion.objects.get_or_create(direccion=direccion)

        partido = form.save(commit=False)
        partido.tipo_futbol = tipo_futbol
        partido.fecha_hora = fecha_hora
        partido.creador = self.request.user
        partido.ubicacion = ubicacion
        partido.gender = gender
        partido.save()
        total_cupos = self.crear_posiciones_cupo(partido, cleaned_data)
        partido.cupos_disponibles = total_cupos
        partido.save()
        return super().form_valid(form)


    def crear_posiciones_cupo(self, partido, cleaned_data):
        total_cupos = 0
        for posicion in ['arqueros', 'defensas', 'medios', 'delanteros']:
            cupos = cleaned_data.get(posicion, 0)
            if cupos > 0:
                pos = PosicionCupo.objects.create(
                    partido=partido, 
                    posicion=posicion.capitalize()[:-1],  
                    cupos_totales=cupos,
                    cupos_ocupados=0 # Assume initial cupos_ocupados is 0
                )
                total_cupos += cupos
        return total_cupos

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
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super(PartidoListView,self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        partidos = Partido.objects.all().order_by('-fecha_hora')
        hoy = datetime.now(timezone.utc).date()
        context['partidos_hoy'] = partidos.filter(fecha_hora__date=hoy)
        context['partidos_manana'] = partidos.filter(fecha_hora__date=hoy + timedelta(days=1))
        context['partidos_semana'] = partidos.filter(fecha_hora__date__range=(hoy + timedelta(days=1), hoy + timedelta(days=7)))
        context['partidos_otros'] = partidos.exclude(fecha_hora__date__in=[hoy, hoy + timedelta(days=1)]).exclude(fecha_hora__date__range=(hoy, hoy + timedelta(days=7))).order_by('-fecha_hora')

        # Agregar información geográfica
        partidos_con_ubicacion = []
        for partido in context['partidos']:
            if partido.ubicacion and partido.ubicacion.geolocation:
                geolocation = partido.ubicacion.geolocation
                partidos_con_ubicacion.append({
                    'id': partido.id,
                    'nombre': str(partido),
                    'lat': geolocation.lat,
                    'lng': geolocation.lon,
                })
        context['partidos_con_ubicacion'] = partidos_con_ubicacion
 
 
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        date_filter = self.request.GET.get('date_filter')
        gender_filter = self.request.GET.get('gender')

        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_hora__date=filter_date)
            except ValueError:
                pass
        
        if gender_filter:  
            queryset = queryset.filter(gender=gender_filter)

        return queryset

class PartidoDetailView(LoginRequiredMixin,DetailView):
    template_name = 'partidos/detalle_partido.html'
    model = Partido

    context_object_name = "partido"
    def get_context_data(self, **kwargs):
        context = super(PartidoDetailView, self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context
    
class MisPartidosListView(LoginRequiredMixin,ListView):
    """Vista para listar los partidos creados por el usuario logueado"""
    model = Partido
    template_name = 'partidos/mis_partidos_list.html'
    context_object_name = 'mis_partidos'
    paginate_by = 10
    ordering = ['-fecha_hora']
    
    def get_queryset(self):
        return Partido.objects.filter(creador=self.request.user).order_by('-fecha_hora')

    def get_context_data(self, **kwargs):
        context = super(MisPartidosListView, self).get_context_data(**kwargs)
        partidos = context['mis_partidos']
        partidos_ids = partidos.values_list('id', flat=True)

        solicitudes = SolicitudUnirse.objects.filter(cupo__partido__id__in=partidos_ids).select_related('solicitante', 'cupo', 'cupo__partido')

        solicitudes_por_partido = {partido.id: [] for partido in partidos}
        for solicitud in solicitudes:
            solicitudes_por_partido[solicitud.cupo.partido.id].append(solicitud)

        context['solicitudes_por_partido'] = solicitudes_por_partido

        for partido in partidos:
            partido.solicitudes_pendientes = len(solicitudes_por_partido[partido.id])
            cupos_info = partido.posiciones_cupos.aggregate(
                total_cupos=models.Sum('cupos_totales'),
                ocupados_cupos=models.Sum('cupos_ocupados')
            )
            partido.cupos_disponibles = cupos_info['total_cupos'] - cupos_info['ocupados_cupos'] if cupos_info['total_cupos'] else 0

        return context

    
class MiPartidoDetailView(LoginRequiredMixin, DetailView):
    model = Partido
    template_name = 'partidos/mi_partido_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partido = context['partido']
        partido.solicitudes = SolicitudUnirse.objects.filter(cupo__partido=partido).select_related('solicitante')
        partido.jugadores_confirmados = partido.jugadores.all()
        return context

@login_required
def unirse_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    cupo = partido.posiciones_cupos.filter(cupos_ocupados__lt=models.F('cupos_totales')).first()
    if not cupo:
            messages.error(request, "No hay cupos disponibles.")
            return redirect('partidos_app:detalle_partido', pk=partido_id)

    # Check if there's already a pending or accepted solicitud
    if SolicitudUnirse.objects.filter(cupo=cupo, solicitante=request.user).exists():
        messages.error(request, "Ya has enviado una solicitud para este partido.")
    else:
        SolicitudUnirse.objects.create(cupo=cupo, solicitante=request.user)
        messages.success(request, "La solicitud se ha enviado correctamente.")

    return redirect('partidos_app:detalle_partido', pk=partido_id)
    
@login_required
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudUnirse, id=solicitud_id, partido__creador=request.user)
    try:
        solicitud.aceptar()  # Ensure this method handles all necessary logic
        messages.success(request, "Solicitud aceptada con éxito.")
    except ValidationError as e:
        messages.error(request, str(e))
    return redirect('partidos_app:detalle_partido', pk=solicitud.partido.id)


@login_required
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudUnirse, id=solicitud_id, partido__creador=request.user)
    solicitud.rechazar()  # This should handle setting the state and any other cleanup
    messages.info(request, "Solicitud rechazada.")
    return redirect('partidos_app:detalle_partido', pk=solicitud.partido.id)
