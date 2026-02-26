from twilio.rest import Client
from ..core.config import settings
import os

class CommunicationService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886") # Twilio Sandbox
        
        self.client = None
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)

    def send_invoice_whatsapp(self, to_phone: str, invoice_number: str, pdf_url: str):
        if not self.client:
            print("Twilio credentials not configured")
            return
        
        # Twilio requires phone numbers in E.164 format with 'whatsapp:' prefix
        if not to_phone.startswith('whatsapp:'):
            to_phone = f"whatsapp:{to_phone}"
            
        try:
            message = self.client.messages.create(
                from_=self.from_whatsapp,
                body=f"Your invoice {invoice_number} is ready. View it here: {pdf_url}",
                to=to_phone,
                media_url=[pdf_url] if pdf_url.startswith('http') else None
            )
            return message.sid
        except Exception as e:
            print(f"Twilio WhatsApp Error: {e}")
            return None

communication_service = CommunicationService()
