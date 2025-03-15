from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('wire',view_category,name='wire'),
    path('register',register,name='register_user'),
    path('login',login_user,name='login_user'),
    path('logout',logout_user,name='logout_user'),
    path('service',service_page,name='service'),
    path('search/', search_service, name='search_service'),
    # path('cart',cart,name='cart'),
     path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:service_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:service_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('cart/increase/<int:service_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:service_id>/', decrease_quantity, name='decrease_quantity'),
]
