import unittest
import os
import json
import tempfile
import shutil
from database.data_manager import DataManager

class TestDataManager(unittest.TestCase):
    """Ma'lumotlar ombori boshqaruvi va atomik saqlash testlari (Isolated)."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_db.json")
        self.trash_path = os.path.join(self.test_dir, "test_trash.json")
        self.settings_path = os.path.join(self.test_dir, "test_settings.json")
        self.log_path = os.path.join(self.test_dir, "test_log.json")
        self.categories_path = os.path.join(self.test_dir, "test_categories.json")
        self.backup_path = os.path.join(self.test_dir, "backups")

        # Boshlang'ich test bazasi
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump([{"id": "uuid-1", "m": "MFY 1", "inn": "111"}], f)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def get_test_dm(self) -> DataManager:
        return DataManager(
            db_file=self.db_path,
            trash_file=self.trash_path,
            categories_file=self.categories_path,
            log_file=self.log_path,
            settings_file=self.settings_path,
            backup_dir=self.backup_path
        )

    def test_atomic_save_and_load(self):
        dm = self.get_test_dm()
        sample_data = [{"id": "item-1", "m": "Test Tashkilot", "inn": "123456789"}]

        # Atomik saqlash
        dm.save_json(self.db_path, sample_data)
        self.assertTrue(os.path.exists(self.db_path))

        # Qayta o'qish
        loaded = dm.load_json(self.db_path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "item-1")
        self.assertEqual(loaded[0]["m"], "Test Tashkilot")

    def test_move_and_restore_trash(self):
        dm = self.get_test_dm()
        self.assertEqual(len(dm.data), 1)
        self.assertEqual(len(dm.trash), 0)

        # 1. Chiqindiga tashlash
        success = dm.move_to_trash(dm.data[0])
        self.assertTrue(success)
        self.assertEqual(len(dm.data), 0)
        self.assertEqual(len(dm.trash), 1)
        self.assertEqual(dm.trash[0]["id"], "uuid-1")
        self.assertIn("deleted_at", dm.trash[0])

        # 2. Chiqindidan tiklash
        success = dm.restore_from_trash(dm.trash[0])
        self.assertTrue(success)
        self.assertEqual(len(dm.data), 1)
        self.assertEqual(len(dm.trash), 0)
        self.assertEqual(dm.data[0]["id"], "uuid-1")
        self.assertNotIn("deleted_at", dm.data[0])

        # 3. Butunlay o'chirish
        dm.move_to_trash(dm.data[0])
        self.assertEqual(len(dm.trash), 1)
        perm_ok = dm.permanent_delete(dm.trash[0])
        self.assertTrue(perm_ok)
        self.assertEqual(len(dm.trash), 0)

    def test_add_and_update_organization(self):
        dm = self.get_test_dm()
        initial_len = len(dm.data)

        # 1. Yangi tashkilot qo'shish
        new_org = {
            "m": "Yangi Test MFY",
            "s": "Mahalla (MFY)",
            "inn": "305123987",
            "f": "Alimov Jamshid",
            "t": "+998901234567"
        }
        added = dm.add_organization(new_org)
        self.assertIn("id", added)
        self.assertEqual(len(dm.data), initial_len + 1)
        self.assertIn("updated_at", added)

        # 2. Mavjud tashkilotni tahrirlash
        added["f"] = "Alimov Jamshid Yangilangan"
        added["bux_tel"] = "94 592 60 04"
        success = dm.update_organization(added)
        self.assertTrue(success)

        # Qayta o'qish (load_data)
        reloaded = dm.load_data()
        updated_item = next((i for i in reloaded if i.get("id") == added["id"]), None)
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item["f"], "Alimov Jamshid Yangilangan")
        self.assertEqual(updated_item["bux_tel"], "94 592 60 04")

    def test_add_and_update_organization_model(self):
        from database.models import Organization
        dm = self.get_test_dm()
        org = Organization(
            m="Model Maktab",
            s="Maktab",
            inn="309876543",
            f="Qodirov Botir",
            lavozim="Direktor",
            bux_tel="+998901234567",
            aparat_soni=20,
            ulangan_soni=15
        )
        added = dm.add_organization(org)
        self.assertEqual(added["m"], "Model Maktab")
        self.assertEqual(added["lavozim"], "Direktor")

        # get_organization_model orqali qayta olish
        model = dm.get_organization_model(org.id)
        self.assertIsNotNone(model)
        self.assertEqual(model.m, "Model Maktab")
        self.assertEqual(model.lavozim, "Direktor")
        self.assertEqual(model.aparat_soni, 20)

        # Modelni yangilash
        model.lavozim = "Bosh Direktor"
        model.aparat_soni = 25
        upd_ok = dm.update_organization(model)
        self.assertTrue(upd_ok)

        reloaded_model = dm.get_organization_model(org.id)
        self.assertEqual(reloaded_model.lavozim, "Bosh Direktor")
        self.assertEqual(reloaded_model.aparat_soni, 25)

if __name__ == "__main__":
    unittest.main()
