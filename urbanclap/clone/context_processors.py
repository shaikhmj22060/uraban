from django.shortcuts import get_object_or_404
from dashboard.models import *  # Import your service model


def cart_item_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # If not logged in, show zero

    return {"cart_item_count": cart_count}