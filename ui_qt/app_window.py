"""
ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Clean Architecture).
Senior darajadagi Fluent UI sidebar navigatsiyasi, yuqori unumdorlik, High-DPI va to'liq sinxronizatsiya.
"""
import os
import sys
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QLabel, QPushButton, QStackedWidget, QStatusBar, QMessageBox,
    QApplication, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QColor

from core.config import APP_TITLE, ICON_PATH, DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE
from core.logger import logger
from database.data_manager import DataManager
from ui_qt.styles import get_stylesheet
from ui_qt.views.dashboard_view import DashboardView
from ui_qt.views.table_view import TableView
from ui_qt.views.trash_view import TrashView
from ui_qt.views.settings_view import SettingsView
from ui_qt.views.mahalla_passport_view import open_mahalla_passport
from ui_qt.views.cabinet_dialog import open_cabinet_dialog
from ui_qt.views.verification_dialog import open_verification_dialog
from ui_qt.views.broadcast_view import open_broadcast_dialog
from ui_qt.views.history_view import open_staff_history_dialog
from ui_qt.views.import_dialog import open_batch_import_dialog
from ui_qt.views.org_edit_dialog import OrgEditDialog

class MainWindow(QMainWindow):
    """Pop Tuman Tizimining Asosiy PyQt5 Oynasi."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_TITLE} (PyQt5 PRO)")
        self.resize(1150, 700)
        self.setMinimumSize(840, 520)

        # Ma'lumotlar boshqaruvchisi
        self.data_manager = DataManager()
        self.data = self.data_manager.data
        self.current_theme = "dark"

        # Ikonka
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        # UI tuzilishi
        self.setup_ui()
        self.apply_theme(self.current_theme)

        logger.info(f"[QT] PyQt5 MainWindow yuklandi: {len(self.data)} ta tashkilot")

    def setup_ui(self):
        # Markaziy konteyner
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.root_layout = QHBoxLayout(self.central_widget)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # 1. SIDEBAR (Chap boshqaruv paneli)
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(8, 12, 8, 10)
        self.sidebar_layout.setSpacing(2)

        # Logo va Sarlavha
        if os.path.exists(ICON_PATH):
            logo_lbl = QLabel()
            pixmap = QPixmap(ICON_PATH).scaled(38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_lbl.setPixmap(pixmap)
            logo_lbl.setAlignment(Qt.AlignCenter)
            self.sidebar_layout.addWidget(logo_lbl)

        title_lbl = QLabel("POP TUMANI")
        title_lbl.setObjectName("sidebar_title")
        title_lbl.setAlignment(Qt.AlignCenter)
        subtitle_lbl = QLabel("SMART TIZIM v2.0")
        subtitle_lbl.setObjectName("sidebar_subtitle")
        subtitle_lbl.setAlignment(Qt.AlignCenter)

        self.sidebar_layout.addWidget(title_lbl)
        self.sidebar_layout.addWidget(subtitle_lbl)
        self.sidebar_layout.addSpacing(8)

        # Navigatsiya tugmalari guruhi
        self.nav_buttons = {}

        # ASOSIY bo'limi
        sec_main = QLabel("ASOSIY")
        sec_main.setObjectName("sidebar_section")
        self.sidebar_layout.addWidget(sec_main)

        self.add_nav_btn("📊 Dashboard", "dashboard", self.show_dashboard)
        self.add_nav_btn("📋 Tashkilotlar", "table", self.show_table)
        self.add_nav_btn("🏘 Mahalla 'Yettiligi'", "passport", lambda: self.open_yettilik())
        self.add_nav_btn("📜 Kadrlar Tarixi", "history", lambda: self.open_history())
        self.add_nav_btn("⚙ Sozlamalar", "settings", self.show_settings)

        self.sidebar_layout.addSpacing(10)

        # TIZIM bo'limi
        sec_sys = QLabel("TIZIM")
        sec_sys.setObjectName("sidebar_section")
        self.sidebar_layout.addWidget(sec_sys)

        self.add_nav_btn("📢 Xabarnoma", "broadcast", lambda: self.open_broadcast())
        self.add_nav_btn("📥 Excel Import", "import", lambda: self.open_import())
        self.add_nav_btn("🗑 Chiqindi Qutisi", "trash", self.show_trash)

        self.sidebar_layout.addStretch()

        # Mavzu almashtirish tugmasi
        self.btn_theme = QPushButton("☀ Kunduzi Rejim")
        self.btn_theme.setProperty("class", "sidebar_btn")
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.sidebar_layout.addWidget(self.btn_theme)

        # Chiqish tugmasi
        btn_exit = QPushButton("🚪 Chiqish")
        btn_exit.setProperty("class", "sidebar_btn")
        btn_exit.setStyleSheet("color: #ef4444; font-weight: 700;")
        btn_exit.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_exit)

        self.root_layout.addWidget(self.sidebar)

        # 2. MARKAZIY KONTENT (QStackedWidget)
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")

        # Sahifalarni yaratish
        self.dashboard_view = DashboardView(parent=self.content_stack, app=self)
        self.table_view = TableView(parent=self.content_stack, app=self)
        self.trash_view = TrashView(parent=self.content_stack, app=self)
        self.settings_view = SettingsView(parent=self.content_stack, app=self)

        self.content_stack.addWidget(self.dashboard_view) # 0
        self.content_stack.addWidget(self.table_view)     # 1
        self.content_stack.addWidget(self.trash_view)     # 2
        self.content_stack.addWidget(self.settings_view)  # 3

        self.root_layout.addWidget(self.content_stack, 1)

        # 3. STATUS BAR
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.lbl_status_total = QLabel(f"Jami tashkilotlar: {len(self.data)} ta")
        self.lbl_status_db = QLabel("Baza: SQLite WAL 🟢")
        self.lbl_status_user = QLabel("Foydalanuvchi: ADMIN 👑")

        self.status_bar.addWidget(self.lbl_status_total)
        self.status_bar.addPermanentWidget(self.lbl_status_db)
        self.status_bar.addPermanentWidget(self.lbl_status_user)

        # Dastlabki sahifani ochish
        self.show_dashboard()

    def add_nav_btn(self, text: str, key: str, callback):
        btn = QPushButton(text)
        btn.setProperty("class", "sidebar_btn")
        btn.setCheckable(True)
        btn.clicked.connect(callback)
        self.sidebar_layout.addWidget(btn)
        self.nav_buttons[key] = btn
        return btn

    def set_active_nav_btn(self, active_key: str):
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == active_key)

    def apply_theme(self, theme: str):
        self.current_theme = theme
        qss = get_stylesheet(theme)
        self.setStyleSheet(qss)
        if theme == "dark":
            self.btn_theme.setText("☀ Kunduzi Rejim")
        else:
            self.btn_theme.setText("🌙 Tungi Rejim")

    def toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
        self.show_toast(f"Mavzu o'zgartirildi: {new_theme.capitalize()}", "info")

    def set_theme(self, theme: str):
        self.apply_theme(theme)

    def show_dashboard(self):
        self.set_active_nav_btn("dashboard")
        self.dashboard_view.update_stats()
        self.content_stack.setCurrentIndex(0)

    def show_table(self):
        self.set_active_nav_btn("table")
        self.table_view.filter_data()
        self.content_stack.setCurrentIndex(1)

    def show_trash(self):
        self.set_active_nav_btn("trash")
        self.trash_view.load_trash()
        self.content_stack.setCurrentIndex(2)

    def show_settings(self):
        self.set_active_nav_btn("settings")
        self.settings_view.load_settings()
        self.content_stack.setCurrentIndex(3)

    def filter_by_category(self, cat_key: str):
        self.show_table()
        self.table_view.on_category_clicked(cat_key)

    def open_add_dialog(self):
        dlg = OrgEditDialog(parent=self, app=self)
        if dlg.exec_() == OrgEditDialog.Accepted:
            self.refresh_all_views()
            self.show_toast("Yangi tashkilot muvaffaqiyatli saqlandi! 🎉", "success")

    def open_yettilik(self, mahalla: Optional[str] = None):
        open_mahalla_passport(self, mahalla)

    def open_cabinet(self, item: Optional[Dict[str, Any]] = None):
        open_cabinet_dialog(self, item)

    def open_verification(self, item: Optional[Dict[str, Any]] = None):
        open_verification_dialog(self, item)

    def open_broadcast(self):
        open_broadcast_dialog(self)

    def open_history(self, mahalla: Optional[str] = None):
        open_staff_history_dialog(self, mahalla=mahalla)

    def open_import(self):
        open_batch_import_dialog(self)

    def refresh_all_views(self):
        self.data = self.data_manager.data
        self.lbl_status_total.setText(f"Jami tashkilotlar: {len(self.data)} ta")
        self.dashboard_view.update_stats()
        self.table_view.filter_data()
        self.trash_view.load_trash()

    def show_toast(self, message: str, toast_type: str = "info"):
        """Status bar orqali chiroyli xabar chiqarish."""
        self.status_bar.showMessage(f"✨ {message}", 4000)

    def closeEvent(self, event):
        """Dastur yopilayotganda avtomatik zaxira nusxa yaratish."""
        logger.info("[QT] Dastur yopilmoqda. SQLite avtomatik zaxira nusxa olinmoqda...")
        try:
            self.data_manager.backup_data()
        except Exception as e:
            logger.warning(f"Zaxira olishda ogohlantirish: {e}")
        event.accept()

def run_qt_app():
    """PyQt5 ilovasini ishga tushirish (High-DPI qo'llab-quvvatlash bilan)."""
    # High-DPI masshtab
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Pop Tuman Tizimi")

    window = MainWindow()
    window.show()
    return app.exec_()
