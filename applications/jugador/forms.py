# forms.py

from django import forms
from django_google_maps import fields as map_fields
from geopy.geocoders import GoogleV3
from .models import Jugador

class SignUpForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña'
            }
        )
    )
    class Meta:
        model = Jugador
        fields = ('user', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'correo', 'descripcion', 'posicion', 'foto', 'direccion')
        exclude = ['geolocation', 'is_staff', 'is_superuser']


    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden')

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 8:
            self.add_error('password1', 'La contraseña debe tener al menos 8 caracteres')
        # check for number
        if not any(char.isdigit() for char in password):
            self.add_error('password1', 'La contraseña debe tener al menos un número')
        # check for letter
        if not any(char.isalpha() for char in password):
            self.add_error('password1', 'La contraseña debe tener al menos una letra')
        # check for uppercase letter
        if not any(char.isupper() for char in password):
            self.add_error('password1', 'La contraseña debe tener al menos una letra mayúscula')
        # check for lowercase letter
        if not any(char.islower() for char in password):
            self.add_error('password1', 'La contraseña debe tener al menos una letra minúscula')
        return password


    def clean(self):
        cleaned_data = super().clean()

        # Use Google Maps Geocoding API to get geolocation from the provided address
        geolocator = GoogleV3(api_key='AIzaSyCEgenBDBqhvJzkyU-wy4TqW6RTRfti-74')
        location = geolocator.geocode(cleaned_data.get('direccion'))

        if location:
            cleaned_data['geolocation'] = f"{location.longitude},{location.latitude}"

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
class LoginForm(forms.Form):
    user = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Usuario'
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }
        ))
    # validation
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user = self.cleaned_data['user']
        password = self.cleaned_data['password']
        if not authenticate(user=user, password=password):
            raise forms.ValidationError('Los datos del usuario no son correctos')
        return self.cleaned_data

class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña'
            }
        )
    )