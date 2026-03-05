import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "BillPro GST Invoice API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8081",
        "https://invoice-backend-python-4.onrender.com",
    ]
    
    # Database
    DATABASE_URL: str = ""

    def __init__(self, **values):
        super().__init__(**values)
        raw_url = os.getenv("DATABASE_URL", "postgresql://postgres:Kannathasan%4018@db.gqqfwuhluzjqmhybrsev.supabase.co:5432/postgres")
        self.DATABASE_URL = self._sanitize_db_url(raw_url)

    def _sanitize_db_url(self, url: str) -> str:
        import re
        from urllib.parse import quote_plus
        
        # Strip extraneous whitespace and brackets
        url = url.strip().strip('[]')
        
        # Regex to capture parts safely
        # Note: the password group matches greedily until the LAST @ before the host
        pattern = r"^(?P<prefix>\w+://)(?P<user>[^:/]+):(?P<password>.+)@(?P<host>[^:/@]+):(?P<port>\d+)/(?P<db>.+)$"
        match = re.match(pattern, url)
        
        if match:
            password = match.group("password")
            # Only encode if it contains special chars and isn't already looking encoded
            if ("@" in password or "[" in password or "]" in password) and "%" not in password:
                safe_pass = quote_plus(password)
                return f"{match.group('prefix')}{match.group('user')}:{safe_pass}@{match.group('host')}:{match.group('port')}/{match.group('db')}"
        
        return url
    
    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "MANGOCITY@1234567890")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://gqqfwuhluzjqmhybrsev.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "sb_publishable_k1kV3ahqslcNzjhvA3WQXw_pvrU6xdA")
    
    # Third-party APIs
    RAZORPAY_KEY: str = os.getenv("RAZORPAY_KEY", "")
    RAZORPAY_SECRET: str = os.getenv("RAZORPAY_SECRET", "")
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")

    class Config:
        case_sensitive = True

settings = Settings()
