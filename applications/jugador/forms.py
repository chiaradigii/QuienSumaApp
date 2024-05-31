from datetime import datetime
from django import forms
from .models import Jugador
from .widgets import DatePickerInput 
from django.contrib.auth import authenticate
from applications.ubicaciones.models import Ubicacion
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model

class SignUpForm(forms.ModelForm):

    SEXO_CHOICES = [
        ('M', 'Maculino'),
        ('F', 'Femenino'),
    ]
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

    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento',
        required=True,
        input_formats=['%d-%m-%Y'], 
        widget=DatePickerInput()
    )

    sexo = forms.ChoiceField(
        label='sexo',
        choices=SEXO_CHOICES,
        widget=forms.RadioSelect,
        initial='M',
    )
    
    correo = forms.EmailField(
        error_messages={
            'invalid': 'Ingresa un correo valido (ejemplo@dominio.com)',
        }
    )

    class Meta:
        model = Jugador
        fields = ('user', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'correo', 'posicion', 'foto','direccion', 'password1', 'password2')
        exclude = ['geolocation', 'is_staff', 'is_superuser']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')
        return password2

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('La contraseña debe tener al menos un número.')
        if not any(char.isalpha() for char in password):
            raise ValidationError('La contraseña debe tener al menos una letra.')
        if not any(char.isupper() for char in password):
            raise ValidationError('La contraseña debe tener al menos una letra mayúscula.')
        if not any(char.islower() for char in password):
            raise ValidationError('La contraseña debe tener al menos una letra minúscula.')
        elif not password:
            raise ValidationError('La contraseña es obligatoria.')
        return password
    
    from datetime import datetime

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento.year > datetime.today().year - 18:
            raise ValidationError('Debes ser mayor de 18 años para registrarte.')
        elif fecha_nacimiento.year < 1900 or fecha_nacimiento.year > datetime.today().year:
            raise ValidationError('Fecha de nacimiento inválida.')
        elif not fecha_nacimiento:
            raise ValidationError('La fecha de nacimiento es obligatoria.')
        return fecha_nacimiento

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        print("Validating email:", correo)
        validator = EmailValidator()
        try:
            validator(correo)
        except forms.ValidationError:
            print("Invalid email:", correo)  
            raise ValidationError('Ingresa un correo valido (ejemplo@dominio.com)')
        if not correo:
            raise ValidationError('El correo es obligatorio.')
        return correo

        
    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['user', 'nombre', 'apellido']
        for field in required_fields:
            if not cleaned_data.get(field):
                raise ValidationError(f'El campo {field} es obligatorio')
        return cleaned_data
    

class LoginForm(forms.Form):
    username = forms.CharField(
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
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Las credenciales son incorrectas')
        return cleaned_data

from django.core.exceptions import ValidationError

class EditProfileForm(forms.ModelForm):
    direccion = forms.CharField(
        required=False,
        label='Dirección',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_direccion', 'placeholder': 'Nueva dirección'})
    )
    
    posicion = forms.ChoiceField(
        required=False,
        label='Posición',
        choices=Jugador.posicion_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    foto = forms.ImageField(
        required=False,
        label='Foto',
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Jugador
        fields = ['posicion', 'direccion', 'foto']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        jugador = super().save(commit=False)
        direccion = self.cleaned_data.get('direccion')
        foto = self.cleaned_data.get('foto')
        
        if commit:
            if direccion and jugador.ubicacion:
                # Update existing Ubicacion
                ubicacion = jugador.ubicacion
                ubicacion.direccion = direccion
                ubicacion.save()
            elif direccion:
                # Create new Ubicacion instance if not exists
                ubicacion = Ubicacion.objects.create(direccion=direccion)
                jugador.ubicacion = ubicacion  
            
            if foto:
                jugador.foto = foto

            jugador.save()
        
        return jugador

class EditPasswordForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}),
        required=True
    )
    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'}),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 != new_password2:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
