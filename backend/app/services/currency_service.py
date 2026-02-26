import requests
from typing import Dict, Optional
import time

class CurrencyService:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/INR"
        self._cache = {}
        self._last_fetched = 0
        self._cache_expiry = 3600 # 1 hour

    def get_exchange_rates(self) -> Dict[str, float]:
        """Fetch live exchange rates with caching."""
        now = time.time()
        if now - self._last_fetched < self._cache_expiry and self._cache:
            return self._cache
        
        try:
            response = requests.get(self.base_url)
            data = response.json()
            self._cache = data.get("rates", {})
            self._last_fetched = now
            return self._cache
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return {"INR": 1.0, "USD": 0.012, "EUR": 0.011} # Static partial fallback

    def get_rate(self, target_currency: str) -> float:
        """Get rate for target currency relative to INR."""
        rates = self.get_exchange_rates()
        # The API returns 1 INR = X USD. We want to store how much 1 Target = X INR?
        # Actually, let's store 1 Target = X INR for easier calculation.
        # So we need 1 / rate[target]
        rate_inr_to_target = rates.get(target_currency, 1.0)
        return 1.0 / rate_inr_to_target if rate_inr_to_target != 0 else 1.0

currency_service = CurrencyService()
