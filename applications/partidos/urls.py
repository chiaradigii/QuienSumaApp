from django.urls import path
from .views import *

app_name = 'partidos_app'

urlpatterns = [
 path('crear-partido/', PartidoCreateView.as_view(), name='crear_partido'), 
 path('listar-partidos/', PartidoListView.as_view(), name='listar_partidos'),
 path('mis-partidos/', MisPartidosListView.as_view(), name='mis_partidos'),
 path('mi-partido/<pk>/', MiPartidoDetailView.as_view(), name='mi_partido'),
 path('unirse/<int:partido_id>/', unirse_partido, name='unirse_partido'),
 path('aceptar-solicitud/<int:solicitud_id>/', aceptar_solicitud, name='aceptar_solicitud'),
 path('rechazar-solicitud/<int:solicitud_id>/', rechazar_solicitud, name='rechazar_solicitud'),

]
