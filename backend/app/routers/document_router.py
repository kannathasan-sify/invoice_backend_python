from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ..database import get_db
from ..schemas import document as schemas
from ..services import document_service as service
from ..services.pdf_service import generate_invoice_pdf

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=schemas.Document)
def create_document(doc_in: schemas.DocumentCreate, db: Session = Depends(get_db)):
    # Note: In production, user_id would come from the JWT token
    # For now, using a placeholder or accepting it in request if needed
    user_id = UUID("00000000-0000-0000-0000-000000000000") # Placeholder
    return service.create_company_document(db, doc_in, user_id)

@router.get("/{document_id}", response_model=schemas.Document)
def read_document(document_id: UUID, db: Session = Depends(get_db)):
    db_doc = service.get_document(db, document_id)
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc

@router.get("/company/{company_id}", response_model=List[schemas.Document])
def read_company_documents(company_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_company_documents(db, company_id, skip=skip, limit=limit)

@router.patch("/{document_id}/status", response_model=schemas.Document)
def update_status(document_id: UUID, status: str, db: Session = Depends(get_db)):
    return service.update_document_status(db, document_id, status)

@router.post("/{document_id}/convert", response_model=schemas.Document)
def convert_quotation(document_id: UUID, db: Session = Depends(get_db)):
    # 1. Fetch quotation
    quotation = service.get_document(db, document_id)
    if not quotation or quotation.document_type != "QUOTATION":
        raise HTTPException(status_code=400, detail="Document not found or not a quotation")
    
    # 2. Convert logic (simple status change and type change for this unified model)
    # In a more strict system, we'd create a new record.
    # Here we update the existing one to 'INVOICE' as per the 'Unified Document' requirement.
    quotation.document_type = "INVOICE"
    quotation.status = "draft"
    quotation.document_number = f"I-{str(uuid.uuid4())[:8].upper()}"
    db.commit()
    db.refresh(quotation)
    return quotation
from fastapi.responses import FileResponse
import os

@router.get("/{document_id}/pdf")
def get_document_pdf(document_id: UUID, db: Session = Depends(get_db)):
    # 1. Fetch document with all details
    doc = db.query(service.models.Document).filter(service.models.Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # 2. Prepare data for PDF service
    # ReportLab expects a dictionary-like structure
    doc_data = {
        "document_type": doc.document_type,
        "document_number": doc.document_number,
        "issue_date": str(doc.issue_date),
        "due_date": str(doc.due_date),
        "notes": doc.notes,
        "subtotal": float(doc.subtotal),
        "total_amount": float(doc.total_amount),
        "company": {
            "name": doc.company.name,
            "address": doc.company.address,
            "gstin": doc.company.gstin
        },
        "customer": {
            "name": doc.customer.name,
            "address": doc.customer.address,
            "gstin": doc.customer.gstin
        },
        "items": [
            {
                "item_name": item.item_name,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "tax_percentage": float(item.tax_percentage),
                "cgst_amount": float(item.cgst_amount),
                "sgst_amount": float(item.sgst_amount),
                "igst_amount": float(item.igst_amount),
                "total_amount": float(item.total_amount)
            } for item in doc.items
        ]
    }
    
    # 3. Generate PDF
    temp_dir = "temp_pdfs"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    filename = f"{doc.document_number}.pdf"
    file_path = os.path.join(temp_dir, filename)
    
    generate_invoice_pdf(doc_data, file_path)
    
    # 4. Return as file
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )
