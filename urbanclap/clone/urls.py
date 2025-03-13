from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('wire',view_category,name='wire'),
    path('register',register,name='register_user'),
    path('login',login_user,name='login_user'),
    path('logout',logout_user,name='logout_user'),
    path('service',service,name='service'),
]
