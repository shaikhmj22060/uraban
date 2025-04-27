from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generate_invoice_pdf(user, booking, total_amout, quantity):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "Service Booking Invoice")

    # Booking Info
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Invoice Date: {datetime.now().strftime('%d-%m-%Y')}")
    p.drawString(50, height - 120, f"Booking ID: {booking.id}")
    p.drawString(50, height - 140, f"Client Name: {booking.client.username}")
    p.drawString(50, height - 160, f"Email: {booking.client.email}")

    # Service Info
    p.drawString(50, height - 200, "Service Details:")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 220, f"Service: {booking.service.name}")
    p.drawString(250, height - 220, f"Quantity: {quantity}")
    p.drawString(400, height - 220, f"Amount Paid: ₹{total_amout}")

    # Footer
    p.setFont("Helvetica", 10)
    p.drawString(50, 80, "This is a system-generated invoice for your completed payment.")
    p.drawString(50, 65, "Thank you for booking with us!")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
