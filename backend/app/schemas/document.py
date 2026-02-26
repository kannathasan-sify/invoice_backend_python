from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime
from uuid import UUID

class DocumentItemBase(BaseModel):
    item_name: str
    quantity: Decimal
    unit_price: Decimal
    product_id: Optional[UUID] = None
    tax_percentage: Optional[Decimal] = 0

class DocumentItemCreate(DocumentItemBase):
    pass

class DocumentItem(DocumentItemBase):
    id: UUID
    cgst_amount: Decimal
    sgst_amount: Decimal
    igst_amount: Decimal
    total_amount: Decimal

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    customer_id: UUID
    project_id: Optional[UUID] = None
    document_type: str = Field(..., pattern="^(QUOTATION|INVOICE)$")
    intra_state: bool = True
    notes: Optional[str] = None
    valid_until: Optional[date] = None
    due_date: Optional[date] = None

class DocumentCreate(DocumentBase):
    company_id: UUID
    items: List[DocumentItemCreate]

class DocumentUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class Document(DocumentBase):
    id: UUID
    company_id: UUID
    user_id: Optional[UUID]
    document_number: str
    subtotal: Decimal
    total_cgst: Decimal
    total_sgst: Decimal
    total_igst: Decimal
    total_amount: Decimal
    status: str
    issue_date: date
    pdf_url: Optional[str] = None
    payment_link: Optional[str] = None
    currency: str = "INR"
    exchange_rate: Decimal = 1.0
    items: List[DocumentItem] = []

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    gstin: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    subdomain: Optional[str] = None
    custom_domain: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: UUID
    class Config:
        from_attributes = True
