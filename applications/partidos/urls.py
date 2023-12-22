from django.urls import path
from .views import *

app_name = 'partidos_app'

urlpatterns = [
 path('crear-partido/', PartidoCreateView.as_view(), name='crear_partido'), 
 path('listar-partidos/', PartidoListView.as_view(), name='listar_partidos'),
 path('detalle-partido/<pk>/',
    PartidoDetailView.as_view(),
    name='detalle_partido',
    ),
]
