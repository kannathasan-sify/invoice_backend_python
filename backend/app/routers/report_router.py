from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import reports_service
import uuid

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/gstr/{company_id}")
def download_gstr_report(company_id: uuid.UUID, db: Session = Depends(get_db)):
    excel_data = reports_service.generate_gstr_report(db, company_id)
    
    filename = f"GSTR_Report_{company_id}_{uuid.uuid4().hex[:6]}.xlsx"
    
    return Response(
        content=excel_data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
