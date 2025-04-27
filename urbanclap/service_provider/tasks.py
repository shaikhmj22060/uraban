from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_service_status_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,       
        settings.EMAIL_HOST_USER,  # or settings.EMAIL_HOST_USER
        [recipient_email],
        fail_silently=False,
    )