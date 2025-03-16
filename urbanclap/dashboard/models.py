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
    


from django.contrib.auth.models import AbstractUser
from django.db import models

class custom_user(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
