import unittest
import os
import tempfile
from database.sqlite_manager import SQLiteManager

class TestSQLiteManager(unittest.TestCase):
    """SQLite Manager ACID va Ma'lumotlar Bazasi Testlari."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_mahalla.db")
        self.manager = SQLiteManager(self.db_path)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_database_initialization(self):
        """Jadvallar to'g'ri yaratilganligini tekshirish."""
        self.assertTrue(os.path.exists(self.db_path))
        items = self.manager.get_all_organizations()
        self.assertEqual(items, [])

    def test_bulk_insert_and_get_all(self):
        """Ommaviy yozuv qo'shish va barchasini olish testi."""
        sample_data = [
            {
                "id": "org-1",
                "s": "Mahalla (MFY)",
                "m": "Chorkesar MFY",
                "f": "Yondashev Xojiakbar",
                "t": "+998901234567",
                "inn": "203599806",
                "jshr": "30807995910027",
                "seriya": "AB4561091",
                "izoh": "Test tashkilot"
            },
            {
                "id": "org-2",
                "s": "Maktab",
                "m": "1-maktab",
                "f": "Karimov Anvar",
                "t": "+998911112233",
                "inn": "201234567",
                "izoh": ""
            }
        ]
        count = self.manager.bulk_insert_organizations(sample_data)
        self.assertEqual(count, 2)

        retrieved = self.manager.get_all_organizations()
        self.assertEqual(len(retrieved), 2)
        by_inn = self.manager.get_organization_by_inn("203599806")
        self.assertIsNotNone(by_inn)
        self.assertEqual(by_inn.get("m"), "Chorkesar MFY")
        self.assertEqual(by_inn.get("jshr"), "30807995910027")

    def test_upsert_and_delete(self):
        """Yozuvni kiritish, yangilash va o'chirish."""
        item = {
            "id": "org-single",
            "s": "Bog'cha",
            "m": "5-MTT",
            "f": "Aliyeva Nargiza",
            "t": "+998933334455",
            "inn": "301999888"
        }
        self.manager.upsert_organization(item)
        res = self.manager.get_organization_by_id("org-single")
        self.assertIsNotNone(res)
        self.assertEqual(res["m"], "5-MTT")

        # Yangilash
        item["m"] = "5-sonli Davlat Maktabgacha Ta'lim Tashkiloti"
        self.manager.upsert_organization(item)
        res2 = self.manager.get_organization_by_id("org-single")
        self.assertEqual(res2["m"], "5-sonli Davlat Maktabgacha Ta'lim Tashkiloti")

        # O'chirish
        self.manager.delete_organization("org-single")
        self.assertIsNone(self.manager.get_organization_by_id("org-single"))

    def test_staff_history(self):
        """Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish."""
        self.manager.add_staff_history(
            org_id="org-10",
            org_name="Yakkatut MFY",
            mahalla="Yakkatut MFY",
            role="Hokim yordamchisi",
            old_fio="Sobiq Xodim Olim",
            new_fio="Yangi Xodim Botir",
            old_phone="+998901111111",
            new_phone="+998902222222",
            changed_by="admin",
            reason="Navbatdagi rotatsiya"
        )

        history = self.manager.get_staff_history(mahalla="Yakkatut MFY")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["old_fio"], "Sobiq Xodim Olim")
        self.assertEqual(history[0]["new_fio"], "Yangi Xodim Botir")
        self.assertEqual(history[0]["changed_by"], "admin")

    def test_backup_database(self):
        """Zaxira nusxa yaratish funksiyasini tekshirish."""
        item = {"id": "org-bk", "m": "Test Backup", "inn": "999888777"}
        self.manager.upsert_organization(item)
        backup_path = self.manager.backup_database()
        self.assertTrue(os.path.exists(backup_path))
        self.assertGreater(os.path.getsize(backup_path), 0)

if __name__ == "__main__":
    unittest.main()
