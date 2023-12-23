from django.contrib import admin
from .models import Partido
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

admin.site.register(Partido)