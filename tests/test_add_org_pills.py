"""
tests/test_add_org_pills.py: Toifalar qatorida tashkilot qo'shish va yangi toifa kiritish testlari.
"""
import unittest
import os
import tempfile
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from database.data_manager import DataManager
from database.sqlite_manager import SQLiteManager
from ui_qt.views.contracts_view import ContractsView
from ui_qt.views.table_view import TableView
from ui_qt.views.contract_add_dialog import ContractAddDialog
from ui_qt.views.org_edit_dialog import OrgEditDialog

app = QApplication.instance() or QApplication(sys.argv)


class MockApp:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.data = data_manager.data
        self.current_theme = "dark"
        self.font_size = 14

    def check_permission(self, action="edit", parent=None):
        return True

    def refresh_all_views(self):
        pass

    def show_toast(self, msg, t="info"):
        pass


class TestAddOrgPills(unittest.TestCase):
    """Toifalar qatorida tashkilot va toifa qo'shish testlari."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = os.path.join(self.temp_dir.name, "test_mahalla.json")
        self.trash_file = os.path.join(self.temp_dir.name, "test_trash.json")
        self.categories_file = os.path.join(self.temp_dir.name, "test_categories.json")
        self.log_file = os.path.join(self.temp_dir.name, "test_log.json")
        self.settings_file = os.path.join(self.temp_dir.name, "test_settings.json")
        self.sqlite_db = os.path.join(self.temp_dir.name, "test_sqlite.db")
        self.backup_dir = os.path.join(self.temp_dir.name, "backups")

        self.dm = DataManager(
            db_file=self.db_file,
            trash_file=self.trash_file,
            categories_file=self.categories_file,
            log_file=self.log_file,
            settings_file=self.settings_file,
            sqlite_file=self.sqlite_db,
            backup_dir=self.backup_dir
        )
        self.dm.data = [
            {"id": "1", "s": "Maktab", "m": "1-maktab", "inn": "111222333", "aparat_soni": 5, "ulangan_soni": 3, "bux_tel": "+998901234567"},
            {"id": "2", "s": "Bog'cha", "m": "2-bog'cha", "inn": "222333444", "aparat_soni": 2, "ulangan_soni": 1, "bux_tel": "+998907654321"}
        ]
        self.dm.save_data()
        self.mock_app = MockApp(self.dm)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_data_manager_add_category(self):
        """DataManager orqali yangi toifa qo'shish va saqlanishi."""
        initial_count = len(self.dm.categories)
        self.assertNotIn("Sport va Madaniyat", self.dm.categories)

        ok = self.dm.add_category("Sport va Madaniyat")
        self.assertTrue(ok)
        self.assertEqual(len(self.dm.categories), initial_count + 1)
        self.assertIn("Sport va Madaniyat", self.dm.categories)

        # Takroriy qo'shish rad etilishi kerak
        ok_dup = self.dm.add_category("Sport va Madaniyat")
        self.assertFalse(ok_dup)

    def test_02_contracts_view_pills_buttons(self):
        """ContractsView da toifalar qatorida Tashkilot qo'shish va Toifa tugmalari mavjudligi."""
        view = ContractsView(app=self.mock_app)
        view.load_data()

        # Tugmalar yaratilganligini tekshirish
        self.assertTrue(hasattr(view, "btn_pill_add"))
        self.assertTrue(hasattr(view, "btn_pill_add_cat"))
        self.assertEqual(view.btn_pill_add.text(), "➕ Tashkilot qo'shish")
        self.assertEqual(view.btn_pill_add_cat.text(), "+ Toifa")

        # Shortcut Ctrl+N mavjudligini tekshirish
        self.assertTrue(hasattr(view, "shortcut_add"))
        self.assertEqual(view.shortcut_add.key().toString(), "Ctrl+N")

    def test_03_table_view_pills_buttons(self):
        """TableView da toifalar qatorida Tashkilot qo'shish va Toifa tugmalari mavjudligi."""
        view = TableView(app=self.mock_app)
        view.init_data()

        # Tugmalar yaratilganligini tekshirish
        self.assertTrue(hasattr(view, "btn_pill_add"))
        self.assertTrue(hasattr(view, "btn_pill_add_cat"))
        self.assertEqual(view.btn_pill_add.text(), "➕ Tashkilot qo'shish")
        self.assertEqual(view.btn_pill_add_cat.text(), "+ Toifa")

        # Shortcut Ctrl+N mavjudligini tekshirish
        self.assertTrue(hasattr(view, "shortcut_add"))
        self.assertEqual(view.shortcut_add.key().toString(), "Ctrl+N")

    def test_04_contract_add_dialog_prefilled_category(self):
        """ContractAddDialog yangi tashkilot rejimida toifani to'g'ri qabul qilishi."""
        init_item = {"_is_new": True, "s": "Bog'cha"}
        dlg = ContractAddDialog(app=self.mock_app, item=init_item)

        self.assertFalse(dlg.is_edit)
        self.assertEqual(dlg.combo_category.currentText(), "Bog'cha")

    def test_05_org_edit_dialog_prefilled_category(self):
        """OrgEditDialog yangi tashkilot rejimida toifani to'g'ri qabul qilishi."""
        init_item = {"_is_new": True, "s": "Maktab"}
        dlg = OrgEditDialog(app=self.mock_app, item=init_item)

        self.assertFalse(dlg.is_edit)
        self.assertEqual(dlg.combo_type.currentText(), "Maktab")


if __name__ == "__main__":
    unittest.main()
