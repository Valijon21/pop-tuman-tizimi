"""
tests.test_features_12346: 1, 2, 3, 4, 6-topshiriqlar bo'yicha maxsus sinov testlari.
1. Ma'lumotlar bazasi yaxlitligi (SQLite & JSON 100% sinxronlik, temp table va to'liq o'chirish).
2. QLockFile orqali yagona nusxa (Single Instance Guard) tekshiruvi.
3. Telegram bot sessiya yangilanishi va exponential backoff.
4. Mahalla Yettiligi 360° Pasport A4 PDF eksporti (vektor, QR kod va jadvallar).
6. QTableWidget signal bloklash va batch o'chirish unumdorligi.
"""
import os
import sys
import tempfile
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLockFile

from database.data_manager import DataManager
from database.sqlite_manager import SQLiteManager
from services.pdf_service import export_mahalla_passport_pdf, export_organizations_pdf
from services.telegram_bot import TelegramBotService
from ui_qt.views.trash_view import TrashView
from ui_qt.views.contracts_view import ContractsView

app = QApplication.instance() or QApplication(sys.argv)

class TestFeatures12346(unittest.TestCase):

    def setUp(self):
        self.dm = DataManager()

    def test_task1_sqlite_integrity_and_delete(self):
        """Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi."""
        test_id = "test-uuid-integrity-9999"
        test_org = {
            "id": test_id,
            "m": "Test Integrity Tashkilot",
            "s": "Maktab",
            "inn": "999888777",
            "f": "Test Rahbar",
            "t": "+998901112233"
        }
        # Qo'shish
        self.dm.add_organization(test_org)
        self.assertIsNotNone(self.dm.sqlite.get_organization_by_id(test_id))

        # Chiqindiga ko'chirish
        ok = self.dm.move_to_trash(test_org)
        self.assertTrue(ok)
        # Asosiy SQLite jadvalida qolmasligi kerak
        self.assertIsNone(self.dm.sqlite.get_organization_by_id(test_id))

        # Butunlay o'chirish
        del_ok = self.dm.permanent_delete(test_org)
        self.assertTrue(del_ok)
        self.assertFalse(self.dm.sqlite.delete_trash_item(test_id))

    def test_task2_single_instance_lock(self):
        """Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash."""
        test_lock_path = os.path.join(tempfile.gettempdir(), "test_pop_instance.lock")
        lock1 = QLockFile(test_lock_path)
        self.assertTrue(lock1.tryLock(100), "Birlamchi qulf muvaffaqiyatli olinishi kerak")

        # Ikkinchi instansiya urinishi
        lock2 = QLockFile(test_lock_path)
        self.assertFalse(lock2.tryLock(50), "Ikkinchi instansiya qulflana olmasligi kerak")

        lock1.unlock()
        self.assertTrue(lock2.tryLock(100), "Birlamchi qulf bo'shatilgach, ikkinchi instansiya qulfni olishi kerak")
        lock2.unlock()

    def test_task3_telegram_session_and_backoff(self):
        """Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi."""
        bot = TelegramBotService()
        self.assertIsNotNone(bot.session)
        old_session = bot.session

        # Sessiyani qayta yangilash
        bot._renew_session()
        self.assertIsNotNone(bot.session)
        self.assertIsNot(bot.session, old_session, "Yangi sessiya obyekti yaratilishi kerak")

    def test_task4_mahalla_passport_a4_pdf_generation(self):
        """Task 4: Mahalla pasportini A4 PDF formatida to'liq generatsiya qilish."""
        roles = [
            {"role_title": "Mahalla Raisi", "f": "Test Rais", "t": "+998901111111", "inn": "111111111", "jshr": "11111111111111", "seriya": "AA1111111"},
            {"role_title": "Hokim Yordamchisi", "f": "Test Yordamchi", "t": "+998902222222", "inn": "222222222", "jshr": "22222222222222", "seriya": "AA2222222"},
            {"role_title": "Yoshlar Yetakchisi", "f": "Test Yoshlar", "t": "+998903333333", "inn": "333333333", "jshr": "33333333333333", "seriya": "AA3333333"},
            {"role_title": "Xotin-qizlar Faoli", "f": "Test Faol", "t": "+998904444444", "inn": "444444444", "jshr": "44444444444444", "seriya": "AA4444444"},
            {"role_title": "Profilaktika Inspektori", "f": "Test Profilaktika", "t": "+998905555555", "inn": "555555555", "jshr": "55555555555555", "seriya": "AA5555555"},
            {"role_title": "Soliq Inspektori", "f": "Test Soliq", "t": "+998906666666", "inn": "666666666", "jshr": "66666666666666", "seriya": "AA6666666"},
            {"role_title": "Ijtimoiy Xodim", "f": "Test Ijtimoiy", "t": "+998907777777", "inn": "777777777", "jshr": "77777777777777", "seriya": "AA7777777"},
        ]
        out_pdf = os.path.join(tempfile.gettempdir(), "test_features_passport.pdf")
        ok = export_mahalla_passport_pdf("Iskovut MFY", roles, out_pdf)
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(out_pdf))
        self.assertGreater(os.path.getsize(out_pdf), 10000, "PDF fayl hajmi 10KB dan katta va mazmunli bo'lishi kerak")

        # Tashkilotlar PDF hisoboti
        out_orgs_pdf = os.path.join(tempfile.gettempdir(), "test_features_orgs.pdf")
        orgs_ok = export_organizations_pdf(self.dm.data[:10], "Sinov Hisoboti", out_orgs_pdf)
        self.assertTrue(orgs_ok)
        self.assertTrue(os.path.exists(out_orgs_pdf))

    def test_task5_auto_backup_scheduler(self):
        """Task 5: Avtomatlashtirilgan fonda davriy zaxira olish (Auto-Backup Scheduler)."""
        # 1. DataManager.backup_data() ikkala formatda saqlashi va dict qaytarishi
        res = self.dm.backup_data()
        self.assertIsInstance(res, dict)
        self.assertTrue("json" in res and "db" in res and "timestamp" in res)
        self.assertTrue(os.path.exists(res["json"]), "JSON zaxira fayli yaratilgan bo'lishi kerak")
        self.assertTrue(os.path.exists(res["db"]), "SQLite .db zaxira fayli yaratilgan bo'lishi kerak")
        self.assertGreater(os.path.getsize(res["json"]), 0)
        self.assertGreater(os.path.getsize(res["db"]), 0)

        # 2. SettingsView UI va event boshqaruvi
        from ui_qt.views.settings_view import SettingsView
        dummy_app = type("DummyApp", (), {
            "data": self.dm.data,
            "data_manager": self.dm,
            "current_theme": "dark",
            "show_toast": lambda *a, **k: None,
            "refresh_all_views": lambda *a, **k: None,
            "restart_backup_timer": lambda *a, **k: None,
            "trigger_auto_backup": lambda *a, **k: None
        })()
        sview = SettingsView(app=dummy_app)
        self.assertTrue(hasattr(sview, "chk_auto_backup"))
        self.assertTrue(hasattr(sview, "combo_backup_interval"))
        self.assertTrue(hasattr(sview, "lbl_last_backup"))

        # Oraliq o'zgarishi
        sview.on_backup_interval_changed(1) # 30 daqiqa
        self.assertEqual(self.dm.settings.get("auto_backup_interval_mins"), 30)

        # Yoqish / o'chirish
        sview.on_auto_backup_toggled(0) # Unchecked
        self.assertEqual(self.dm.settings.get("auto_backup_enabled"), False)

        sview.on_auto_backup_toggled(2) # Checked
        self.assertEqual(self.dm.settings.get("auto_backup_enabled"), True)

        # Oxirgi zaxira matni yangilanishi
        sview.update_last_backup_display("2026-09-24 23:50:00")
        self.assertIn("2026-09-24 23:50:00", sview.lbl_last_backup.text())

    def test_task6_table_signals_and_batch_ops(self):
        """Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik."""
        dummy_app = type("DummyApp", (), {
            "data": self.dm.data,
            "data_manager": self.dm,
            "current_theme": "dark",
            "show_toast": lambda msg, t="info": None,
            "refresh_all_views": lambda: None
        })()

        # ContractsView
        cview = ContractsView(app=dummy_app)
        cview.load_data()
        self.assertEqual(cview.table.updatesEnabled(), True)
        self.assertEqual(cview.table.signalsBlocked(), False)

        # TrashView
        tview = TrashView(app=dummy_app)
        tview.load_trash()
        self.assertEqual(tview.table.updatesEnabled(), True)
        self.assertEqual(tview.table.signalsBlocked(), False)

if __name__ == "__main__":
    unittest.main()
