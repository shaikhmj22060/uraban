from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from .forms import *

# Create your views here.

# category view section
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def admin_profile(request):
    return render(request, 'dashboard/admin_profile.html')

def view_category(request):
    data = Category.objects.all()
    sub_data = subcatagory.objects.all()
    return render(request, 'dashboard/category.html',{'data':data,'sub_data':sub_data})


def edit_category(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        data = Category.objects.get(id=id)
        data.name = name
        data.image = image
        data.save()
        return redirect('view_category')
    else:
      return HttpResponse(request,"errrrr")
    
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        data = Category.objects.create(name=name, image=image)
        return redirect('view_category')
    else:
        return HttpResponse(request,"errrrr")
    
def delete_category(request,id):
    # if request.method == 'POST':
        data = Category.objects.get(id=id)
        data.delete()
        return redirect('view_category')

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
    return redirect('view_category')  # Replace 'subcategory_list' with your actual URL name


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
        return redirect('view_category')
def delete_sub(request, id):
    # Fetch the SubCategory object to delete
    data = get_object_or_404(subcatagory, id=id)
    # Delete the object
    data.delete()
    # Redirect to the subcategory list
    return redirect('view_category')  # Replace 'subcategory_list' with your actual URL name

# service view section

def view_service(request):
    services = service.objects.all()
    subcategories = subcatagory.objects.all()
    return render(request, 'dashboard/services.html', {'services': services, 'subcategories': subcategories})

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

def delete_service(request, id):
    services = get_object_or_404(service, id=id)
    services.delete()
    return redirect('view_service')