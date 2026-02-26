import unittest
from decimal import Decimal
from app.services.gst_service import calculate_gst

class TestGSTService(unittest.TestCase):
    def test_intra_state_calculation(self):
        # 1 Qty * 1000 Price + 18% GST (Intra-state)
        result = calculate_gst(1, 1000, 18, intra_state=True)
        self.assertEqual(result["cgst"], Decimal("90.00"))
        self.assertEqual(result["sgst"], Decimal("90.00"))
        self.assertEqual(result["igst"], Decimal("0.00"))
        self.assertEqual(result["total"], Decimal("1180.00"))

    def test_inter_state_calculation(self):
        # 2 Qty * 500 Price + 12% GST (Inter-state)
        result = calculate_gst(2, 500, 12, intra_state=False)
        self.assertEqual(result["cgst"], Decimal("0.00"))
        self.assertEqual(result["sgst"], Decimal("0.00"))
        self.assertEqual(result["igst"], Decimal("120.00"))
        self.assertEqual(result["total"], Decimal("1120.00"))

    def test_zero_tax(self):
        result = calculate_gst(1, 500, 0, intra_state=True)
        self.assertEqual(result["total"], Decimal("500.00"))

if __name__ == "__main__":
    unittest.main()
