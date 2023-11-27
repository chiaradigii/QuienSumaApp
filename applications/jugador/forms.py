from django import forms

from .models import Jugador

class SingUpForm(forms.ModelForm):

    class Meta:
        model = Jugador
        fields =  ('__all__')
        widgets = {

            #'categoria' : forms.CheckboxSelectMultiple()
        }
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña',required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}))