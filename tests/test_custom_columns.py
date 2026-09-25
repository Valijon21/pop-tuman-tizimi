"""
tests/test_custom_columns.py: Dinamik ustunlar qo'shish va boshqarish bo'yicha birlik testlar.
"""
import unittest
import os
import tempfile
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QModelIndex

from ui_qt.components.table_model import OrganizationTableModel
from ui_qt.components.column_manager_dialog import ColumnManagerDialog
from database.sqlite_manager import SQLiteManager

app = QApplication.instance() or QApplication(sys.argv)

class TestCustomColumns(unittest.TestCase):
    """Dinamik ustunlar va ularning saqlanishi bo'yicha to'liq testlar."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_custom_col.db")
        self.sqlite = SQLiteManager(self.db_path)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_table_model_dynamic_columns(self):
        """OrganizationTableModel ga dinamik ustunlar qo'shish va o'qish."""
        data = [
            {"id": "1", "s": "Maktab", "m": "1-maktab", "f": "Direktor", "t": "+998901112233", "inn": "123456789", "izoh": "Test", "col_manzil": "Pop shahar, 5-uy"},
            {"id": "2", "s": "Bog'cha", "m": "2-bog'cha", "f": "Mudira", "t": "+998902223344", "inn": "987654321", "izoh": "", "col_manzil": "Chorkesar MFY"}
        ]
        model = OrganizationTableModel(data)
        self.assertEqual(model.columnCount(), 7)  # Standart 7 ustun

        # Maxsus ustun qo'shish
        custom_cols = [{"name": "Manzil", "key": "col_manzil", "width": 180}]
        model.set_custom_columns(custom_cols)
        self.assertEqual(model.columnCount(), 8)

        # HeaderData tekshirish
        header_title = model.headerData(7, Qt.Horizontal, Qt.DisplayRole)
        self.assertEqual(header_title, "Manzil")

        # Data tekshirish
        idx_row0_col7 = model.index(0, 7)
        self.assertEqual(model.data(idx_row0_col7, Qt.DisplayRole), "Pop shahar, 5-uy")

        idx_row1_col7 = model.index(1, 7)
        self.assertEqual(model.data(idx_row1_col7, Qt.DisplayRole), "Chorkesar MFY")

    def test_02_table_model_custom_cell_editing(self):
        """OrganizationTableModel da maxsus ustun katagini inline tahrirlash."""
        data = [
            {"id": "1", "s": "Maktab", "m": "1-maktab", "col_email": "old@maktab.uz"}
        ]
        model = OrganizationTableModel(data, custom_columns=[{"name": "Email", "key": "col_email", "width": 150}])

        saved_changes = []
        model.on_cell_changed = lambda it, k, v: saved_changes.append((it["id"], k, v))

        idx = model.index(0, 7)
        flags = model.flags(idx)
        self.assertTrue(bool(flags & Qt.ItemIsEditable))

        success = model.setData(idx, "yangi@maktab.uz", Qt.EditRole)
        self.assertTrue(success)
        self.assertEqual(data[0]["col_email"], "yangi@maktab.uz")
        self.assertEqual(len(saved_changes), 1)
        self.assertEqual(saved_changes[0], ("1", "col_email", "yangi@maktab.uz"))

    def test_03_table_model_sorting_custom_columns(self):
        """Maxsus ustunlar bo'yicha to'g'ri saralash."""
        data = [
            {"id": "1", "m": "B tashkilot", "col_shahar": "Zomin"},
            {"id": "2", "m": "A tashkilot", "col_shahar": "Andijon"},
            {"id": "3", "m": "C tashkilot", "col_shahar": "Buxoro"},
        ]
        model = OrganizationTableModel(data, custom_columns=[{"name": "Shahar", "key": "col_shahar", "width": 120}])

        # 7-ustun (Shahar) bo'yicha o'sish tartibida saralash
        model.sort(7, Qt.AscendingOrder)
        self.assertEqual(model._data[0]["col_shahar"], "Andijon")
        self.assertEqual(model._data[1]["col_shahar"], "Buxoro")
        self.assertEqual(model._data[2]["col_shahar"], "Zomin")

    def test_04_sqlite_ensure_column_exists_and_persistence(self):
        """SQLiteManager da yangi ustun ochish va ma'lumotlarni xatosiz saqlash."""
        cols_before = self.sqlite.get_table_columns("organizations")
        self.assertNotIn("col_test_hudud", cols_before)

        # Yangi ustun qo'shish
        ok = self.sqlite.ensure_column_exists("col_test_hudud", "TEXT")
        self.assertTrue(ok)

        cols_after = self.sqlite.get_table_columns("organizations")
        self.assertIn("col_test_hudud", cols_after)

        # Yangi ustun bilan yozuv kiritish
        org = {
            "id": "org-dyn-1",
            "s": "Tibbiyot",
            "m": "Tuman shifoxonasi",
            "inn": "777888999",
            "col_test_hudud": "Markaziy bino, 2-qavat"
        }
        self.sqlite.insert_or_replace_organization(org)

        loaded = self.sqlite.get_organization_by_id("org-dyn-1")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.get("col_test_hudud"), "Markaziy bino, 2-qavat")

    def test_05_column_manager_dialog(self):
        """ColumnManagerDialog komponenti to'g'ri ishlashi."""
        dlg = ColumnManagerDialog(view_type="table", current_columns=[{"name": "Eski", "key": "col_eski", "width": 100}])
        self.assertEqual(len(dlg.columns), 1)

        # Maxsus ustun qo'shish
        dlg.edit_custom_name.setText("Qarzdorlik Holati")
        dlg.spin_width.setValue(160)
        dlg.add_custom_field()

        self.assertEqual(len(dlg.columns), 2)
        added_col = dlg.columns[1]
        self.assertEqual(added_col["name"], "Qarzdorlik Holati")
        self.assertEqual(added_col["width"], 160)
        self.assertTrue(added_col["key"].startswith("col_"))

        # O'chirish
        dlg.remove_column(0)
        self.assertEqual(len(dlg.columns), 1)
        self.assertEqual(dlg.columns[0]["name"], "Qarzdorlik Holati")
        dlg.close()

if __name__ == "__main__":
    unittest.main()
