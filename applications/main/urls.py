
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path("pagina-principal/",
     views.MainPageView.as_view(),
     name='pagina_principal',
     ),
]
