from sqlalchemy.orm import Session
from ..models import document as models
from ..schemas import customer as schemas
import uuid

def get_customer(db: Session, customer_id: uuid.UUID):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_company_customers(db: Session, company_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).filter(models.Customer.company_id == company_id)\
        .offset(skip).limit(limit).all()

def create_customer(db: Session, customer_in: schemas.CustomerCreate):
    db_customer = models.Customer(**customer_in.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: uuid.UUID, customer_in: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: uuid.UUID):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer
