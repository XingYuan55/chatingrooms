from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Message
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def chat(request):
    users = User.objects.exclude(username=request.user.username)
    messages = Message.objects.filter(receiver__isnull=True) | \
              Message.objects.filter(sender=request.user) | \
              Message.objects.filter(receiver=request.user)
    return render(request, 'chat/index.html', {
        'users': users,
        'messages': messages
    })

@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        message = Message.objects.create(
            sender=request.user,
            receiver=User.objects.get(username=request.POST.get('receiver')) if request.POST.get('receiver') else None,
            image=request.FILES['image'],
            is_private=bool(request.POST.get('receiver'))
        )
        return JsonResponse({'status': 'success', 'image_url': message.image.url})
    return JsonResponse({'status': 'error'}) 