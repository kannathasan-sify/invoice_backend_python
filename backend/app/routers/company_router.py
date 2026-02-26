from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..schemas import document as schemas
from ..services import company_service as service

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=schemas.Company)
def create_company(company_in: schemas.CompanyCreate, db: Session = Depends(get_db)):
    # Placeholder user_id
    user_id = UUID("00000000-0000-0000-0000-000000000000")
    return service.create_company(db, company_in, user_id)

@router.get("/me", response_model=List[schemas.Company])
def get_my_companies(db: Session = Depends(get_db)):
    user_id = UUID("00000000-0000-0000-0000-000000000000")
    return service.get_user_companies(db, user_id)

@router.get("/{company_id}", response_model=schemas.Company)
def get_company(company_id: UUID, db: Session = Depends(get_db)):
    db_company = service.get_company_profile(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company
