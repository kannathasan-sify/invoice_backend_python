from decimal import Decimal
from typing import Dict

def calculate_gst(
    quantity: float, 
    unit_price: float, 
    tax_percent: float, 
    intra_state: bool = True
) -> Dict[str, Decimal]:
    """
    Calculates GST components based on quantity, unit price, and tax percentage.
    If intra_state is True, tax is split into CGST and SGST.
    If intra_state is False, tax is assigned to IGST.
    """
    q = Decimal(str(quantity))
    price = Decimal(str(unit_price))
    tax_p = Decimal(str(tax_percent))

    subtotal = q * price
    tax_total = (subtotal * tax_p) / Decimal("100")

    if intra_state:
        cgst = tax_total / Decimal("2")
        sgst = tax_total / Decimal("2")
        igst = Decimal("0")
    else:
        cgst = Decimal("0")
        sgst = Decimal("0")
        igst = tax_total

    total = subtotal + tax_total

    return {
        "subtotal": subtotal.quantize(Decimal("0.01")),
        "cgst": cgst.quantize(Decimal("0.01")),
        "sgst": sgst.quantize(Decimal("0.01")),
        "igst": igst.quantize(Decimal("0.01")),
        "total": total.quantize(Decimal("0.01")),
    }
