from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name = 'dashboard'),
    # category urls
    path('category/', view_category , name = 'view_category'),
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
]
