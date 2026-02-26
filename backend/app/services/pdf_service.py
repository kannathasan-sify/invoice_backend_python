import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch

def generate_invoice_pdf(document_data: dict, output_path: str):
    """
    Generates a professional PDF invoice or quotation using ReportLab.
    document_data should contain company, customer, and items details.
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=24, textColor=colors.hexColor("#1111d4"), 
        spaceAfter=12, alignment=1
    )
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=10, leading=12)

    # Header: Document Title (INVOICE or QUOTATION)
    doc_type = document_data.get("document_type", "INVOICE").upper()
    elements.append(Paragraph(doc_type, title_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Company & Customer Info
    company = document_data.get("company", {})
    customer = document_data.get("customer", {})
    
    info_data = [
        [
            Paragraph(f"<b>FROM:</b><br/>{company.get('name')}<br/>{company.get('address')}<br/>GSTIN: {company.get('gstin')}", header_style),
            Paragraph(f"<b>TO:</b><br/>{customer.get('name')}<br/>{customer.get('address')}<br/>GSTIN: {customer.get('gstin')}", header_style)
        ],
        [
            Paragraph(f"<b>Invoice #:</b> {document_data.get('document_number')}<br/><b>Date:</b> {document_data.get('issue_date')}", header_style),
            Paragraph(f"<b>Due Date:</b> {document_data.get('due_date') or document_data.get('valid_until')}", header_style)
        ]
    ]
    info_table = Table(info_data, colWidths=[3*inch, 3*inch])
    info_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.4 * inch))

    # Items Table
    item_header = ["Item", "Qty", "Price", "Tax %", "CGST", "SGST", "IGST", "Total"]
    table_data = [item_header]
    
    for item in document_data.get("items", []):
        table_data.append([
            item.get("item_name"),
            str(item.get("quantity")),
            str(item.get("unit_price")),
            f"{item.get('tax_percentage')}%",
            str(item.get("cgst_amount")),
            str(item.get("sgst_amount")),
            str(item.get("igst_amount")),
            str(item.get("total_amount"))
        ])

    # Totals
    table_data.append(["", "", "", "", "", "", "<b>Subtotal</b>", str(document_data.get("subtotal"))])
    table_data.append(["", "", "", "", "", "", "<b>Grand Total</b>", f"<b>{document_data.get('total_amount')}</b>"])

    item_table = Table(table_data, colWidths=[1.5*inch, 0.5*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 1.0*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.hexColor("#1111d4")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (-2,-2), (-1,-1), 'RIGHT'),
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 0.5 * inch))

    # Footer/Signature
    footer_text = f"Notes: {document_data.get('notes', 'Thank you for your business!')}"
    elements.append(Paragraph(footer_text, styles['Normal']))
    elements.append(Spacer(1, 1 * inch))
    elements.append(Paragraph("__________________________<br/>Authorized Signature", styles['Normal']))

    doc.build(elements)
    return output_path
