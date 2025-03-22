from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ServiceProvider
from django.contrib.auth import get_user_model
from django.http import JsonResponse

# Create your views here.



User = get_user_model()

def Sdashobard(request):
    return render(request, 'service_provider/service_dashboard.html')

def service_provider_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        # Check for username and email existence
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists. Please choose a different one.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists. Please use a different one.'})

        # Create user and service provider
        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = 'service_provider'
        if profile_image:
            user.profile_image = profile_image
        user.save()

        ServiceProvider.objects.create(user=user)

        return JsonResponse({'status': 'success', 'message': 'Registration successful! Please wait for admin approval.'})

    return render(request, 'service_provider/service_register.html')
