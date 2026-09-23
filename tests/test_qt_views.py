"""
tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtirilgan testlari.
"""
import unittest
import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Offscreen (boshsiz) rejimda ishlash uchun platformani o'rnatish
os.environ["QT_QPA_PLATFORM"] = "offscreen"
app = QApplication.instance() or QApplication(sys.argv)

class TestQtArchitecture(unittest.TestCase):
    """PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash."""

    def test_styles_generation(self):
        from ui_qt.styles import get_stylesheet
        dark = get_stylesheet("dark")
        light = get_stylesheet("light")
        self.assertIn("QMainWindow", dark)
        self.assertIn("#0f172a", dark)
        self.assertIn("QMainWindow", light)
        self.assertIn("#f8fafc", light)

    def test_table_model(self):
        from ui_qt.components.table_model import OrganizationTableModel
        sample_data = [
            {"s": "Mahalla (MFY)", "m": "Chorkesar MFY", "f": "Yondashev X.", "t": "+998901234567", "inn": "203599806", "izoh": "Aktiv"},
            {"s": "Maktab", "m": "22-sonli Maktab", "f": "Dehqanova A.", "t": "+998912345678", "inn": "206907205", "izoh": ""},
        ]
        model = OrganizationTableModel(sample_data)
        self.assertEqual(model.rowCount(), 2)
        self.assertEqual(model.columnCount(), 7)

        # Headerlar
        self.assertEqual(model.headerData(0, Qt.Horizontal), "№")
        self.assertEqual(model.headerData(2, Qt.Horizontal), "Tashkilot Nomi")
        self.assertEqual(model.headerData(5, Qt.Horizontal), "INN")

        # Qator ma'lumotlari
        idx_0 = model.index(0, 2)
        self.assertEqual(model.data(idx_0, Qt.DisplayRole), "Chorkesar MFY")

        idx_1 = model.index(1, 5)
        self.assertEqual(model.data(idx_1, Qt.DisplayRole), "206907205")

        # Saralash
        model.sort(5, Qt.AscendingOrder)
        self.assertEqual(model.get_item_by_row(0)["m"], "Chorkesar MFY")

        model.sort(5, Qt.DescendingOrder)
        self.assertEqual(model.get_item_by_row(0)["m"], "22-sonli Maktab")

    def test_view_imports(self):
        from ui_qt.views.org_edit_dialog import OrgEditDialog
        from ui_qt.views.cabinet_dialog import CabinetDialog, copy_cabinet_quick
        from ui_qt.views.verification_dialog import VerificationDialog, copy_verification_quick
        from ui_qt.views.mahalla_passport_view import MahallaPassportView
        from ui_qt.views.broadcast_view import BroadcastView
        from ui_qt.views.history_view import HistoryView
        from ui_qt.views.import_dialog import ImportDialog
        from ui_qt.views.trash_view import TrashView
        from ui_qt.views.settings_view import SettingsView
        from ui_qt.views.dashboard_view import DashboardView
        from ui_qt.views.table_view import TableView
        from ui_qt.app_window import MainWindow

        self.assertIsNotNone(OrgEditDialog)
        self.assertIsNotNone(CabinetDialog)
        self.assertIsNotNone(VerificationDialog)
        self.assertIsNotNone(MahallaPassportView)
        self.assertIsNotNone(BroadcastView)
        self.assertIsNotNone(HistoryView)
        self.assertIsNotNone(ImportDialog)
        self.assertIsNotNone(TrashView)
        self.assertIsNotNone(SettingsView)
        self.assertIsNotNone(DashboardView)
        self.assertIsNotNone(TableView)
        self.assertIsNotNone(MainWindow)

    def test_cabinet_quick_copy(self):
        from ui_qt.views.cabinet_dialog import copy_cabinet_quick
        import pyperclip

        class MockApp:
            def show_toast(self, msg, t="info"): pass

        mock_app = MockApp()
        sample = {"m": "22-Maktab", "inn": "206907205", "f": "Azimaxon"}
        copy_cabinet_quick(mock_app, sample)
        copied = pyperclip.paste()
        self.assertIn("22-Maktab", copied)
        self.assertIn("cabinetga dostup", copied)

    def test_verification_quick_copy(self):
        from ui_qt.views.verification_dialog import copy_verification_quick
        import pyperclip

        class MockApp:
            def show_toast(self, msg, t="info"): pass

        mock_app = MockApp()
        sample = {
            "m": "Chorkesar MFY", "inn": "203599806",
            "f": "Yondashev Xojiakbar", "jshr": "30807995910027",
            "seriya": "AB4561091", "lavozim": "Hokim yordamchisi"
        }
        copy_verification_quick(mock_app, sample)
        copied = pyperclip.paste()
        self.assertIn("Chorkesar MFY", copied)
        self.assertIn("verfikatsiya bervoring", copied)
        self.assertIn("30807995910027", copied)

    def test_main_window_instantiation(self):
        from ui_qt.app_window import MainWindow
        win = MainWindow()
        self.assertIsNotNone(win)
        self.assertEqual(win.content_stack.count(), 4)
        win.show_table()
        self.assertEqual(win.content_stack.currentIndex(), 1)
        win.show_dashboard()
        self.assertEqual(win.content_stack.currentIndex(), 0)
        win.close()

if __name__ == "__main__":
    unittest.main()
