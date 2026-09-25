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
        from ui_qt.views.contracts_view import ContractsView
        from ui_qt.views.trash_view import TrashView
        from ui_qt.views.settings_view import SettingsView
        from ui_qt.views.dashboard_view import DashboardView
        from ui_qt.views.table_view import TableView
        from ui_qt.views.contract_add_dialog import ContractAddDialog
        from ui_qt.views.qr_dialog import QRDialog
        from ui_qt.views.password_dialog import PasswordPromptDialog, request_password
        from ui_qt.app_window import MainWindow

        self.assertIsNotNone(OrgEditDialog)
        self.assertIsNotNone(CabinetDialog)
        self.assertIsNotNone(VerificationDialog)
        self.assertIsNotNone(MahallaPassportView)
        self.assertIsNotNone(BroadcastView)
        self.assertIsNotNone(HistoryView)
        self.assertIsNotNone(ImportDialog)
        self.assertIsNotNone(ContractsView)
        self.assertIsNotNone(TrashView)
        self.assertIsNotNone(SettingsView)
        self.assertIsNotNone(DashboardView)
        self.assertIsNotNone(TableView)
        self.assertIsNotNone(ContractAddDialog)
        self.assertIsNotNone(QRDialog)
        self.assertIsNotNone(PasswordPromptDialog)
        self.assertIsNotNone(request_password)
        self.assertIsNotNone(MainWindow)

    def test_password_permission_check(self):
        from ui_qt.views.password_dialog import PasswordPromptDialog, request_password

        class MockDataMgr:
            settings = {"passwords": {}}

        class MockApp:
            current_theme = "dark"
            font_size = 12
            data_manager = MockDataMgr()
            _session_authenticated = {}

        mock_app = MockApp()
        # Offscreen yoki sessiya avtorizatsiyasida True qaytarishi kerak
        self.assertTrue(request_password(None, mock_app, action="edit"))
        self.assertTrue(request_password(None, mock_app, action="settings"))

        dlg = PasswordPromptDialog(parent=None, app=mock_app, action="edit")
        self.assertEqual(dlg.action, "edit")
        dlg.edit_pwd.setText("1234567")
        dlg.submit_password()
        self.assertTrue(mock_app._session_authenticated.get("edit", False))
        dlg.close()

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

    def test_dashboard_charts_and_cards(self):
        from ui_qt.components.widgets import (
            ClickableCard, CategoryDonutChart, CategoryLegend, CategoryBarChart
        )
        # 1. ClickableCard
        card = ClickableCard()
        clicked_flag = []
        card.clicked.connect(lambda: clicked_flag.append(True))
        card.clicked.emit()
        self.assertTrue(clicked_flag)

        # 2. CategoryDonutChart
        donut = CategoryDonutChart()
        test_data = [
            ("Mahalla (MFY)", 74, "#10b981"),
            ("Maktablar", 76, "#f59e0b"),
            ("Bog'chalar (MTT)", 57, "#8b5cf6"),
        ]
        donut.set_data(test_data)
        self.assertEqual(donut.total, 207)
        self.assertEqual(len(donut.segments), 3)

        # 3. CategoryLegend
        legend = CategoryLegend()
        selected_cat = []
        legend.category_selected.connect(lambda c: selected_cat.append(c))
        legend.set_data(test_data)
        self.assertTrue(legend.layout.count() > 0)

        # 4. CategoryBarChart
        bars = CategoryBarChart()
        bars.set_data(test_data)
        self.assertTrue(bars.layout.count() > 0)

    def test_org_edit_dialog_instantiation(self):
        from ui_qt.views.org_edit_dialog import OrgEditDialog
        # Test add new dialog
        dlg_add = OrgEditDialog()
        self.assertIsNotNone(dlg_add)
        self.assertFalse(dlg_add.is_edit)

        # Test edit existing dialog
        sample_org = {
            "s": "Maktab",
            "m": "22-sonli Maktab",
            "f": "Dehqanova Azimaxon",
            "t": "+998901234567",
            "inn": "206907205",
            "jshr": "30807995910027",
            "seriya": "AB4561091",
            "lavozim": "Direktor",
            "izoh": "Test maktab"
        }
        dlg_edit = OrgEditDialog(item=sample_org)
        self.assertIsNotNone(dlg_edit)
        self.assertTrue(dlg_edit.is_edit)
        self.assertEqual(dlg_edit.edit_inn.text(), "206907205")
        self.assertEqual(dlg_edit.edit_name.text(), "22-sonli Maktab")

    def test_main_window_instantiation(self):
        from ui_qt.app_window import MainWindow
        win = MainWindow()
        self.assertIsNotNone(win)
        self.assertEqual(win.content_stack.count(), 6)
        self.assertIsNotNone(win.contracts_view)
        self.assertIsNotNone(win.apps_view)
        win.show_apps()
        self.assertEqual(win.content_stack.currentIndex(), 5)
        win.close()

    def test_apps_view(self):
        """Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash."""
        from ui_qt.views.apps_view import AppsView
        view = AppsView()
        self.assertIsNotNone(view)
        self.assertTrue(hasattr(view, "btn_run_uzcrypto"))
        self.assertTrue(hasattr(view, "btn_run_anydesk"))
        self.assertTrue(hasattr(view, "btn_folder_uzcrypto"))
        self.assertTrue(hasattr(view, "btn_folder_anydesk"))
        view.refresh_status()
        view.set_theme("light")
        view.set_theme("dark")
        view.close()
    def test_theme_toggle_updates_dashboard(self):
        from ui_qt.app_window import MainWindow
        win = MainWindow()
        self.assertEqual(win.current_theme, "dark")
        self.assertEqual(win.dashboard_view.current_theme, "dark")
        self.assertEqual(win.dashboard_view.donut_chart.theme, "dark")
        self.assertEqual(win.dashboard_view.legend.theme, "dark")
        self.assertEqual(win.dashboard_view.bar_chart.theme, "dark")

        # Tungi -> Kunduzgi rejimga o'tish
        win.toggle_theme()
        self.assertEqual(win.current_theme, "light")
        self.assertEqual(win.dashboard_view.current_theme, "light")
        self.assertEqual(win.dashboard_view.donut_chart.theme, "light")
        self.assertEqual(win.dashboard_view.legend.theme, "light")
        self.assertEqual(win.dashboard_view.bar_chart.theme, "light")
        self.assertEqual(win.btn_theme.text(), "🌙 Tungi Rejim")

        # Kunduzgi -> Tungi rejimga qaytish
        win.toggle_theme()
        self.assertEqual(win.current_theme, "dark")
        self.assertEqual(win.dashboard_view.current_theme, "dark")
        self.assertEqual(win.dashboard_view.donut_chart.theme, "dark")
        self.assertEqual(win.dashboard_view.legend.theme, "dark")
        self.assertEqual(win.dashboard_view.bar_chart.theme, "dark")
        self.assertEqual(win.btn_theme.text(), "☀ Kunduzi Rejim")

        win.close()

    def test_dashboard_stat_cards_layout_and_styling(self):
        """Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'ri ekanligini tekshirish."""
        from ui_qt.views.dashboard_view import DashboardView
        from PyQt5.QtWidgets import QLabel

        class MockApp:
            current_theme = "dark"
            data = [
                {"s": "Mahalla (MFY)", "m": "Chorkesar MFY", "f": "Yondashev X.", "t": "+998901234567", "inn": "203599806"},
                {"s": "Maktab", "m": "22-sonli Maktab", "f": "Dehqanova A.", "t": "+998912345678", "inn": "206907205"},
                {"s": "Bog'cha (MTT)", "m": "1-MTT", "f": "Karimova", "t": "+998901112233", "inn": "201111222"},
                {"s": "Tibbiyot", "m": "1-Shifoxona", "f": "Aliyev", "t": "+998902223344", "inn": "203333444"},
                {"s": "Boshqa", "m": "Kutubxona", "f": "Valiyev", "t": "+998903334455", "inn": "205555666"},
            ]
            def filter_by_category(self, cat): pass

        mock_app = MockApp()
        view = DashboardView(app=mock_app)

        # 6 ta karta mavjudligini tekshirish
        self.assertEqual(view.cards_grid.count(), 6)

        # Har bir kartaning balandligi va ichki ikonkasini tekshirish
        for i in range(view.cards_grid.count()):
            card = view.cards_grid.itemAt(i).widget()
            self.assertIsNotNone(card)
            self.assertGreaterEqual(card.minimumHeight(), 85)

            # Ikonkani topish (o'ng yuqoridagi 30x30 squircle)
            labels = card.findChildren(QLabel)
            icon_lbl = next(l for l in labels if l.width() == 30 and l.height() == 30)
            self.assertIsNotNone(icon_lbl)
            self.assertEqual(icon_lbl.width(), 30)
            self.assertEqual(icon_lbl.height(), 30)
            # Rang formati rgba bo'lishi kerak, noto'g'ri #hex22 emas
            self.assertIn("rgba(", icon_lbl.styleSheet())
            self.assertNotIn("22;", icon_lbl.styleSheet())

        # Light mavzuga o'tkazganda ham to'g'ri ishlashi
        view.set_theme("light")
        self.assertEqual(view.cards_grid.count(), 6)
        card_light = view.cards_grid.itemAt(0).widget()
        self.assertGreaterEqual(card_light.minimumHeight(), 85)
        labels_light = card_light.findChildren(QLabel)
        icon_light = next(l for l in labels_light if l.width() == 30 and l.height() == 30)
        self.assertEqual(icon_light.width(), 30)
        self.assertIn("rgba(", icon_light.styleSheet())
        self.assertNotIn("22;", icon_light.styleSheet())

    def test_dialogs_light_theme(self):
        """Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tekshirish."""
        from ui_qt.views.mahalla_passport_view import MahallaPassportView
        from ui_qt.views.broadcast_view import BroadcastView
        from ui_qt.views.cabinet_dialog import CabinetDialog
        from ui_qt.views.verification_dialog import VerificationDialog
        from ui_qt.views.org_edit_dialog import OrgEditDialog
        from ui_qt.views.history_view import HistoryView
        from ui_qt.views.import_dialog import ImportDialog

        class MockApp:
            current_theme = "light"
            data = [
                {"s": "Mahalla (MFY)", "m": "Yangi to'da MFY", "f": "O'ralov O'", "t": "+998939466283", "inn": "202701806"}
            ]
            def show_toast(self, msg, t="info"): pass

        mock_app = MockApp()

        # 1. Mahalla Passport
        dlg_passport = MahallaPassportView(app=mock_app, selected_mahalla="Yangi to'da MFY")
        self.assertEqual(dlg_passport.current_theme, "light")
        self.assertIn("#f8fafc", dlg_passport.styleSheet())
        dlg_passport.close()

        # 2. Broadcast
        dlg_broadcast = BroadcastView(app=mock_app)
        self.assertEqual(dlg_broadcast.current_theme, "light")
        self.assertIn("#f8fafc", dlg_broadcast.styleSheet())
        dlg_broadcast.close()

        # 3. Cabinet
        dlg_cab = CabinetDialog(app=mock_app, item=mock_app.data[0])
        self.assertEqual(dlg_cab.current_theme, "light")
        self.assertIn("#f8fafc", dlg_cab.styleSheet())
        dlg_cab.close()

        # 4. Verification
        dlg_verif = VerificationDialog(app=mock_app, item=mock_app.data[0])
        self.assertEqual(dlg_verif.current_theme, "light")
        self.assertIn("#f8fafc", dlg_verif.styleSheet())
        dlg_verif.close()

        # 5. Org Edit
        dlg_edit = OrgEditDialog(app=mock_app, item=mock_app.data[0])
        self.assertEqual(dlg_edit.current_theme, "light")
        self.assertIn("#f8fafc", dlg_edit.styleSheet())
        dlg_edit.close()

        # 6. History
        dlg_hist = HistoryView(app=mock_app, mahalla="Yangi to'da MFY")
        self.assertEqual(dlg_hist.current_theme, "light")
        self.assertIn("#f8fafc", dlg_hist.styleSheet())
        dlg_hist.close()

        # 7. Import
        dlg_imp = ImportDialog(app=mock_app)
        self.assertEqual(dlg_imp.current_theme, "light")
        self.assertIn("#f8fafc", dlg_imp.styleSheet())
        dlg_imp.close()

    def test_fast_tab_navigation(self):
        """Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini tekshirish."""
        from ui_qt.app_window import MainWindow
        win = MainWindow()

        # Dastlabki holat
        self.assertEqual(win.content_stack.currentIndex(), 0)

        # Ro'yxat jadvaliga o'tish
        win.show_table()
        self.assertEqual(win.content_stack.currentIndex(), 1)
        self.assertFalse(win._dirty_views["table"])

        # Shartnomalarga o'tish
        win.show_contracts()
        self.assertEqual(win.content_stack.currentIndex(), 2)
        self.assertFalse(win._dirty_views["contracts"])

        # Dashboardga qaytish
        win.show_dashboard()
        self.assertEqual(win.content_stack.currentIndex(), 0)
        self.assertFalse(win._dirty_views["dashboard"])

        # Sozlamalarga o'tish
        win.show_settings()
        self.assertEqual(win.content_stack.currentIndex(), 4)
        self.assertFalse(win._dirty_views["settings"])

        win.close()

    def test_qr_dialog_view(self):
        """QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish."""
        from ui_qt.views.qr_dialog import QRDialog
        sample_item = {
            "m": "Chorkesar MFY",
            "f": "Karimov Sardor",
            "s": "Mahalla Raisi",
            "t": "+998901234567",
            "inn": "301234567"
        }
        dlg = QRDialog(phone="+998901234567", item=sample_item)
        self.assertEqual(dlg.current_mode, "tel")
        self.assertIsNotNone(dlg.current_pil_img)
        self.assertIsNotNone(dlg.lbl_qr_image.pixmap())

        # vCard rejimiga o'tkazish
        dlg.rad_vcard.setChecked(True)
        self.assertEqual(dlg.current_mode, "vcard")
        self.assertIsNotNone(dlg.current_pil_img)

        dlg.close()

    def test_contract_add_dialog(self):
        """Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini tekshirish."""
        from ui_qt.views.contract_add_dialog import ContractAddDialog
        # 1. Yangi qo'shish rejimi
        dlg_add = ContractAddDialog()
        self.assertIsNotNone(dlg_add)
        self.assertFalse(dlg_add.is_edit)
        dlg_add.close()

        # 2. Tahrirlash rejimi
        sample_contract = {
            "id": 999,
            "organization_name": "Test Tashkilot",
            "inn": "123456789",
            "contract_number": "SH-2024/01",
            "apparat_count": 5,
            "connected_count": 3,
            "accountant_phone": "+998901234567",
            "notes": "Test shartnoma"
        }
        dlg_edit = ContractAddDialog(item=sample_contract)
        self.assertIsNotNone(dlg_edit)
        self.assertTrue(dlg_edit.is_edit)
        self.assertEqual(dlg_edit.edit_inn.text(), "123456789")
        self.assertEqual(dlg_edit.edit_name.text(), "Test Tashkilot")
        self.assertEqual(dlg_edit.spin_aparat.value(), 5)
        self.assertEqual(dlg_edit.spin_ulangan.value(), 3)
        dlg_edit.close()

if __name__ == "__main__":
    unittest.main()

