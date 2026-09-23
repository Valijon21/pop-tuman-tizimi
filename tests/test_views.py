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

if __name__ == "__main__":
    unittest.main()
