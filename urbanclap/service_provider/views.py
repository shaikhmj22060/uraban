from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from dashboard.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.



User = get_user_model()

def is_service_provider(user):
    return user.is_authenticated and user.role == 'service_provider'

@login_required
@user_passes_test(is_service_provider)
def Sdashobard(request):
    return render(request, 'service_provider/s_dashboard.html')

@login_required
@user_passes_test(is_service_provider)
def kyc (request):
    categories = Category.objects.all()
    subcategories = subcatagory.objects.all()
    return render(request, 'service_provider/KYC.html', {'categories': categories, 'subcategories': subcategories})

def service_provider_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
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
        user = User.objects.create_user(username=username, email=email, password=password,name=name)
        user.role = 'service_provider'
        if profile_image:
            user.profile_image = profile_image
        user.save()

        
        return JsonResponse({'status': 'success', 'message': 'Registration successful! Redirecting to login...', 'redirect': '/login'})

    return render(request, 'service_provider/service_register.html')


   

@login_required
@user_passes_test(is_service_provider)

def kyc_register(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to submit KYC.'})

        if request.user.role != 'service_provider':
            return JsonResponse({'status': 'error', 'message': 'Only service providers can submit KYC.'})

        # Check if KYC already exists
        if ServiceProvider.objects.filter(user=request.user).exists():
            return JsonResponse({'status': 'error', 'message': 'KYC already submitted for this user.'})

        try:
            # Extract form data
            name = request.POST.get('name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            cat_id = request.POST.get('cat')
            subcat_id = request.POST.get('subcat')
            id_proof = request.FILES.get('id_proof')
            address_proof = request.FILES.get('address_proof')
            certificate = request.FILES.get('certificate')

            if not all([name, phone_number, address, city, state, cat_id, subcat_id, id_proof, address_proof]):
                return JsonResponse({'status': 'error', 'message': 'All required fields must be filled.'})

            category = Category.objects.get(id=cat_id)
            subcategory = subcatagory.objects.get(id=subcat_id)

            # Save KYC Data
            service_provider = ServiceProvider.objects.create(
                user=request.user,
                phone_number=phone_number,
                address=address,
                city=city,
                state=state,
                cat=category,
                subcat=subcategory,
                id_proof=id_proof,
                address_proof=address_proof,
                certificate=certificate,
            )

            # Send Notification to All Admins
            admins = User.objects.filter(role='admin')
            for admin in admins:
                Notification.objects.create(
                    recipient=admin,
                    service_provider=service_provider,
                    message=f"New KYC submitted by {request.user.username}.  review.",
                    created_at=now(),
                    is_read=False
                )

            return JsonResponse({'status': 'success', 'message': 'KYC submitted successfully. Admin will review it soon.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
@user_passes_test(is_service_provider)
def s_notification(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'service_provider/notification.html', {'notifications': notifications})

@login_required
@user_passes_test(is_service_provider)
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    # Delete the notification
    notification.delete()

    # Redirect to the notifications page
    return redirect('s_notification')