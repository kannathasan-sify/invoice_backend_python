from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..schemas import customer as schemas
from ..services import customer_service as service

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=schemas.Customer)
def create_customer(customer_in: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return service.create_customer(db, customer_in)

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: UUID, db: Session = Depends(get_db)):
    db_customer = service.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.get("/company/{company_id}", response_model=List[schemas.Customer])
def read_company_customers(company_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_company_customers(db, company_id, skip=skip, limit=limit)

@router.patch("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: UUID, customer_in: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = service.update_customer(db, customer_id, customer_in)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):
    success = service.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
