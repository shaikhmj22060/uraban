from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from dashboard.models import Payment
import stripe
import requests

from .utils import generate_invoice_pdf
from django.contrib.auth import get_user_model
from service_provider.models import ServiceBooking

stripe.api_key = settings.STRIPE_SECRET_KEY


# @shared_task
# def send_invoice_email(user_email, booking_id, payment_intent_id):
#     try:
#         # Retrieve the booking and related data
#         booking = ServiceBooking.objects.get(id=booking_id)
#         payment = Payment.objects.get(booking=booking)

#         # Retrieve the PaymentIntent
#         intent = stripe.PaymentIntent.retrieve(payment_intent_id)
#         customer_id = intent.customer

#         # Safety check: Make sure the customer exists
#         if not customer_id:
#             raise ValueError("Stripe customer ID not found in PaymentIntent.")

#         # Step 1: Create Invoice Item
#         stripe.InvoiceItem.create(
#             customer=customer_id,
#             amount=int(payment.amount * 100),  # Convert to paise
#             currency="inr",
#             description=f"Service: {booking.service.name}"
#         )

#         # Step 2: Create invoice (but don’t auto-advance yet)
#         invoice = stripe.Invoice.create(
#             customer=customer_id,
#             auto_advance=False  # manually finalize
#         )

#         # Step 3: Finalize invoice
#         finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)

#         # Step 4: Retrieve again to get PDF link
#         invoice = stripe.Invoice.retrieve(finalized_invoice.id)
#         invoice_pdf_url = invoice.invoice_pdf
#         # print("Invoice PDF URL:", invoice_pdf_url)

#         if not invoice_pdf_url:
#             raise ValueError("Invoice PDF URL is not available.")

#         # Step 5: Download the invoice PDF
#         response = requests.get(invoice_pdf_url)

#         # Step 6: Send email with PDF attached
#         email = EmailMessage(
#             subject=f"Invoice for your service booking #{booking.id}",
#             body="Thanks for booking! Please find your invoice attached.",
#             to=[user_email]
#         )
#         email.attach(f"invoice_{booking.id}.pdf", response.content, "application/pdf")
#         email.send()

#         print("Invoice email sent successfully.")

#     except Exception as e:
#         print(f"[Invoice Error] {e}")




@shared_task
def send_custom_invoice_email(user_id, booking_id, total_amount, quantity):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    booking = ServiceBooking.objects.get(id=booking_id)

    pdf_buffer = generate_invoice_pdf(user, booking, total_amount, quantity)

    email = EmailMessage(
        subject="Your Service Booking Invoice",
        body="Thanks for booking with us. Please find your invoice attached.",
        to=[user.email]
    )
    email.attach("invoice.pdf", pdf_buffer.read(), "application/pdf")
    email.send()
