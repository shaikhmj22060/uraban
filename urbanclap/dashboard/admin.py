from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'profile_image')}),
    )

admin.site.register(custom_user, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(subcatagory)
admin.site.register(service)
admin.site.register(Cart)
admin.site.register(KYCRecord)