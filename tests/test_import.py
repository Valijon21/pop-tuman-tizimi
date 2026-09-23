import unittest
import os
import tempfile
import csv
from services.excel_service import import_organizations_from_file

class TestImportService(unittest.TestCase):
    """Excel va CSV fayllardan ommaviy import qilish testlari."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_import_from_csv(self):
        """CSV fayldan tashkilotlarni aniqlash va import qilish."""
        csv_path = os.path.join(self.temp_dir.name, "test_import.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Tashkilot Turi", "Nomi", "F.I.SH", "Telefon", "INN", "Izoh"])
            writer.writerow(["Mahalla", "Navbahor MFY", "Soliyev Bobur", "90 123 45 67", "309112233", "Yangi MFY"])
            writer.writerow(["Maktab", "15-maktab", "Karimova Zebo", "+998912345678", "204556677", ""])

        items, warnings = import_organizations_from_file(csv_path)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["m"], "Navbahor MFY")
        self.assertEqual(items[0]["inn"], "309112233")
        self.assertEqual(items[0]["t"], "+998 (90) 123-45-67")
        self.assertEqual(items[1]["m"], "15-maktab")

    def test_import_empty_file(self):
        """Bo'sh faylni yuklashda ogohlantirish qaytarish."""
        empty_csv = os.path.join(self.temp_dir.name, "empty.csv")
        with open(empty_csv, "w", encoding="utf-8") as f:
            f.write("")

        items, warnings = import_organizations_from_file(empty_csv)
        self.assertEqual(len(items), 0)
        self.assertTrue(len(warnings) > 0)

    def test_import_unsupported_format(self):
        """Noto'g'ri fayl formati xatosi."""
        bad_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(bad_file, "w", encoding="utf-8") as f:
            f.write("text data")

        items, warnings = import_organizations_from_file(bad_file)
        self.assertEqual(len(items), 0)
        self.assertIn("qo'llab-quvvatlanadi", warnings[0].lower())

if __name__ == "__main__":
    unittest.main()
