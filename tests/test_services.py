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

    def test_vcard_qr_service(self):
        from services.qr_service import generate_vcard_data, generate_vcard_qr_image
        vcard = generate_vcard_data(name="Karimov Sardor", phone="901234567", org="Chorkesar MFY", title="Rais", inn="301234567")
        self.assertIn("BEGIN:VCARD", vcard)
        self.assertIn("FN:Karimov Sardor", vcard)
        self.assertIn("ORG:Chorkesar MFY", vcard)
        self.assertIn("TITLE:Rais", vcard)
        self.assertIn("END:VCARD", vcard)

        img = generate_vcard_qr_image(name="Karimov Sardor", phone="901234567", org="Chorkesar MFY", title="Rais", inn="301234567", size=220)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (220, 220))

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

    def test_cabinet_access_text_builder(self):
        from services.cabinet_service import build_cabinet_access_text, get_cabinet_portal_url
        sample = {
            "m": "22-Sonli Umumiy O'rta Ta'lim Maktabi",
            "inn": "206907205",
            "f": "Dehqanova Azimaxon Ortiqovna",
            "s": "Maktab"
        }
        
        text = build_cabinet_access_text(sample)
        expected = (
            "Tashkilot nomi: 22-Sonli Umumiy O'rta Ta'lim Maktabi\n"
            "INN:   206907205\n"
            "F.I.O:  Dehqanova Azimaxon Ortiqovna\n"
            "cabinetga dostup"
        )
        self.assertEqual(text, expected)
        
        # Test portal resolution
        url = get_cabinet_portal_url(sample["s"])
        self.assertEqual(url, "https://e-maktab.uz")

    def test_broadcast_service(self):
        from services.broadcast_service import (
            filter_audience_recipients, extract_clean_phone_list, calculate_sms_segments
        )
        data = [
            {"s": "Hokim yordamchisi", "m": "Chorkesar MFY", "f": "Xojiakbar", "t": "+998901234567"},
            {"s": "Mahalla (MFY)", "m": "Chorkesar MFY", "f": "Aliyev", "t": "+998912345678"},
            {"s": "Maktab", "m": "1-maktab", "f": "Karimov", "t": "+998933334455"},
        ]

        # Test filter by Hokim yordamchisi
        recipients = filter_audience_recipients(data, "hokim_yordamchilari")
        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0]["f"], "Xojiakbar")

        # Test phone extraction
        phones = extract_clean_phone_list(recipients)
        self.assertEqual(phones, ["+998901234567"])

        # Test SMS calculation
        info = calculate_sms_segments("Favqulodda yig'ilish")
        self.assertEqual(info["parts"], 1)
        self.assertGreater(info["length"], 0)

    def test_telegram_bot_service(self):
        from services.telegram_bot import TelegramBotService
        class MockDM:
            data = [{"m": "Chorkesar MFY", "inn": "203599806", "f": "Xojiakbar", "s": "Hokim yordamchisi"}]
            settings = {"telegram_subscribers": [123456]}
        
        # Test initialization with flexible argument order
        bot1 = TelegramBotService(MockDM(), "dummy_token_123")
        self.assertEqual(bot1.token, "dummy_token_123")
        self.assertIn(123456, bot1.subscribers)

        bot2 = TelegramBotService("dummy_token_456", MockDM())
        self.assertEqual(bot2.token, "dummy_token_456")

        # Test command parsing
        self.assertEqual(TelegramBotService.parse_command("/verif_202701426"), ("/verif", "202701426"))
        self.assertEqual(TelegramBotService.parse_command("/cabinet_202701426"), ("/cabinet", "202701426"))
        self.assertEqual(TelegramBotService.parse_command("/verif 202701426"), ("/verif", "202701426"))
        self.assertEqual(TelegramBotService.parse_command("/verif_202701426@PopTumanBot"), ("/verif", "202701426"))

        # Test find first with INN, command string, and Name
        found = bot1._find_first("203599806")
        self.assertIsNotNone(found)
        self.assertEqual(found["m"], "Chorkesar MFY")

        found_by_cmd = bot1._find_first("/verif_203599806")
        self.assertIsNotNone(found_by_cmd)
        self.assertEqual(found_by_cmd["m"], "Chorkesar MFY")

        found_by_name = bot1._find_first("Chorkesar")
        self.assertIsNotNone(found_by_name)
        self.assertEqual(found_by_name["inn"], "203599806")

    def test_gsheet_service_helpers(self):
        from services.gsheet_service import extract_sheet_id, is_service_account_available
        # URL orqali ID ajratib olish
        url = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0"
        self.assertEqual(extract_sheet_id(url), "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")

        # Oddiy nom berilganda o'zini qaytarishi kerak
        self.assertEqual(extract_sheet_id("Mening Jadvalim"), "Mening Jadvalim")

        # Mavjud bo'lmagan fayl tekshiruvi
        self.assertFalse(is_service_account_available("non_existent_file_path_12345.json"))

    def test_worker_thread(self):
        from core.threading_utils import WorkerThread
        from PyQt5.QtWidgets import QApplication
        import sys

        app = QApplication.instance() or QApplication(sys.argv)

        results = []
        errors = []

        def sample_calc(a, b):
            return a + b

        worker = WorkerThread(sample_calc, 10, 20)
        worker.result_ready.connect(lambda res: results.append(res))
        worker.error_occurred.connect(lambda err: errors.append(err))

        worker.start()
        worker.wait(2000)
        app.processEvents()

        self.assertEqual(results, [30])
        self.assertEqual(len(errors), 0)

if __name__ == "__main__":
    unittest.main()



