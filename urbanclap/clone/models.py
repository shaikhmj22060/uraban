
# models.py
from django.db import models
from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey('service_provider.ServiceBooking', on_delete=models.CASCADE)  # replace with actual booking model name if different
    feedback = models.TextField()
    rating = models.IntegerField(null=True, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} for Booking #{self.booking.id}"
