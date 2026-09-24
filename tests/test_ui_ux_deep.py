"""
Comprehensive UI/UX Deep Testing & Verification Script
Simulates loading all views, switching themes, scaling fonts, clicking buttons, opening dialogs.
Runs headless using offscreen Qt platform.
"""
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui_qt.app_window import MainWindow
from ui_qt.views.org_edit_dialog import OrgEditDialog
from ui_qt.views.cabinet_dialog import CabinetDialog
from ui_qt.views.verification_dialog import VerificationDialog
from ui_qt.views.qr_dialog import QRDialog
from ui_qt.views.import_dialog import ImportDialog
from ui_qt.views.contract_add_dialog import ContractAddDialog
from ui_qt.views.mahalla_passport_view import MahallaPassportView
from ui_qt.styles import get_stylesheet

class TestUIUXDeep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if not cls.app:
            cls.app = QApplication(sys.argv)
        cls.window = MainWindow()
        cls.window.resize(1366, 850)
        cls.window.show()

    @classmethod
    def tearDownClass(cls):
        cls.window.close()

    def test_01_main_window_tabs_and_render(self):
        """Test switching across all tabs in MainWindow."""
        tabs = [
            ("Dashboard", self.window.show_dashboard),
            ("Table", self.window.show_table),
            ("Contracts", self.window.show_contracts),
            ("Trash", self.window.show_trash),
            ("Settings", self.window.show_settings),
        ]
        for name, show_func in tabs:
            show_func()
            self.app.processEvents()
            self.assertIsNotNone(self.window.content_stack.currentWidget(), f"Failed rendering tab: {name}")

    def test_02_theme_toggle_and_font_scaling(self):
        """Test toggling between dark/light and dynamic font scaling."""
        # Test Dark Theme
        self.window.set_theme("dark")
        self.app.processEvents()
        self.assertEqual(self.window.current_theme, "dark")
        
        # Test Light Theme
        self.window.set_theme("light")
        self.app.processEvents()
        self.assertEqual(self.window.current_theme, "light")

        # Test toggle_theme
        self.window.toggle_theme()
        self.app.processEvents()
        self.assertEqual(self.window.current_theme, "dark")

        # Test Font Scaling
        for test_size in [11, 13, 15, 18]:
            self.window.update_font_size(test_size)
            self.app.processEvents()
            # Verify stylesheet includes updated font-size
            ss = self.app.styleSheet()
            self.assertIn(f"font-size: {test_size}px", ss)

        # Reset to default
        self.window.set_theme("dark")
        self.window.update_font_size(13)
        self.app.processEvents()

    def test_03_dashboard_view_components(self):
        """Test Dashboard buttons, KPI cards, charts, and table interactions."""
        self.window.show_dashboard()
        dash = self.window.dashboard_view
        self.assertIsNotNone(dash)
        dash.update_stats()
        self.app.processEvents()
        
        # Click refresh / all
        dash.btn_all.click()
        self.app.processEvents()

    def test_04_table_view_components_and_pills(self):
        """Test TableView search, pill selection, category filters."""
        self.window.show_table()
        table_v = self.window.table_view
        self.assertIsNotNone(table_v)
        table_v.filter_data()
        self.app.processEvents()

        # Search test
        table_v.edit_search.setText("Maktab")
        self.app.processEvents()
        table_v.edit_search.setText("")
        self.app.processEvents()

        # Pill filter buttons test
        if hasattr(table_v, "pill_buttons"):
            for cat, btn in list(table_v.pill_buttons.items())[:3]:
                btn.click()
                self.app.processEvents()
            # Switch back to All
            if "Barchasi" in table_v.pill_buttons:
                table_v.pill_buttons["Barchasi"].click()
                self.app.processEvents()

    def test_05_contracts_view(self):
        """Test ContractsView loading, KPI cards and filters."""
        self.window.show_contracts()
        cv = self.window.contracts_view
        cv.load_data()
        self.app.processEvents()
        
        # Test pill clicks
        if hasattr(cv, "pill_buttons"):
            for cat, btn in list(cv.pill_buttons.items())[:3]:
                btn.click()
                self.app.processEvents()

    def test_06_trash_and_settings_views(self):
        """Test TrashView and SettingsView loading."""
        self.window.show_trash()
        tv = self.window.trash_view
        tv.load_trash()
        self.app.processEvents()

        self.window.show_settings()
        sv = self.window.settings_view
        sv.load_settings()
        self.app.processEvents()

    def test_07_dialogs_instantiation(self):
        """Test all dialogs for clean initialization, styles, and button bindings."""
        mock_dark = type("App", (), {"current_theme": "dark", "data_manager": self.window.data_manager, "data": self.window.data})()
        mock_light = type("App", (), {"current_theme": "light", "data_manager": self.window.data_manager, "data": self.window.data})()

        # 1. OrgEditDialog (Add mode)
        dlg_add = OrgEditDialog(parent=self.window, app=mock_dark)
        self.app.processEvents()
        dlg_add.close()

        # 2. CabinetDialog (Dark & Light)
        mock_org = {
            "m": "Pop Tuman 1-Maktab",
            "inn": "123456789",
            "jshr": "30101010100011",
            "login": "login_test",
            "password": "password_test",
            "cabinet_url": "https://soliq.uz"
        }
        dlg_cab_dark = CabinetDialog(parent=self.window, app=mock_dark, item=mock_org)
        self.app.processEvents()
        dlg_cab_dark.close()

        dlg_cab_light = CabinetDialog(parent=self.window, app=mock_light, item=mock_org)
        self.app.processEvents()
        dlg_cab_light.close()

        # 3. VerificationDialog (Dark & Light)
        dlg_ver_dark = VerificationDialog(parent=self.window, app=mock_dark, item=mock_org)
        self.app.processEvents()
        dlg_ver_dark.close()

        dlg_ver_light = VerificationDialog(parent=self.window, app=mock_light, item=mock_org)
        self.app.processEvents()
        dlg_ver_light.close()

        # 4. QRDialog
        dlg_qr = QRDialog(item=mock_org, phone="+998901234567", parent=self.window)
        self.app.processEvents()
        dlg_qr.close()

        # 5. ImportDialog
        dlg_imp = ImportDialog(parent=self.window, app=mock_dark)
        self.app.processEvents()
        dlg_imp.close()

        # 6. ContractAddDialog
        dlg_con = ContractAddDialog(parent=self.window, app=mock_dark)
        self.app.processEvents()
        dlg_con.close()

        # 7. MahallaPassportView (Dark & Light)
        dlg_mah_dark = MahallaPassportView(parent=self.window, app=mock_dark, selected_mahalla="Chorkesar MFY")
        self.app.processEvents()
        dlg_mah_dark.close()

        dlg_mah_light = MahallaPassportView(parent=self.window, app=mock_light, selected_mahalla="Chorkesar MFY")
        self.app.processEvents()
        dlg_mah_light.close()

    def test_08_styles_generation(self):
        """Verify stylesheet generator with dark/light and various font sizes."""
        for theme in ["dark", "light"]:
            for fs in [10, 12, 14, 16, 20]:
                ss = get_stylesheet(theme, fs)
                self.assertTrue(len(ss) > 500)
                self.assertIn(".btn_primary", ss)
                self.assertIn(".btn_secondary", ss)
                self.assertIn(".btn_success", ss)
                self.assertIn(".btn_danger", ss)
                self.assertIn(".btn_warning", ss)
                self.assertIn(".btn_info", ss)
                self.assertIn(".btn_purple", ss)
                self.assertIn(".pill_btn", ss)
                self.assertIn("QCheckBox", ss)
                self.assertIn("QRadioButton", ss)
                self.assertIn("QSpinBox", ss)
                self.assertIn("QStatusBar", ss)
                self.assertIn("QToolTip", ss)

if __name__ == "__main__":
    unittest.main()
