from sqlalchemy.orm import Session
from ..models import inventory as models
from ..schemas import inventory as schemas
import uuid

def create_product(db: Session, product_in: schemas.ProductCreate):
    db_product = models.Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_company_products(db: Session, company_id: uuid.UUID):
    return db.query(models.Product).filter(models.Product.company_id == company_id).all()

def update_stock(db: Session, update: schemas.StockUpdate):
    db_ledger = models.StockLedger(**update.model_dump())
    db.add(db_ledger)
    db.commit()
    db.refresh(db_ledger)
    return db_ledger

def get_stock_level(db: Session, product_id: uuid.UUID):
    # Sum of quantity_change in ledger for this product
    from sqlalchemy import func
    result = db.query(func.sum(models.StockLedger.quantity_change))\
        .filter(models.StockLedger.product_id == product_id).scalar()
    return result or 0
