
from django.urls import path
from .views import *
urlpatterns = [
    path('',Sdashobard,name='provider_dashboard'),
    path('Sregister/',service_provider_register,name='Sregister'),
]
