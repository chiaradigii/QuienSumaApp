from django.urls import path
from . import views

app_name = 'futbolClubs_app'

urlpatterns = [
    path('geocode', views.geocode, name='geocode'),
    path('geocode/club/<int:pk>',views.geocode_club, name="geocode_club"),
]