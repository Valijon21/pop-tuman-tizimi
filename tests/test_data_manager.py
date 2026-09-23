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

if __name__ == "__main__":
    unittest.main()
