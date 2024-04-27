from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    View
)
from .models import Jugador
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from .forms import SignUpForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from ..ubicaciones.models import Ubicacion
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator

class SignUpView(FormView):
    """Vista para crear un nuevo jugador"""
    model = Jugador
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('jugador_app:success_signup')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        # Create or Update the Ubicacion instance
        direccion = cleaned_data.get('direccion')
        ubicacion = Ubicacion(direccion=direccion)
        ubicacion.save()
        # Create the Jugador instance
        user = Jugador.objects.create_user(
            user=form.cleaned_data['user'],
            nombre=form.cleaned_data['nombre'],
            apellido=form.cleaned_data['apellido'],
            fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
            sexo=form.cleaned_data['sexo'],
            correo=form.cleaned_data['correo'],
            posicion=form.cleaned_data['posicion'],
            foto=form.cleaned_data['foto'],
            ubicacion = ubicacion,
            password=form.cleaned_data['password1']
        )
        user.save()
        # Session variable to show a success message in the login page
        self.request.session['registro_exitoso'] = True
        self.request.session.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        if 'registro_exitoso' in request.session:
            del request.session['registro_exitoso']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SignUpView,self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)
        
class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm 
    success_url = reverse_lazy('main_app:pagina_principal')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginView,self).form_valid(form)

class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home/home.html'))

class UpdatePasswordView(FormView):
    template_name = 'registration/password_change_form.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('registration/login.html')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.user,
            password=usuario.password
        )
        if user:
            user.set_password(form.cleaned_data['password1'])
            user.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class JugadorListView(LoginRequiredMixin,ListView):
    template_name = "jugador/jugadores_disponibles.html"
    model = Jugador
    context_object_name = "jugadores"
    paginate_by = 10

    def get_queryset(self):
        queryset = super(JugadorListView, self).get_queryset()
        kword = self.request.GET.get('kword', '')

        if kword:
            queryset = queryset.filter(nombre__icontains=kword)

        return queryset.exclude(is_superuser=True)

class SuccessSignUpView(TemplateView):
    template_name = 'registration/success_signup.html'    
    model = Jugador
    form_class = SignUpForm

class JugadorDetailView(LoginRequiredMixin,DetailView):
    template_name = "jugador/detalle_jugador.html"
    model = Jugador
    context_object_name = "jugador"
    def get_context_data(self, **kwargs):
        context = super(JugadorDetailView, self).get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context