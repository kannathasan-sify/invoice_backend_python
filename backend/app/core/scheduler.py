from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import document as models
from ..services.email_service import email_service
from ..services.communication_service import communication_service
from datetime import date, datetime, timedelta
import uuid

scheduler = BackgroundScheduler()

def auto_generate_recurring_invoices():
    """Daily task to generate invoices from recurring templates."""
    db: Session = SessionLocal()
    try:
        # Implementation: Find documents marked as recurring that are due for generation
        # For now, this is a placeholder for the logic discussed in Phase 2
        print(f"[{datetime.now()}] Running recurring invoice generation task...")
    finally:
        db.close()

def send_overdue_reminders():
    """Daily task to send reminders for unpaid, overdue invoices."""
    db: Session = SessionLocal()
    try:
        print(f"[{datetime.now()}] Running overdue reminders task...")
        today = date.today()
        overdue_docs = db.query(models.Document).filter(
            models.Document.document_type == "INVOICE",
            models.Document.status != "paid",
            models.Document.due_date < today
        ).all()
        
        for doc in overdue_docs:
            customer = db.query(models.Customer).filter(models.Customer.id == doc.customer_id).first()
            if customer and customer.email:
                email_service.send_invoice_email(
                    to_email=customer.email,
                    invoice_number=doc.document_number,
                    amount=float(doc.total_amount),
                    pdf_url=doc.pdf_url or "Link pending",
                    payment_link=doc.payment_link
                )
            
            if customer and customer.phone:
                communication_service.send_invoice_whatsapp(
                    to_phone=customer.phone,
                    invoice_number=doc.document_number,
                    pdf_url=doc.pdf_url or ""
                )
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        # Run daily at 1:00 AM
        scheduler.add_job(
            auto_generate_recurring_invoices,
            CronTrigger(hour=1, minute=0),
            id="recurring_invoices",
            replace_existing=True
        )
        # Run daily at 9:00 AM
        scheduler.add_job(
            send_overdue_reminders,
            CronTrigger(hour=9, minute=0),
            id="overdue_reminders",
            replace_existing=True
        )
        scheduler.start()
        print("Scheduler started background tasks.")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shut down.")
