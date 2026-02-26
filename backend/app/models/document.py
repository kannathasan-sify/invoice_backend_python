import uuid
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    gstin = Column(String)
    address = Column(String)
    state = Column(String)
    phone = Column(String)
    email = Column(String)
    logo_url = Column(String)
    bank_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)
    branch_name = Column(String)
    signature_url = Column(String)
    subdomain = Column(String, unique=True, index=True)
    custom_domain = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CompanyUser(Base):
    __tablename__ = "company_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), nullable=False) # Refers to Supabase auth.users
    role = Column(String) # OWNER, ADMIN, STAFF, ACCOUNTANT
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('company_id', 'user_id', name='_company_user_uc'),)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    gstin = Column(String)
    address = Column(String)
    state = Column(String)
    phone = Column(String)
    email = Column(String)
    contact_person = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True)) # Creator
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    document_type = Column(String) # QUOTATION, INVOICE
    document_number = Column(String, unique=True)
    subtotal = Column(Numeric(12, 2), default=0)
    total_cgst = Column(Numeric(12, 2), default=0)
    total_sgst = Column(Numeric(12, 2), default=0)
    total_igst = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), default=0)
    status = Column(String, default="draft")
    issue_date = Column(Date, server_default=func.current_date())
    valid_until = Column(Date)
    due_date = Column(Date)
    notes = Column(String)
    pdf_url = Column(String)
    payment_link = Column(String)
    currency = Column(String, default="INR")
    exchange_rate = Column(Numeric(12, 6), default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company")
    customer = relationship("Customer")
    items = relationship("DocumentItem", back_populates="document", cascade="all, delete-orphan")

class DocumentItem(Base):
    __tablename__ = "document_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Numeric(12, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    tax_percentage = Column(Numeric(5, 2))
    cgst_amount = Column(Numeric(12, 2), default=0)
    sgst_amount = Column(Numeric(12, 2), default=0)
    igst_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(12, 2), nullable=False)
    
    document = relationship("Document", back_populates="items")
