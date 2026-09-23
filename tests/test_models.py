import unittest
from database.models import Organization

class TestModels(unittest.TestCase):
    """Organization ma'lumotlar modeli testlari."""

    def test_organization_creation_and_defaults(self):
        org = Organization(m="Pop Tuman Xalq Ta'limi", inn="123456789")
        self.assertTrue(bool(org.id))
        self.assertEqual(org.m, "Pop Tuman Xalq Ta'limi")
        self.assertEqual(org.inn, "123456789")
        self.assertIsNone(org.deleted_at)

    def test_from_dict_and_to_dict(self):
        data = {
            "id": "test-uuid-1234",
            "s": "Maktab",
            "m": "   1-sonli umumiy o'rta ta'lim maktabi   ",
            "f": "Alimov Alisher",
            "t": "+998 (90) 123-45-67",
            "inn": "301 234 567",
            "izoh": "Ta'mirda",
            "lavozim": "Direktor",
            "bux_tel": "+998931112233",
            "aparat_soni": 15,
            "ulangan_soni": 10,
            "updated_at": "2026-09-24 03:00:00"
        }
        org = Organization.from_dict(data)
        self.assertEqual(org.id, "test-uuid-1234")
        self.assertEqual(org.s, "Maktab")
        # Sanitizatsiya tekshiruvi: ortiqcha probellar tozalangan
        self.assertEqual(org.m, "1-sonli umumiy o'rta ta'lim maktabi")
        # INN tozalangan
        self.assertEqual(org.inn, "301234567")
        self.assertEqual(org.lavozim, "Direktor")
        self.assertEqual(org.bux_tel, "+998931112233")
        self.assertEqual(org.aparat_soni, 15)
        self.assertEqual(org.ulangan_soni, 10)

        d = org.to_dict()
        self.assertEqual(d["id"], "test-uuid-1234")
        self.assertEqual(d["inn"], "301234567")
        self.assertEqual(d["lavozim"], "Direktor")
        self.assertEqual(d["bux_tel"], "+998931112233")
        self.assertEqual(d["aparat_soni"], 15)
        self.assertEqual(d["ulangan_soni"], 10)
        self.assertEqual(d["updated_at"], "2026-09-24 03:00:00")
        self.assertNotIn("deleted_at", d)

    def test_organization_validation(self):
        # Yaroqli tashkilot
        valid_org = Organization(m="Chorkesar MFY", inn="305123987", t="+998901234567")
        is_ok, errs = valid_org.validate()
        self.assertTrue(is_ok)
        self.assertEqual(len(errs), 0)

        # Nomi yo'q tashkilot
        invalid_org = Organization(m="", inn="305123987")
        is_ok, errs = invalid_org.validate()
        self.assertFalse(is_ok)
        self.assertTrue(any("nomi" in e for e in errs))

        # Noto'g'ri INN
        bad_inn_org = Organization(m="Tashkilot", inn="123")
        is_ok, errs = bad_inn_org.validate()
        self.assertFalse(is_ok)
        self.assertTrue(any("9 ta raqam" in e for e in errs))

if __name__ == "__main__":
    unittest.main()
