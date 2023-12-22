import datetime
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Partido, PosicionCupo
from ..ubicaciones.models import Ubicacion
from ..ubicaciones.utils import obtener_geolocalizacion
from django.utils import timezone

class PartidoForm(forms.ModelForm):
    """Formulario para crear un partido"""
    arqueros = forms.IntegerField(min_value=0, required=False, initial=0, label='Arqueros a convocar')
    defensas = forms.IntegerField(min_value=0, required=False, initial=0, label='Defensas a convocar')
    medios = forms.IntegerField(min_value=0, required=False, initial=0, label='Medios a convocar')
    delanteros = forms.IntegerField(min_value=0, required=False, initial=0, label='Delanteros a convocar')
    
    fecha_hora = forms.DateTimeField(
    required=True,
    input_formats=['%d-%m-%Y %H:%M'],  
    widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Fecha y hora'
        },
        format='%d-%m-%Y %H:%M'  
    )
)
    direccion = forms.CharField(
        label='Dirección',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }
        )
    )
    class Meta:
        model = Partido
        fields = ['tipo_futbol', 'fecha_hora', 'direccion', 'arqueros', 'defensas', 'medios', 'delanteros']
        exclude = ('ubicacion','creador','geolocation')

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data['fecha_hora']
        now = timezone.now()
        if fecha_hora < now:
            raise forms.ValidationError('La fecha no puede ser anterior a la actual')
        return fecha_hora


    def clean(self):
        cleaned_data = super().clean()
        direccion = cleaned_data.get('direccion')
        geolocation = obtener_geolocalizacion(direccion)
        if geolocation:
            Ubicacion.objects.update_or_create(
                direccion=direccion,
                defaults={'geolocation': geolocation} 
            )
        return cleaned_data
    
    def save(self, commit=True):
        partido = super().save(commit=False)
        if commit:
            partido.save()
            PosicionCupo.objects.create(partido=partido, posicion='ARQUERO', cupos=self.cleaned_data['arqueros'])
            PosicionCupo.objects.create(partido=partido, posicion='DEFENSA', cupos=self.cleaned_data['defensas'])
            PosicionCupo.objects.create(partido=partido, posicion='MEDIO', cupos=self.cleaned_data['medios'])
            PosicionCupo.objects.create(partido=partido, posicion='DELANTERO', cupos=self.cleaned_data['delanteros'])
        return partido
    
