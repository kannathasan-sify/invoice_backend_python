from sqlalchemy.orm import Session
from ..models import document as models
from ..schemas import document as schemas
from .gst_service import calculate_gst
from datetime import datetime
import uuid
from .payment_service import payment_service
from .email_service import email_service
from .inventory_service import update_stock
from .currency_service import currency_service
from ..schemas import inventory as inv_schemas

def get_document(db: Session, document_id: uuid.UUID):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_company_documents(db: Session, company_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Document).filter(models.Document.company_id == company_id)\
        .offset(skip).limit(limit).all()

def create_company_document(db: Session, doc_in: schemas.DocumentCreate, user_id: uuid.UUID):
    # 1. Initialize totals
    subtotal = 0
    total_cgst = 0
    total_sgst = 0
    total_igst = 0
    total_amount = 0
    
    # 2. Prepare items and calculate taxes
    db_items = []
    for item in doc_in.items:
        gst = calculate_gst(
            quantity=float(item.quantity),
            unit_price=float(item.unit_price),
            tax_percent=float(item.tax_percentage),
            intra_state=doc_in.intra_state
        )
        
        db_item = models.DocumentItem(
            item_name=item.item_name,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_percentage=item.tax_percentage,
            cgst_amount=gst["cgst"],
            sgst_amount=gst["sgst"],
            igst_amount=gst["igst"],
            total_amount=gst["total"]
        )
        db_items.append(db_item)
        
        # Phase 3: Stock Decrement for Invoices
        if doc_in.document_type == "INVOICE" and item.product_id:
            update_stock(db, inv_schemas.StockUpdate(
                product_id=item.product_id,
                warehouse_id=doc_in.warehouse_id if hasattr(doc_in, 'warehouse_id') else uuid.UUID("00000000-0000-0000-0000-000000000000"), # Default/Placeholder
                quantity_change=-float(item.quantity),
                transaction_type="SALE"
            ))
        
        subtotal += gst["subtotal"]
        total_cgst += gst["cgst"]
        total_sgst += gst["sgst"]
        total_igst += gst["igst"]
        total_amount += gst["total"]

    # 3. Create document
    doc_number = f"{doc_in.document_type[:1]}-{str(uuid.uuid4())[:8].upper()}"
    
    # Phase 3: Multi-Currency
    exchange_rate = 1.0
    if doc_in.currency != "INR":
        exchange_rate = currency_service.get_rate(doc_in.currency)
    
    db_doc = models.Document(
        company_id=doc_in.company_id,
        user_id=user_id,
        customer_id=doc_in.customer_id,
        project_id=doc_in.project_id,
        document_type=doc_in.document_type,
        document_number=doc_number,
        currency=doc_in.currency,
        exchange_rate=exchange_rate,
        subtotal=subtotal,
        total_cgst=total_cgst,
        total_sgst=total_sgst,
        total_igst=total_igst,
        total_amount=total_amount,
        notes=doc_in.notes,
        valid_until=doc_in.valid_until,
        due_date=doc_in.due_date,
        items=db_items
    )
    
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    
    # 4. Phase 2 Features: Payments & Notifications
    if db_doc.document_type == "INVOICE":
        customer = db.query(models.Customer).filter(models.Customer.id == db_doc.customer_id).first()
        if customer and customer.email:
            # Generate Razorpay Link
            payment_link = payment_service.create_payment_link(
                amount=float(db_doc.total_amount),
                invoice_number=db_doc.document_number,
                customer_name=customer.name,
                customer_email=customer.email
            )
            
            if payment_link:
                db_doc.payment_link = payment_link
                db.commit()
                db.refresh(db_doc)
            
            # Send Email
            email_service.send_invoice_email(
                to_email=customer.email,
                invoice_number=db_doc.document_number,
                amount=float(db_doc.total_amount),
                pdf_url=db_doc.pdf_url or "Link pending",
                payment_link=db_doc.payment_link
            )
            
    return db_doc

def update_document_status(db: Session, document_id: uuid.UUID, status: str):
    db_doc = get_document(db, document_id)
    if db_doc:
        db_doc.status = status
        db.commit()
        db.refresh(db_doc)
    return db_doc
