
from django.urls import path
from .views import *
from dashboard.views import profile_view
urlpatterns = [
    path('',Sdashobard,name='provider_dashboard'),
    path('Sregister/',service_provider_register,name='Sregister'),
    path('kyc/',kyc,name='kyc'),
    path('kyc_register/',kyc_register,name='kyc_register'),
    path('s_notificaton/',s_notification,name='s_notification'),
    path('s_notifications/<int:notification_id>/mark_as_read/', mark_as_read, name='mark_as_read'),
    path('s_profile/',profile_view,name='s_profile'),
]
