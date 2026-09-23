import unittest
import sys

class TestViewImports(unittest.TestCase):
    """Barcha UI ko'rinishlari (Views) runtime rejimida to'g'ri import bo'lishini tekshirish."""

    def test_dashboard_view_import(self):
        from ui.views import dashboard_view
        self.assertTrue(callable(dashboard_view.render_dashboard))

    def test_table_view_import(self):
        from ui.views import table_view
        self.assertTrue(callable(table_view.render_table))

    def test_trash_view_import(self):
        from ui.views import trash_view
        self.assertTrue(callable(trash_view.render_trash))

    def test_settings_view_import(self):
        from ui.views import settings_view
        self.assertTrue(callable(settings_view.render_settings))

    def test_app_import(self):
        from ui.app import MahallaDasturi
        self.assertIsNotNone(MahallaDasturi)

    def test_cabinet_dialog_import(self):
        from ui.views import cabinet_dialog
        self.assertTrue(callable(cabinet_dialog.open_cabinet_dialog))
        self.assertTrue(callable(cabinet_dialog.copy_cabinet_quick))

    def test_mahalla_passport_view_import(self):
        from ui.views import mahalla_passport_view
        self.assertTrue(callable(mahalla_passport_view.open_mahalla_passport))

    def test_history_view_import(self):
        from ui.views import history_view
        self.assertTrue(callable(history_view.open_staff_history_dialog))

    def test_import_dialog_import(self):
        from ui.views import import_dialog
        self.assertTrue(callable(import_dialog.open_batch_import_dialog))

    def test_broadcast_view_import(self):
        from ui.views import broadcast_view
        self.assertTrue(callable(broadcast_view.open_broadcast_dialog))

if __name__ == "__main__":
    unittest.main()


