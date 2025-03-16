from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from dashboard.models import *
# Create your views here.

@login_required
def home(request):
    return render(request,'clone/home.html')



@login_required
def service_page(request):
    return render(request,'clone/service.html')



@login_required
def view_category_client(request):
    data = Category.objects.all()
    sub_data = subcatagory.objects.all()
    services = service.objects.all()
    return render(request, 'clone/wireframe.html',{'data':data,'sub_data':sub_data,'services': services})
def is_admin(user):
    return user.is_authenticated and getattr(user, "role", None) == "admin"

@login_required
@user_passes_test(is_admin)  # Redirect to custom login page
def admin_dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        
        user = custom_user.objects.create_user(username=username, email=email, password=password, role=role)
        user.save()
        login(request, user)
        return redirect('home')  # Redirect after login

    return render(request, 'clone/register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Use .get() to avoid KeyError
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)

            # Redirect based on user role
            if user.role == 'admin':
                return redirect('dashboard')
            # elif user.role == 'service_provider':
            #     return redirect('service_provider_dashboard')
            elif user.role == 'client':
                return redirect('wire')
            else:
                return redirect('home')  # Default redirect if no role is set
            
        else:
            return render(request, 'clone/index.html', {'error_message': 'Invalid credentials'})

    return render(request, 'clone/index.html')

def logout_user(request):
    logout(request)
    return redirect('login_user')

def search_service(request):
    query = request.GET.get('q')  # Get the search term from the URL
    results = []

    if query:
        results = service.objects.filter(name__icontains=query)  # Case-insensitive search

    return render(request, 'clone/search.html', {'results': results, 'query': query})

# cart views
@login_required
def add_to_cart(request, service_id):
    services = get_object_or_404(service, id=service_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, service=services)

    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    return redirect("cart_view")

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)  # Only get items for the logged-in user

    total_price = sum(item.service.price * item.quantity for item in cart_items)
    cart_item_count = cart_items.count()  # Count different services, not quantity

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "cart_item_count": cart_item_count
    }
    
    return render(request, "clone/cart.html", context)

@login_required
def increase_quantity(request, service_id):
    cart_item = Cart.objects.filter(user=request.user, service_id=service_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_view')

@login_required
def decrease_quantity(request, service_id):
    cart_item = Cart.objects.filter(user=request.user, service_id=service_id).first()
    
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity reaches 0
    
    return redirect('cart_view')

@login_required
def remove_from_cart(request, service_id):
    Cart.objects.filter(user=request.user, service_id=service_id).delete()
    return redirect('cart_view')

@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart_view')
