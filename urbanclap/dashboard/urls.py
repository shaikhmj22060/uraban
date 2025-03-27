from django.urls import path
from .views import *
from clone.views import *

urlpatterns = [
    path('', admin_dashboard, name = 'dashboard'),
    path('profile/', profile_view, name = 'profile'),
    path('users/', all_users_view, name = 'users'),
    path('roles/', users_by_roles, name = 'roles'),
     path('create-admin/', create_admin, name='create_admin'),
    # category urls
    path('category/', view_category , name = 'category'),
    path('editcatgory/<int:id>/',edit_category,name='edit_category'),
    path('createcat/',create_category,name='createcat'),
    path('deletecat/<int:id>/',delete_category,name='deletecat'),
    path('createsubcat',create_sub,name='createsubcat'),
    path('editsubcat/<int:id>/',edit_sub,name='editsubcat'),
    path('deletesubcat/<int:id>/',delete_sub,name='deletesubcat'),
    
    # service urls
    path('service/', view_service, name = 'view_service'),
     path('services/create/', create_service, name='createservice'),
    path('services/edit/<int:id>/', edit_service, name='editservice'),
    path('services/delete/<int:id>/', delete_service, name='deleteservice'),
    
    #Messages urls
    path('notifications/', admin_notifications, name='admin_notifications'),
    path('notifications/approve/<int:provider_id>/', approve_kyc, name='approve_kyc'),
    path('notifications/reject/<int:provider_id>/', reject_kyc, name='reject_kyc'),
    path('notifications/review/<int:provider_id>/', review_kyc, name='review_kyc'),
    
    
    path('kyc-history/', kyc_history, name='kyc_history'),
]
