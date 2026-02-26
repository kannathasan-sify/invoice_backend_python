from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.document import Document
from uuid import UUID

def get_company_stats(db: Session, company_id: UUID):
    # Total Revenue (Paid Invoices)
    total_revenue = db.query(func.sum(Document.total_amount))\
        .filter(Document.company_id == company_id, Document.document_type == "INVOICE", Document.status == "paid").scalar() or 0

    # Pending Payments (Sent Invoices)
    pending_payments = db.query(func.sum(Document.total_amount))\
        .filter(Document.company_id == company_id, Document.document_type == "INVOICE", Document.status == "sent").scalar() or 0

    # Counts
    total_invoices = db.query(func.count(Document.id))\
        .filter(Document.company_id == company_id, Document.document_type == "INVOICE").scalar() or 0
    
    total_quotations = db.query(func.count(Document.id))\
        .filter(Document.company_id == company_id, Document.document_type == "QUOTATION").scalar() or 0

    return {
        "total_revenue": float(total_revenue),
        "pending_payments": float(pending_payments),
        "total_invoices": total_invoices,
        "total_quotations": total_quotations
    }
