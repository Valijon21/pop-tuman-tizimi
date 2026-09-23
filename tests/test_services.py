import unittest
import os
import tempfile
from services.search_service import SearchService, normalize_text
from services.qr_service import clean_phone_number, generate_phone_qr_image
from services.excel_service import export_organizations_to_excel
from PIL import Image

class TestServices(unittest.TestCase):
    """Qidiruv, QR va Excel xizmatlari testlari."""

    def setUp(self):
        self.sample_data = [
            {"id": "1", "s": "Mahalla", "m": "Chorkesar MFY", "f": "Karimov Sardor", "t": "+998 90 123-45-67", "inn": "301234567", "izoh": "Markazda"},
            {"id": "2", "s": "Maktab", "m": "1-sonli Maktab", "f": "Usmonov Jamshid", "t": "+998 91 987-65-43", "inn": "309876543", "izoh": "Yangi bino"},
            {"id": "3", "s": "Bog'cha", "m": "5-sonli Bog'cha (MTT)", "f": "Aliyeva Malika", "t": "+998 93 111-22-33", "inn": "305555555", "izoh": "Bolalar bog'chasi"}
        ]

    def test_normalize_text(self):
        self.assertEqual(normalize_text("O`zbekiston"), "o'zbekiston")
        self.assertEqual(normalize_text("Bo‘g‘cha"), "bo'g'cha")

    def test_search_by_name(self):
        res = SearchService.search(self.sample_data, query="Chorkesar")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], "1")

    def test_search_by_inn(self):
        res = SearchService.search(self.sample_data, query="309876")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], "2")

    def test_search_by_category(self):
        res = SearchService.search(self.sample_data, category="Maktab")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["m"], "1-sonli Maktab")

    def test_search_by_field_type(self):
        # Nomi bo'yicha qidiruv
        res = SearchService.search(self.sample_data, query="Chorkesar", field_type="Nomi")
        self.assertEqual(len(res), 1)
        # F.I.SH bo'yicha qidiruv
        res = SearchService.search(self.sample_data, query="Karimov", field_type="F.I.SH")
        self.assertEqual(len(res), 1)
        # Nomi bo'yicha "Karimov" qidirilganda topilmasligi kerak
        res = SearchService.search(self.sample_data, query="Karimov", field_type="Nomi")
        self.assertEqual(len(res), 0)

    def test_search_stats(self):
        stats = SearchService.get_stats(self.sample_data)
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["with_inn"], 3)
        self.assertEqual(stats["with_phone"], 3)
        self.assertEqual(stats["categories"]["Mahalla"], 1)

    def test_qr_service_in_memory(self):
        phone = clean_phone_number("+998 (90) 123-45-67")
        self.assertEqual(phone, "+998901234567")
        img = generate_phone_qr_image(phone, size=200)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (200, 200))

    def test_excel_export(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            export_organizations_to_excel(self.sample_data, tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 1000)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_verification_text_builder(self):
        from services.verification_service import build_verification_text, extract_identifiers_from_text, format_role
        
        sample = {
            "m": "Chorkesar MFY",
            "inn": "203599806",
            "f": "Yondashev Xojiakbar Rustamali o‘g‘li",
            "s": "Hokim yordamchisi",
            "izoh": "JSHR: 30807995910027, Pasport: AB4561091"
        }
        
        # Test identifier extraction from comment
        jshr, seriya = extract_identifiers_from_text(sample["izoh"])
        self.assertEqual(jshr, "30807995910027")
        self.assertEqual(seriya, "AB4561091")
        
        # Test role formatting
        role = format_role(sample["s"], sample["m"])
        self.assertEqual(role, "Chorkesar MFY hokim yordamchisi")
        
        # Test full template generation
        text = build_verification_text(sample)
        self.assertIn("Tashkilot nomi: Chorkesar MFY", text)
        self.assertIn("-INN:   203599806", text)
        self.assertIn("F.I.O:  Yondashev Xojiakbar Rustamali o‘g‘li", text)
        self.assertIn("JSHR : 30807995910027", text)
        self.assertIn("Seriya : AB4561091", text)
        self.assertIn("Lavozimi: Chorkesar MFY hokim yordamchisi", text)
        self.assertIn("verfikatsiya bervoring.", text)

if __name__ == "__main__":
    unittest.main()

