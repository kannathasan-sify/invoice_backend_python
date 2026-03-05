from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    gstin: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_person: Optional[str] = None

class CustomerCreate(CustomerBase):
    company_id: UUID

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    gstin: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_person: Optional[str] = None

class Customer(CustomerBase):
    id: UUID
    company_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
