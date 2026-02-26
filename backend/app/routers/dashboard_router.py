from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..services import dashboard_service as service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/{company_id}")
def get_summary(company_id: UUID, db: Session = Depends(get_db)):
    return service.get_company_stats(db, company_id)
