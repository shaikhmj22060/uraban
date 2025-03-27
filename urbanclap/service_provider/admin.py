from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ServiceProvider)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'service_provider', 'message', 'created_at', 'is_read']
