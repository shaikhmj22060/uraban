
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
    path('accept-service/<int:booking_id>/', accept_service, name='accept_service'),
    path('completed-service/<int:booking_id>/',mark_service_completed,name= 'complete_service'),
    path('accepted-services/', accepted_services, name='accepted_services'),
    path('s_booking_request/',Service_request,name='s_booking_request'),
    path('notifications/', notification_test_view, name='notification_test'),
   path("send-notification/<int:user_id>/", send_test_notification, name="send_test_notification"),
]
