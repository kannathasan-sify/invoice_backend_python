from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import inventory as schemas
from ..services import inventory_service as service
import uuid
from typing import List

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, product)

@router.get("/products/company/{company_id}", response_model=List[schemas.Product])
def get_products(company_id: uuid.UUID, db: Session = Depends(get_db)):
    return service.get_company_products(db, company_id)

@router.post("/stock/", response_model=None)
def update_stock(update: schemas.StockUpdate, db: Session = Depends(get_db)):
    service.update_stock(db, update)
    return {"message": "Stock updated successfully"}

@router.get("/stock/{product_id}")
def get_stock_level(product_id: uuid.UUID, db: Session = Depends(get_db)):
    return {"product_id": product_id, "stock_level": service.get_stock_level(db, product_id)}
