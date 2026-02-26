import razorpay
from ..core.config import settings
from typing import Optional

class PaymentService:
    def __init__(self):
        self.client = None
        if settings.RAZORPAY_KEY and settings.RAZORPAY_SECRET:
            self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

    def create_payment_link(self, amount: float, invoice_number: str, customer_name: str, customer_email: str) -> Optional[str]:
        if not self.client:
            # Fallback or Log: "Razorpay credentials not configured"
            return None
        
        try:
            # Amount in paise (e.g. 100.00 -> 10000)
            amount_paise = int(float(amount) * 100)
            
            data = {
                "amount": amount_paise,
                "currency": "INR",
                "accept_partial": False,
                "first_min_partial_amount": 0,
                "description": f"Payment for Invoice {invoice_number}",
                "customer": {
                    "name": customer_name,
                    "email": customer_email,
                    "contact": "" # Can be added if available
                },
                "notify": {
                    "sms": True,
                    "email": True
                },
                "reminder_enable": True,
                "notes": {
                    "invoice_number": invoice_number
                },
                "callback_url": "https://example.com/payment-callback", # TODO: Update with real URL
                "callback_method": "get"
            }
            
            response = self.client.payment_link.create(data)
            return response.get('short_url')
        except Exception as e:
            print(f"Error creating Razorpay payment link: {e}")
            return None

payment_service = PaymentService()
