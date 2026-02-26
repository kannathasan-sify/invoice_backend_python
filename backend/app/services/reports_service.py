import pandas as pd
from sqlalchemy.orm import Session
from ..models import document as models
from io import BytesIO
import uuid

def generate_gstr_report(db: Session, company_id: uuid.UUID):
    # Fetch all invoices for the company
    docs = db.query(models.Document).filter(
        models.Document.company_id == company_id,
        models.Document.document_type == "INVOICE"
    ).all()
    
    data = []
    for doc in docs:
        customer = db.query(models.Customer).filter(models.Customer.id == doc.customer_id).first()
        for item in doc.items:
            data.append({
                "Invoice Number": doc.document_number,
                "Date": doc.issue_date,
                "Customer Name": customer.name if customer else "Unknown",
                "Customer GSTIN": customer.gstin if customer else "",
                "Item Name": item.item_name,
                "Quantity": item.quantity,
                "Unit Price": item.unit_price,
                "Taxable Value": float(item.quantity) * float(item.unit_price),
                "GST %": item.tax_percentage,
                "CGST": item.cgst_amount,
                "SGST": item.sgst_amount,
                "IGST": item.igst_amount,
                "Total Amount": item.total_amount,
                "Status": doc.status
            })
            
    df = pd.DataFrame(data)
    
    # Write to Excel in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='GSTR_Report')
        
    return output.getvalue()
