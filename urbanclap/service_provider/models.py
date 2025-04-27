from django.db import models
from django.forms import ValidationError
from decimal import Decimal
from django.conf import settings
from django.utils.timezone import now


class ServiceProvider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    cat = models.ForeignKey('dashboard.Category', on_delete=models.SET_NULL, null=True, blank=True)
    subcat = models.ForeignKey('dashboard.subcatagory', on_delete=models.SET_NULL, null=True, blank=True)

    # Document Uploads for Verification
    id_proof = models.FileField(upload_to='kyc/id_proofs/', blank=True, null=True)
    address_proof = models.FileField(upload_to='kyc/address_proofs/', blank=True, null=True)
    certificate = models.FileField(upload_to='kyc/certificates/', blank=True, null=True)

    # Status and Approval
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.name if self.user.name else self.user.username

    class Meta:
        verbose_name = 'Service Provider'
        verbose_name_plural = 'Service Providers'

class Notification(models.Model):
    ADMIN = 'admin'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    service_provider = models.ForeignKey(
        'service_provider.ServiceProvider', on_delete=models.CASCADE, null=True, blank=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}"
    

class ServiceBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'client'}
    )
    service = models.ForeignKey('dashboard.service', on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_services',
        limit_choices_to={'role': 'service_provider'}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField()
    service_time = models.TimeField()
    address = models.TextField(max_length=48,blank=False,null=False)

    def clean(self):
        # Ensure only clients can book services
        if self.client.role != 'client':
            raise ValidationError("Only clients can book services.")

        # Ensure only service providers can be assigned
        if self.service_provider and self.service_provider.role != 'service_provider':
            raise ValidationError("Only service providers can be assigned to a service.")

    def save(self, *args, **kwargs):
        self.clean()
        super(ServiceBooking, self).save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} - {self.service.name} - {self.status}"
    


class ServiceProviderEarning(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.OneToOneField('service_provider.ServiceBooking', on_delete=models.CASCADE)
    payment = models.OneToOneField('dashboard.Payment', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    provider_earning = models.DecimalField(max_digits=10, decimal_places=2)
    payout_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payout_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider.name} - Booking {self.booking.id} - {self.payout_status}"