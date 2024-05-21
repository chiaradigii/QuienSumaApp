# applications/comunicaciones/views.py 
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from applications.jugador.models import Jugador
from .models import ChatSession, Notification
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

def start_chat(request, jugador_id):
    current_user = request.user
    other_user = get_object_or_404(Jugador, pk=jugador_id)
    chat_session, created = ChatSession.get_or_create_session(current_user, other_user)
    return redirect('comunicaciones_app:chatPage', chat_id=chat_session.id)


def chatPage(request, chat_id):
    chat_session = get_object_or_404(ChatSession, id=chat_id)
    messages = chat_session.messages.all().order_by('timestamp')

    if chat_session.user1 == request.user:
        other_user = chat_session.user2
    else:
        other_user = chat_session.user1

    return render(request, 'comunicaciones/chatPage.html', {'chat_id': chat_id, 'messages': messages, 'other_user': other_user})

@csrf_exempt
@login_required
def mark_notification_read(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def fetch_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return JsonResponse({
        "notifications": list(notifications.values("id", "message", "created_at"))
    })