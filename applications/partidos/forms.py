import datetime
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Partido, PosicionCupo
from ..ubicaciones.models import Ubicacion
from ..ubicaciones.utils import obtener_geolocalizacion
from django.forms import inlineformset_factory

class PartidoForm(forms.ModelForm):
    """Formulario para crear un partido"""
    arqueros = forms.IntegerField(min_value=0, required=False, initial=0)
    defensas = forms.IntegerField(min_value=0, required=False, initial=0)
    medios = forms.IntegerField(min_value=0, required=False, initial=0)
    delanteros = forms.IntegerField(min_value=0, required=False, initial=0)
    
    fecha_hora = forms.DateTimeField(
    required=True,
    widget=forms.HiddenInput()
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
        exclude = ('ubicacion','creador')

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data['fecha_hora']
        if fecha_hora < datetime.datetime.now():
            raise forms.ValidationError('La fecha no puede ser anterior a la actual')
        return fecha_hora
    
    def clean(self):
        cleaned_data = super(PartidoForm, self).clean()
        direccion = cleaned_data.get('direccion')
        geolocation = obtener_geolocalizacion(direccion)
        if geolocation:
            ubicacion, created = Ubicacion.objects.update_or_create(
                direccion=direccion,
                defaults={'geolocation': geolocation} 
            )
            cleaned_data['ubicacion'] = ubicacion
        return cleaned_data
    
    def save(self, commit=True):
        return super(PartidoForm, self).save(commit=commit)
    
