import os
from typing import Optional, List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        self.sg_client = None
        if settings.SENDGRID_API_KEY:
            self.sg_client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_invoice_email(self, to_email: str, invoice_number: str, amount: float, pdf_url: str, payment_link: Optional[str] = None):
        subject = f"Invoice {invoice_number} from Your Company"
        
        body = f"""
        Dear Customer,

        Please find attached the invoice {invoice_number} for the amount of ₹{amount}.
        
        You can view/download the PDF here: {pdf_url}
        """
        
        if payment_link:
            body += f"\n\nYou can pay online using this link: {payment_link}"
            
        body += "\n\nRegards,\nAccounts Team"

        if self.sg_client:
            self._send_via_sendgrid(to_email, subject, body)
        else:
            self._send_via_smtp(to_email, subject, body)

    def _send_via_sendgrid(self, to_email: str, subject: str, content: str):
        message = Mail(
            from_email='noreply@example.com',
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )
        try:
            self.sg_client.send(message)
        except Exception as e:
            print(f"SendGrid Error: {e}")

    def _send_via_smtp(self, to_email: str, subject: str, content: str):
        # Basic SMTP settings from env (local testing or production SMTP)
        smtp_host = os.getenv("SMTP_HOST", "localhost")
        smtp_port = int(os.getenv("SMTP_PORT", "1025")) # Default for MailHog or similar
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASS", "")

        msg = MIMEMultipart()
        msg['From'] = 'noreply@example.com'
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        except Exception as e:
            print(f"SMTP Error: {e}")

email_service = EmailService()
