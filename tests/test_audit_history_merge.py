"""
tests.test_audit_history_merge: Proposals 2, 3, and 4 Unit and Integration Tests.
1. Proposal 2: Data Quality Auditor (AuditReportDialog, health score, quick defect filters).
2. Proposal 3: Visual Timeline History UI (HistoryView dual mode, chronological cards, diff badges).
3. Proposal 4: Two-Way Smart Diff & Merge Engine (ImportDialog difference analysis, classification, merge).
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Offscreen Qt for headless testing
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["TESTING"] = "1"

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

if not QApplication.instance():
    _app = QApplication(sys.argv)
else:
    _app = QApplication.instance()

from ui_qt.views.audit_report_dialog import AuditReportDialog
from ui_qt.views.history_view import HistoryView
from ui_qt.views.import_dialog import ImportDialog
from ui_qt.views.table_view import TableView
from ui_qt.views.contracts_view import ContractsView


class TestAuditHistoryMerge(unittest.TestCase):
    """Test suite covering Proposals 2, 3, and 4."""

    def setUp(self):
        self.mock_data = [
            {
                "id": "org-1",
                "m": "1-Maktab",
                "s": "Maktab",
                "inn": "123456789",
                "t": "+998901112233",
                "bux_tel": "+998912223344",
                "f": "Karimov Anvar",
                "lavozim": "Direktor",
                "aparat_soni": 10,
                "ulangan_soni": 5
            },
            {
                "id": "org-2",
                "m": "2-Maktab (Kamchilikli)",
                "s": "Maktab",
                "inn": "",  # missing INN
                "t": "",    # missing phone
                "bux_tel": "+998935556677",
                "f": "Salimov Botir",
                "lavozim": "Direktor",
                "aparat_soni": 15,
                "ulangan_soni": 0  # 0 connected
            },
            {
                "id": "org-3",
                "m": "Navbahor MFY (Bux yo'q)",
                "s": "Mahalla",
                "inn": "987654321",
                "t": "+998971234567",
                "bux_tel": "",  # missing accountant
                "f": "",  # missing leader name
                "lavozim": "Rais",
                "aparat_soni": 4,
                "ulangan_soni": 4
            }
        ]

        self.mock_sqlite = MagicMock()
        self.mock_sqlite.get_all.return_value = list(self.mock_data)
        self.mock_sqlite.get_staff_history.return_value = [
            {
                "id": 1,
                "mahalla_nomi": "1-Maktab",
                "lavozim": "Direktor",
                "eski_xodim": "Aliev Vali",
                "yangi_xodim": "Karimov Anvar",
                "sabab": "Kadrlar rotatsiyasi",
                "sana": "2026-09-25 10:00:00"
            }
        ]

        self.mock_dm = MagicMock()
        self.mock_dm.data = list(self.mock_data)
        self.mock_dm.settings = {}
        self.mock_dm.categories = ["Mahalla", "Maktab", "Bog'cha"]
        self.mock_dm.backup_data.return_value = "backup_test.json"
        self.mock_dm.save_data.return_value = True
        self.mock_dm.sqlite = self.mock_sqlite

        self.mock_app = MagicMock()
        self.mock_app.current_theme = "dark"
        self.mock_app.data_manager = self.mock_dm
        self.mock_app.data = list(self.mock_data)
        self.mock_app.sqlite = self.mock_sqlite
        self.mock_app.current_user = "TEST_USER"

    # =========================================================================
    # 1. PROPOSAL 2: DATA QUALITY AUDITOR TESTS
    # =========================================================================

    def test_01_audit_report_dialog_metrics(self):
        """AuditReportDialog metrics calculation and health score."""
        dlg = AuditReportDialog(parent=None, app=self.mock_app)

        self.assertEqual(dlg.total, 3)
        self.assertEqual(len(dlg.missing_inn), 1)    # org-2
        self.assertEqual(len(dlg.missing_phone), 1)  # org-2
        self.assertEqual(len(dlg.missing_bux), 1)    # org-3
        self.assertEqual(len(dlg.missing_fio), 1)    # org-3

        # Deficient records should include org-2 and org-3 (2 defective organizations)
        self.assertEqual(len(dlg.all_defective), 2)
        # Health score must be calculated (0 to 100)
        self.assertGreater(dlg.health_score, 0)
        self.assertLessEqual(dlg.health_score, 100)
        dlg.close()

    def test_02_table_view_audit_quick_filters(self):
        """TableView combo_audit quick filters for missing fields and defects."""
        tv = TableView(app=self.mock_app)
        tv.filter_data()

        # 1. Filter: INN yo'q
        idx = tv.combo_audit.findText("⚠️ INN yo'q")
        self.assertGreaterEqual(idx, 0)
        tv.combo_audit.setCurrentIndex(idx)
        tv.filter_data()
        self.assertEqual(len(tv.filtered_data), 1)
        self.assertEqual(tv.filtered_data[0]["m"], "2-Maktab (Kamchilikli)")

        # 2. Filter: Buxgalter yo'q
        idx = tv.combo_audit.findText("💼 Buxgalter yo'q")
        self.assertGreaterEqual(idx, 0)
        tv.combo_audit.setCurrentIndex(idx)
        tv.filter_data()
        self.assertEqual(len(tv.filtered_data), 1)
        self.assertEqual(tv.filtered_data[0]["m"], "Navbahor MFY (Bux yo'q)")

        # 3. Filter: Kamchiliklar (all defective records)
        idx = tv.combo_audit.findText("🚨 Kamchiliklar")
        self.assertGreaterEqual(idx, 0)
        tv.combo_audit.setCurrentIndex(idx)
        tv.filter_data()
        self.assertEqual(len(tv.filtered_data), 2)

        # 4. Filter: Barchasi (reset)
        idx = tv.combo_audit.findText("🔍 Barchasi")
        tv.combo_audit.setCurrentIndex(idx)
        tv.filter_data()
        self.assertEqual(len(tv.filtered_data), 3)
        tv.close()

    def test_03_contracts_view_audit_quick_filters(self):
        """ContractsView combo_audit quick filters."""
        cv = ContractsView(app=self.mock_app)
        cv.load_data()

        # Filter: INN yo'q
        idx = cv.combo_audit.findText("⚠️ INN yo'q")
        self.assertGreaterEqual(idx, 0)
        cv.combo_audit.setCurrentIndex(idx)
        cv.filter_data()
        self.assertEqual(len(cv.filtered_data), 1)
        self.assertEqual(cv.filtered_data[0]["m"], "2-Maktab (Kamchilikli)")

        # Filter: Ulanmagan (0 ta)
        idx = cv.combo_audit.findText("🔗 Ulanmagan (0 ta)")
        self.assertGreaterEqual(idx, 0)
        cv.combo_audit.setCurrentIndex(idx)
        cv.filter_data()
        self.assertEqual(len(cv.filtered_data), 1)
        self.assertEqual(cv.filtered_data[0]["m"], "2-Maktab (Kamchilikli)")
        cv.close()

    # =========================================================================
    # 2. PROPOSAL 3: VISUAL TIMELINE HISTORY UI TESTS
    # =========================================================================

    def test_04_history_view_dual_mode_and_timeline(self):
        """HistoryView dual mode switcher (Timeline and Table) and card rendering."""
        hv = HistoryView(parent=None, app=self.mock_app)
        self.assertIsNotNone(hv.btn_mode_timeline)
        self.assertIsNotNone(hv.btn_mode_table)
        self.assertEqual(hv.stack.currentIndex(), 0)  # 0 is Timeline

        # Verify timeline records
        self.assertEqual(len(hv.all_records), 1)
        self.assertGreater(hv.timeline_layout.count(), 0)

        # Switch to table mode
        hv.switch_view(1)
        self.assertEqual(hv.stack.currentIndex(), 1)
        self.assertEqual(hv.table.rowCount(), 1)

        # Switch back to timeline mode
        hv.switch_view(0)
        self.assertEqual(hv.stack.currentIndex(), 0)
        hv.close()

    def test_05_history_view_search_and_filter(self):
        """HistoryView search input and role filter."""
        hv = HistoryView(parent=None, app=self.mock_app)
        
        # Test search
        hv.txt_search.setText("Anvar")
        hv.filter_records()
        self.assertEqual(len(hv.filtered_records), 1)

        hv.txt_search.setText("MavjudEmasSoz")
        hv.filter_records()
        self.assertEqual(len(hv.filtered_records), 0)

        hv.txt_search.clear()
        hv.filter_records()
        self.assertEqual(len(hv.filtered_records), 1)
        hv.close()

    # =========================================================================
    # 3. PROPOSAL 4: TWO-WAY SMART DIFF & MERGE ENGINE TESTS
    # =========================================================================

    def test_06_smart_diff_analysis_classification(self):
        """ImportDialog._analyze_differences classifies MODIFIED, NEW, UNCHANGED accurately."""
        dlg = ImportDialog(parent=None, app=self.mock_app)

        incoming_records = [
            # 1. Existing org with changed director & phone -> MODIFIED
            {
                "inn": "123456789",
                "m": "1-Maktab",
                "s": "Maktab",
                "f": "Eshmatov Toshmat",  # Was Karimov Anvar
                "t": "+998909998877",     # Was +998901112233
                "bux_tel": "+998912223344"
            },
            # 2. Brand new organization -> NEW
            {
                "inn": "555666777",
                "m": "Yangi Innovatsion Maktab",
                "s": "Maktab",
                "f": "G'ofurov Sherzod",
                "t": "+998931110022"
            },
            # 3. Unchanged organization -> UNCHANGED
            {
                "inn": "987654321",
                "m": "Navbahor MFY (Bux yo'q)",
                "s": "Mahalla",
                "f": "",
                "t": "+998971234567",
                "bux_tel": ""
            }
        ]

        diff_results = dlg._analyze_differences(incoming_records)
        self.assertEqual(len(diff_results), 3)

        # Check item 1 (MODIFIED)
        mod_item = diff_results[0]
        self.assertEqual(mod_item["status"], "MODIFIED")
        self.assertGreater(len(mod_item["diffs"]), 0)
        diff_str = " ".join(mod_item["diffs"])
        self.assertIn("Rahbar", diff_str)
        self.assertIn("Telefon", diff_str)

        # Check item 2 (NEW)
        new_item = diff_results[1]
        self.assertEqual(new_item["status"], "NEW")

        # Check item 3 (UNCHANGED)
        unchanged_item = diff_results[2]
        self.assertEqual(unchanged_item["status"], "UNCHANGED")
        dlg.close()

    def test_07_commit_smart_merge(self):
        """ImportDialog.commit_smart_merge executes backup, updates DB, and logs staff history."""
        dlg = ImportDialog(parent=None, app=self.mock_app)

        incoming_records = [
            {
                "inn": "123456789",
                "m": "1-Maktab",
                "s": "Maktab",
                "f": "Eshmatov Toshmat",  # Director rotation
                "t": "+998909998877",
                "bux_tel": "+998912223344"
            }
        ]

        analyzed = dlg._analyze_differences(incoming_records)
        dlg._on_analysis_done(analyzed)

        # Set checkbox checked in table_preview
        dlg.table_preview.item(0, 0).setCheckState(Qt.Checked)

        with patch("PyQt5.QtWidgets.QMessageBox.information"), \
             patch("PyQt5.QtWidgets.QMessageBox.question", return_value=16384):  # QMessageBox.Yes
            dlg.commit_smart_merge()

        # Ensure sqlite add_staff_history was invoked
        self.mock_sqlite.add_staff_history.assert_called()
        call_kwargs = self.mock_sqlite.add_staff_history.call_args[1]
        self.assertEqual(call_kwargs.get("old_fio"), "Karimov Anvar")
        self.assertEqual(call_kwargs.get("new_fio"), "Eshmatov Toshmat")

        # Ensure data manager backup was called before merge
        self.mock_dm.backup_data.assert_called()
        dlg.close()


if __name__ == "__main__":
    unittest.main()
