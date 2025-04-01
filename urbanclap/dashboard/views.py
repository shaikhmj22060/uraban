from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from service_provider.models import *

# Create your views here.

# category view section

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

login_required
@user_passes_test(is_admin)
def admin_profile(request):
    return render(request, 'dashboard/admin_profile.html')

login_required
@user_passes_test(is_admin)
def all_users_view(request):
    users = custom_user.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})


login_required
@user_passes_test(is_admin)
def view_category(request):
    data = Category.objects.all()
    sub_data = subcatagory.objects.all()
    return render(request, 'dashboard/category.html',{'data':data,'sub_data':sub_data})


login_required
@user_passes_test(is_admin)
def edit_category(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        data = Category.objects.get(id=id)
        data.name = name
        data.image = image
        data.save()
        return redirect('category')
    else:
      return HttpResponse(request,"errrrr")

login_required
@user_passes_test(is_admin)    
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        data = Category.objects.create(name=name, image=image)
        return redirect('category')
    else:
        return HttpResponse(request,"errrrr")

login_required
@user_passes_test(is_admin)    
def delete_category(request,id):
    # if request.method == 'POST':
        data = Category.objects.get(id=id)
        data.delete()
        return redirect('category')

login_required
@user_passes_test(is_admin)
def edit_sub(request, id):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')  # Get the selected category ID

        # Fetch the SubCategory object to update
        data = get_object_or_404(subcatagory, id=id)

        # Update fields
        data.name = name
        if image:  # Only update the image if a new one is provided
            data.image = image

        # Update the associated category
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            data.category = category

        # Save the changes
        data.save()

    # Redirect to a success page or the subcategory list
    return redirect('category')  # Replace 'subcategory_list' with your actual URL name


login_required
@user_passes_test(is_admin)
def create_sub(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')  # Get the selected category ID

        # Fetch the associated Category object
        category = get_object_or_404(Category, id=category_id)

        # Create and save the new SubCategory object
        subcategory = subcatagory(
            name=name,
            image=image,
            category=category
        )
        subcategory.save()

        # Redirect to a success page or the subcategory list
        return redirect('category')

login_required
@user_passes_test(is_admin)    
def delete_sub(request, id):
    # Fetch the SubCategory object to delete
    data = get_object_or_404(subcatagory, id=id)
    # Delete the object
    data.delete()
    # Redirect to the subcategory list
    return redirect('category')  # Replace 'subcategory_list' with your actual URL name

# service view section

login_required
@user_passes_test(is_admin)
def view_service(request):
    services = service.objects.all()
    subcategories = subcatagory.objects.all()
    return render(request, 'dashboard/services.html', {'services': services, 'subcategories': subcategories})

login_required
@user_passes_test(is_admin)
def create_service(request):
    if request.method == 'POST':
        # Get data from the request
        name = request.POST.get('name')
        subcatagory_id = request.POST.get('subcatagory')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')

        # Fetch the SubCategory instance
        subcategory = get_object_or_404(subcatagory, id=subcatagory_id)

        # Create and save the new Service
        service.objects.create(
            name=name,
            subcatagory=subcategory,
            image=image,
            price=price,
            description=description
        )
        return redirect('view_service')
    
    # If it's a GET request, fetch subcategories for the dropdown
    subcategories = subcatagory.objects.all()
    return render(request, 'add_service.html', {'subcategories': subcategories})

login_required
@user_passes_test(is_admin)
def edit_service(request, id):
    services = get_object_or_404(service, id=id)
    if request.method == 'POST':
        # Get data from the request
        name = request.POST.get('name')
        subcatagory_id = request.POST.get('subcatagory')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')

        # Fetch the SubCategory instance
        subcategory = get_object_or_404(subcatagory, id=subcatagory_id)

        # Update the Service instance
        services.name = name
        services.subcatagory = subcategory
        services.price = price
        services.description = description
        if image:  # Only update the image if a new one is provided
            services.image = image
        services.save()

        return redirect('view_service')
    
    # If it's a GET request, fetch subcategories for the dropdown
    subcategories = subcatagory.objects.all()
    return render(request, 'edit_service.html', {'service': services, 'subcategories': subcategories})

login_required
@user_passes_test(is_admin)
def delete_service(request, id):
    services = get_object_or_404(service, id=id)
    services.delete()
    return redirect('view_service')





login_required
@user_passes_test(is_admin)
def profile_view(request):
    user = request.user
    template_name = "dashboard/admin_profile.html"
    redirect_url = "profile"

    # Check if the request is for the service provider profile
    if request.resolver_match.url_name == "s_profile":
        template_name = "service_provider/s_profile.html"
        redirect_url = "s_profile"

    if request.method == "POST":
        name = request.POST.get("name", user.username)
        email = request.POST.get("email", user.email)
        profile_image = request.FILES.get("profile_image")

        # Update user details
        user.username = name
        user.email = email

        if profile_image:
            user.profile_image = profile_image

        user.save()
        messages.success(request, "Profile updated successfully!")

        # Redirect to the respective dashboard
        return redirect(redirect_url)

    return render(request, template_name, {"user": user})



login_required
@user_passes_test(is_admin)
def users_by_roles(request):
    role = request.GET.get('role', 'client')
    users = custom_user.objects.filter(role=role)
    return render(request, 'dashboard/roles.html', {'users': users})

login_required
@user_passes_test(is_admin)
def create_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')
        
        if custom_user.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('roles')
        
        if custom_user.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('roles')
        
        # Create admin user
        custom_user.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            profile_image=profile_image
        )
        messages.success(request, 'Admin created successfully.')
        return redirect('roles')
    
    return redirect('roles')

login_required
@user_passes_test(is_admin)
def admin_notifications(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return JsonResponse({'status': 'error', 'message': 'Access denied.'})

    # Fetch notifications for the logged-in admin
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'dashboard/notification.html', {'notifications': notifications})

login_required
@user_passes_test(is_admin)
def approve_kyc(request, provider_id):
    service_provider = get_object_or_404(ServiceProvider, id=provider_id)

    # Create approval record
    KYCRecord.objects.create(user=service_provider.user, status='approved')

    # Update service provider status
    service_provider.is_verified = True
    service_provider.save()
    Notification.objects.filter(service_provider=service_provider).delete()
    # Send notification
    Notification.objects.create(
        recipient=service_provider.user,
        message="Congratulations! Your KYC has been approved."
    )

    messages.success(request, "KYC approved successfully.")
    return redirect('admin_notifications')


# Reject KYC

login_required
@user_passes_test(is_admin)
def reject_kyc(request, provider_id):
    service_provider = get_object_or_404(ServiceProvider, id=provider_id)
    reason = request.POST.get('reason')

    if not reason:
        messages.error(request, "Rejection reason is required.")
        return redirect('review_kyc', service_provider_id=provider_id)

    # Create rejection record with reason
    KYCRecord.objects.create(user=service_provider.user, status='rejected', reason=reason)

    # Delete the KYC data from the ServiceProvider model
    service_provider.delete()
    
    # Delete notifications using provider_id
    Notification.objects.filter(service_provider_id=provider_id).delete()

    # Send notification to the user
    Notification.objects.create(
        recipient=service_provider.user,
        message=f"Your KYC has been rejected. Reason: {reason}"
    )

    messages.success(request, "KYC rejected successfully.")
    return redirect('admin_notifications')

login_required
@user_passes_test(is_admin)
def review_kyc(request, provider_id):
    service_provider = get_object_or_404(ServiceProvider, id=provider_id)
    return render(request, 'dashboard/review_kyc.html', {'service_provider': service_provider})


login_required
@user_passes_test(is_admin)
def kyc_history(request):
    kyc_records = KYCRecord.objects.all().order_by('-created_at')
    return render(request, 'dashboard/kyc_history.html', {'kyc_records': kyc_records})