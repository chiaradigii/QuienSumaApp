# Views.py 
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from applications.jugador.models import Jugador
from .models import ChatSession
from django.contrib.auth import get_user_model

User = get_user_model()

def start_chat(request, jugador_id):
    current_user = request.user
    other_user = get_object_or_404(Jugador, pk=jugador_id)
    chat_session, created = ChatSession.get_or_create_session(current_user, other_user)
    return redirect('comunicaciones_app:chatPage', chat_id=chat_session.id)


def chatPage(request, chat_id):
    # Assuming that ChatSession stores references to user IDs or similar
    chat_session = get_object_or_404(ChatSession, id=chat_id)

    # Render a template to display the chat or handle other logic
    print('Rendering chatPage with chat_id:', chat_id)
    return render(request, 'comunicaciones/chatPage.html', {'chat_id': chat_id})