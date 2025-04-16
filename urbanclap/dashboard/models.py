from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'media/category')
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)    
    def __str__(self):
        return self.name

class subcatagory(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'media/subcategory')
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.name
    
class service(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = None)
    subcatagory = models.ForeignKey(subcatagory, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'media/service')
    price = models.FloatField()
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.quantity})"
    



class custom_user(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    
class KYCRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    reason = models.TextField(blank=True, null=True)  # Only used if rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"



class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.OneToOneField('service_provider.ServiceBooking', on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.status}"
