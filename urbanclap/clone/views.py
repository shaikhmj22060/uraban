from django.contrib import messages

from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from dashboard.models import *
from service_provider.models import *
import stripe
# Create your views here.

def is_client(user):
    return user.is_authenticated and user.role == 'client'


def home(request):
    return render(request,'clone/home.html')




def service_page(request):
    return render(request,'clone/service.html')




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
        
        
        user = custom_user.objects.create_user(username=username, email=email, password=password)
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
            elif user.role == 'service_provider':
                 return redirect('provider_dashboard')
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
@user_passes_test(is_client)
def add_to_cart(request, service_id):
    services = get_object_or_404(service, id=service_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, service=services)

    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    return redirect("cart_view")

@login_required
@user_passes_test(is_client)
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
@user_passes_test(is_client)
def increase_quantity(request, service_id):
    cart_item = Cart.objects.filter(user=request.user, service_id=service_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_view')

@login_required
@user_passes_test(is_client)
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
@user_passes_test(is_client)
def remove_from_cart(request, service_id):
    Cart.objects.filter(user=request.user, service_id=service_id).delete()
    return redirect('cart_view')

@login_required
@user_passes_test(is_client)
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart_view')



# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.service.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        service_date = request.POST.get('service_date')
        service_time = request.POST.get('service_time')
        address = request.POST.get('address')
        if not service_date or not service_time:
            messages.error(request, "Please select a valid service date and time.")
            return redirect('checkout')

        # Create Payment Intent
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Convert to cents
                currency="inr",
                metadata={"user_id": request.user.id}
            )
            request.session['service_date'] = service_date
            request.session['service_time'] = service_time
            request.session['address'] = address
            request.session['payment_intent_id'] = intent['id']
            return render(request, 'clone/payment.html', {
                'cart_items': cart_items,
                'total_amount': total_amount,
                'client_secret': intent.client_secret
            })
        except Exception as e:
            messages.error(request, f"Payment Error: {e}")
            return redirect('checkout')

    return render(request, 'clone/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

def payment_success_view(request):
    payment_intent_id = request.session.get('payment_intent_id')
    service_date = request.session.get('service_date')
    service_time = request.session.get('service_time')
    address = request.session.get('address')

    if not payment_intent_id:
        messages.error(request, "Payment session not found.")
        return redirect('checkout')

    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if payment_intent.status == 'succeeded':
            # Create service bookings
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                ServiceBooking.objects.create(
                    client=request.user,
                    service=item.service,
                    service_date=service_date,
                    service_time=service_time,
                    address=address,
                )
            # Clear cart
            cart_items.delete()

            messages.success(request, "Payment successful! Booking confirmed.")
            return redirect('client_bookings')
        else:
            messages.error(request, "Payment not successful. Please try again.")
            return redirect('checkout')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('checkout')
    

def client_bookings(request):
    bookings = ServiceBooking.objects.filter(client=request.user).order_by('-booking_date')
    return render(request, 'clone/client_bookings.html', {'bookings': bookings})

