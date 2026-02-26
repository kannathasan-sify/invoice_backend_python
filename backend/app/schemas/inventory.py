from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str
    description: Optional[str] = None
    base_price: Decimal = 0
    tax_percentage: Optional[Decimal] = None

class ProductCreate(ProductBase):
    company_id: UUID

class Product(ProductBase):
    id: UUID
    company_id: UUID
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class WarehouseBase(BaseModel):
    name: str
    location: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    company_id: UUID

class Warehouse(WarehouseBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    product_id: UUID
    warehouse_id: UUID
    quantity_change: Decimal
    transaction_type: str
    reference_id: Optional[UUID] = None
