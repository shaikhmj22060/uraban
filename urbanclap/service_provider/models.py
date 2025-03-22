from django.db import models
from dashboard.models import *
from django.conf import settings

class ServiceProvider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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