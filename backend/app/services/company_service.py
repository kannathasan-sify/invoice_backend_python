from sqlalchemy.orm import Session
from ..models import document as models
from ..schemas import document as schemas
import uuid

def create_company(db: Session, company_in: schemas.CompanyCreate, user_id: uuid.UUID):
    db_company = models.Company(**company_in.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    # Automatically add the creator as the OWNER
    company_user = models.CompanyUser(
        company_id=db_company.id,
        user_id=user_id,
        role="OWNER"
    )
    db.add(company_user)
    db.commit()
    
    return db_company

def get_user_companies(db: Session, user_id: uuid.UUID):
    return db.query(models.Company).join(models.CompanyUser)\
        .filter(models.CompanyUser.user_id == user_id).all()

def get_company_profile(db: Session, company_id: uuid.UUID):
    return db.query(models.Company).filter(models.Company.id == company_id).first()
