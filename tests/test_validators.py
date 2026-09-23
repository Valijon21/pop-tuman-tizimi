import unittest
from core.validators import (
    clean_inn, validate_inn,
    clean_phone, format_phone, validate_phone,
    sanitize_text
)

class TestValidators(unittest.TestCase):
    """Kiritilgan ma'lumotlarni tekshirish va tozalash testlari."""

    def test_clean_inn(self):
        self.assertEqual(clean_inn("123 456 789"), "123456789")
        self.assertEqual(clean_inn("INN: 305-123-999"), "305123999")
        self.assertEqual(clean_inn(""), "")

    def test_validate_inn(self):
        # 9 xonali to'g'ri INN
        ok, res = validate_inn("123456789")
        self.assertTrue(ok)
        self.assertEqual(res, "123456789")

        # Bo'sh INN allow_empty=True bo'lganda ruxsat beriladi
        ok, _ = validate_inn("", allow_empty=True)
        self.assertTrue(ok)

        # Bo'sh INN allow_empty=False bo'lganda xato beradi
        ok, msg = validate_inn("", allow_empty=False)
        self.assertFalse(ok)

        # 8 xonali (kam) INN
        ok, msg = validate_inn("12345678")
        self.assertFalse(ok)
        self.assertIn("9 ta raqam", msg)

        # 10 xonali (ortiqcha) INN
        ok, msg = validate_inn("1234567890")
        self.assertFalse(ok)

    def test_clean_phone(self):
        self.assertEqual(clean_phone("90 123 45 67"), "+998901234567")
        self.assertEqual(clean_phone("+998 (91) 345-67-89"), "+998913456789")
        self.assertEqual(clean_phone("835-123-4567"), "+998351234567")

    def test_format_phone(self):
        self.assertEqual(format_phone("901234567"), "+998 (90) 123-45-67")
        self.assertEqual(format_phone("+998911234567"), "+998 (91) 123-45-67")

    def test_validate_phone(self):
        ok, res = validate_phone("90 123-45-67")
        self.assertTrue(ok)
        self.assertEqual(res, "+998 (90) 123-45-67")

        ok, msg = validate_phone("12345")
        self.assertFalse(ok)

    def test_sanitize_text(self):
        self.assertEqual(sanitize_text("   Salom   Dunyo   "), "Salom Dunyo")
        self.assertEqual(sanitize_text("Matn\x00\x07"), "Matn")

if __name__ == "__main__":
    unittest.main()
