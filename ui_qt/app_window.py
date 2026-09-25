"""
ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Clean Architecture).
Senior darajadagi Fluent UI sidebar navigatsiyasi, yuqori unumdorlik, High-DPI va to'liq sinxronizatsiya.
"""
import os
import sys
import time
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QLabel, QPushButton, QStackedWidget, QStatusBar, QMessageBox,
    QApplication, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QLockFile
from PyQt5.QtGui import QIcon, QPixmap, QColor

from core.config import (
    APP_TITLE, ICON_PATH, ICON_ICO_PATH, LOGO_PATH,
    DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE
)
from core.logger import logger
from core.threading_utils import WorkerThread
from database.data_manager import DataManager
from ui_qt.styles import get_stylesheet, create_crisp_pixmap
from ui_qt.views.dashboard_view import DashboardView
from ui_qt.views.table_view import TableView
from ui_qt.views.contracts_view import ContractsView
from ui_qt.views.trash_view import TrashView
from ui_qt.views.settings_view import SettingsView
from ui_qt.views.apps_view import AppsView
from ui_qt.views.mahalla_passport_view import open_mahalla_passport
from ui_qt.views.cabinet_dialog import open_cabinet_dialog
from ui_qt.views.verification_dialog import open_verification_dialog
from ui_qt.views.broadcast_view import open_broadcast_dialog
from ui_qt.views.history_view import open_staff_history_dialog
from ui_qt.views.import_dialog import open_batch_import_dialog
from ui_qt.views.org_edit_dialog import OrgEditDialog
from ui_qt.views.qr_dialog import open_qr_dialog

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
        self.font_size = int(self.data_manager.settings.get("font_size", 12))
        self._dirty_views = {
            "dashboard": False,
            "table": False,
            "contracts": False,
            "apps": False,
            "trash": True,
            "settings": True
        }

        # Ilova va Oyna ikonasi (Tepa panel va Windows Taskbar uchun)
        self.app_icon = QIcon()
        if os.path.exists(ICON_ICO_PATH):
            self.app_icon.addFile(ICON_ICO_PATH)
        if os.path.exists(ICON_PATH):
            self.app_icon.addFile(ICON_PATH)
        if not self.app_icon.isNull():
            self.setWindowIcon(self.app_icon)

        # Sessiya autentifikatsiyasi (edit va settings parollari uchun)
        self._session_authenticated: Dict[str, bool] = {}

        # UI tuzilishi
        self.setup_ui()
        self.apply_theme(self.current_theme, self.font_size)

        # Telegram botni fonda (asinxron) ishga tushirish
        self.bot_service = None
        self.start_background_bot()

        # Avtomatlashtirilgan fonda davriy zaxira (Task 5: Auto-Backup Scheduler)
        self.backup_timer = QTimer(self)
        self._backup_worker = None
        self.setup_auto_backup()

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

        # Logo va Sarlavha (Ichki brend logotipi - POP DATA)
        brand_box = QWidget()
        brand_box.setObjectName("sidebar_brand_box")
        b_layout = QVBoxLayout(brand_box)
        b_layout.setContentsMargins(4, 4, 4, 4)
        b_layout.setSpacing(0)
        b_layout.setAlignment(Qt.AlignCenter)

        logo_path = LOGO_PATH if os.path.exists(LOGO_PATH) else ICON_PATH
        if os.path.exists(logo_path):
            logo_lbl = QLabel()
            pixmap = create_crisp_pixmap(logo_path, target_width=138, target_height=138, supersample=3.0)
            logo_lbl.setPixmap(pixmap)
            logo_lbl.setAlignment(Qt.AlignCenter)
            logo_lbl.setStyleSheet("background: transparent; border: none;")
            b_layout.addWidget(logo_lbl)

        self.sidebar_layout.addWidget(brand_box)
        self.sidebar_layout.addSpacing(4)

        # Navigatsiya tugmalari guruhi
        self.nav_buttons = {}
        self._last_page_key = "dashboard"  # Dialog ochilganda orqaga qaytish uchun

        # ASOSIY bo'limi
        sec_main = QLabel("ASOSIY")
        sec_main.setObjectName("sidebar_section")
        self.sidebar_layout.addWidget(sec_main)

        self.add_nav_btn("📊 Dashboard", "dashboard", self.show_dashboard)
        self.add_nav_btn("🏢 Tashkilotlar", "table", self.show_table)
        self.add_nav_btn("📑 Shartnoma & Ulanish", "contracts", self.show_contracts)
        self.add_nav_btn("🏘 Mahalla 'Yettiligi'", "passport", lambda: self._open_dialog_nav("passport", self.open_yettilik))
        self.add_nav_btn("📜 Kadrlar Tarixi", "history", lambda: self._open_dialog_nav("history", self.open_history))
        self.add_nav_btn("💻 Dasturlar", "apps", self.show_apps)
        self.add_nav_btn("⚙ Sozlamalar", "settings", self.show_settings)

        self.sidebar_layout.addSpacing(10)

        # TIZIM bo'limi
        sec_sys = QLabel("TIZIM")
        sec_sys.setObjectName("sidebar_section")
        self.sidebar_layout.addWidget(sec_sys)

        self.add_nav_btn("📢 Xabarnoma", "broadcast", lambda: self._open_dialog_nav("broadcast", self.open_broadcast))
        self.add_nav_btn("📥 Excel Import", "import", lambda: self._open_dialog_nav("import", self.open_import))
        self.add_nav_btn("🗑 Chiqindi Qutisi", "trash", self.show_trash)

        self.sidebar_layout.addStretch()

        # Mavzu almashtirish tugmasi
        self.btn_theme = QPushButton("☀ Kunduzi Rejim")
        self.btn_theme.setProperty("class", "sidebar_btn")
        self.btn_theme.clicked.connect(self.toggle_theme)
        self.sidebar_layout.addWidget(self.btn_theme)

        # Chiqish tugmasi
        btn_exit = QPushButton("🚪 Chiqish")
        btn_exit.setProperty("class", "sidebar_btn_danger")
        btn_exit.clicked.connect(self.close)
        self.sidebar_layout.addWidget(btn_exit)

        self.root_layout.addWidget(self.sidebar)

        # 2. STATUS BAR (Vidjetlar yuklanishidan oldin yaratiladi)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.lbl_status_total = QLabel(f"Jami tashkilotlar: {len(self.data)} ta")
        self.lbl_status_db = QLabel("Baza: SQLite WAL 🟢")
        self.lbl_status_user = QLabel("Foydalanuvchi: ADMIN 👑")

        self.status_bar.addWidget(self.lbl_status_total)
        self.status_bar.addPermanentWidget(self.lbl_status_db)
        self.status_bar.addPermanentWidget(self.lbl_status_user)

        # 3. MARKAZIY KONTENT (QStackedWidget)
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")

        # Sahifalarni yaratish
        self.dashboard_view = DashboardView(parent=self.content_stack, app=self)
        self.table_view = TableView(parent=self.content_stack, app=self)
        self.contracts_view = ContractsView(parent=self.content_stack, app=self)
        self.trash_view = TrashView(parent=self.content_stack, app=self)
        self.settings_view = SettingsView(parent=self.content_stack, app=self)
        self.apps_view = AppsView(parent=self.content_stack, app=self)

        self.content_stack.addWidget(self.dashboard_view) # 0
        self.content_stack.addWidget(self.table_view)     # 1
        self.content_stack.addWidget(self.contracts_view) # 2
        self.content_stack.addWidget(self.trash_view)     # 3
        self.content_stack.addWidget(self.settings_view)  # 4
        self.content_stack.addWidget(self.apps_view)      # 5

        self.root_layout.addWidget(self.content_stack, 1)

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
        # Faqat sahifa tugmalari uchun oxirgi sahifani saqlash
        if active_key in ("dashboard", "table", "contracts", "apps", "trash", "settings"):
            self._last_page_key = active_key
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == active_key)

    def _open_dialog_nav(self, key: str, func):
        """Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish."""
        func()
        self.set_active_nav_btn(self._last_page_key)

    def apply_theme(self, theme: str, font_size: Optional[int] = None):
        self.current_theme = theme
        if font_size is not None:
            self.font_size = int(font_size)
        qss = get_stylesheet(theme, self.font_size)
        # Barcha top-level dialoglar (QDialog), menyular va oynalar uchun ilova darajasida qo'llash
        app_inst = QApplication.instance()
        if app_inst:
            from PyQt5.QtGui import QFont
            app_inst.setFont(QFont("Segoe UI", self.font_size))
            app_inst.setStyleSheet(qss)
        self.setStyleSheet(qss)

        # Barcha sahifalarning mavzusini yangilash
        for view_name in ("dashboard_view", "table_view", "contracts_view", "apps_view", "trash_view", "settings_view"):
            view = getattr(self, view_name, None)
            if view:
                if hasattr(view, "set_theme"):
                    view.set_theme(theme)
                if hasattr(view, "set_font_size"):
                    view.set_font_size(self.font_size)

        is_light = (theme == "light")
        if is_light:
            self.btn_theme.setText("🌙 Tungi Rejim")
            if hasattr(self, "lbl_status_total"):
                self.lbl_status_total.setStyleSheet("color: #475569; font-weight: 600;")
                self.lbl_status_db.setStyleSheet("color: #059669; font-weight: 700;")
                self.lbl_status_user.setStyleSheet("color: #0284c7; font-weight: 700;")
        else:
            self.btn_theme.setText("☀ Kunduzi Rejim")
            if hasattr(self, "lbl_status_total"):
                self.lbl_status_total.setStyleSheet("color: #94a3b8; font-weight: 600;")
                self.lbl_status_db.setStyleSheet("color: #10b981; font-weight: 700;")
                self.lbl_status_user.setStyleSheet("color: #38bdf8; font-weight: 700;")

    def update_font_size(self, new_font_size: int):
        """Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash."""
        self.font_size = new_font_size
        self.apply_theme(self.current_theme, self.font_size)
        self.show_toast(f"Shrift o'lchami o'zgartirildi: {new_font_size}px", "info")

    def toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme, self.font_size)
        self.show_toast(f"Mavzu o'zgartirildi: {'Kunduzgi' if new_theme == 'light' else 'Tungi'}", "info")

    def set_theme(self, theme: str):
        self.apply_theme(theme, self.font_size)

    def show_dashboard(self):
        self.set_active_nav_btn("dashboard")
        if self._dirty_views.get("dashboard", False):
            self.dashboard_view.update_stats()
            self._dirty_views["dashboard"] = False
        self.content_stack.setCurrentIndex(0)

    def show_table(self):
        self.set_active_nav_btn("table")
        if self._dirty_views.get("table", False):
            self.table_view.filter_data()
            self._dirty_views["table"] = False
        self.content_stack.setCurrentIndex(1)

    def show_contracts(self):
        self.set_active_nav_btn("contracts")
        if self._dirty_views.get("contracts", False):
            self.contracts_view.load_data()
            self._dirty_views["contracts"] = False
        self.content_stack.setCurrentIndex(2)

    def show_trash(self):
        self.set_active_nav_btn("trash")
        if self._dirty_views.get("trash", True):
            self.trash_view.load_trash()
            self._dirty_views["trash"] = False
        self.content_stack.setCurrentIndex(3)

    def check_permission(self, action: str = "edit", parent=None) -> bool:
        """Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish."""
        from ui_qt.views.password_dialog import request_password
        return request_password(parent or self, self, action=action)

    def show_apps(self):
        """Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk)."""
        self.set_active_nav_btn("apps")
        if hasattr(self, "apps_view") and hasattr(self.apps_view, "refresh_status"):
            self.apps_view.refresh_status()
        self.content_stack.setCurrentIndex(5)

    def show_settings(self):
        """Sozlamalar sahifasini ochish (773423321v paroli bilan himoyalangan)."""
        if not self.check_permission("settings"):
            self.set_active_nav_btn(self._last_page_key)
            return
        self.set_active_nav_btn("settings")
        if self._dirty_views.get("settings", True):
            self.settings_view.load_settings()
            self._dirty_views["settings"] = False
        self.content_stack.setCurrentIndex(4)

    def filter_by_category(self, cat_key: str):
        self.show_table()
        self.table_view.on_category_clicked(cat_key)

    def open_add_dialog(self):
        """Yangi tashkilot qo'shish (1234567 paroli bilan himoyalangan)."""
        if not self.check_permission("edit"):
            return
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
        if not self.check_permission("edit"):
            return
        open_batch_import_dialog(self)

    def open_qr(self, item: Optional[Dict[str, Any]] = None, phone: str = "", org_name: str = "", person_name: str = "", role: str = "", inn: str = ""):
        """QR-kod oynasini ochish."""
        open_qr_dialog(self, item=item, phone=phone, org_name=org_name, person_name=person_name, role=role, inn=inn)

    def start_background_bot(self):
        """Telegram botni fon rejimida (asinxron) ishga tushirish."""
        if os.environ.get("QT_QPA_PLATFORM") == "offscreen" or os.environ.get("TESTING") == "1":
            return
        try:
            token = self.data_manager.settings.get("telegram_bot_token", "").strip()
            if token and len(token) > 15:
                from services.telegram_bot import get_telegram_bot_service
                self.bot_service = get_telegram_bot_service(self.data_manager, token)
                if not self.bot_service.running:
                    self.bot_service.start()
                    logger.info("[BOT] Telegram bot fon oqimida (asinxron) ishga tushirildi.")
        except Exception as e:
            logger.error(f"[BOT] Telegram botni ishga tushirishda xatolik: {e}")

    def stop_background_bot(self):
        """Telegram botni to'xtatish."""
        if hasattr(self, "bot_service") and self.bot_service:
            try:
                self.bot_service.stop()
                logger.info("[BOT] Telegram bot to'xtatildi.")
            except Exception as e:
                logger.error(f"[BOT] Botni to'xtatishda xatolik: {e}")

    def refresh_all_views(self):
        self.data = self.data_manager.data
        self.lbl_status_total.setText(f"Jami tashkilotlar: {len(self.data)} ta")
        for k in self._dirty_views:
            self._dirty_views[k] = True

        if hasattr(self.table_view, "setup_category_pills"):
            self.table_view.setup_category_pills()
        if hasattr(self.contracts_view, "setup_category_pills"):
            self.contracts_view.setup_category_pills()

        # Hozir ko'rinib turgan sahifani darhol yangilash
        cur_idx = self.content_stack.currentIndex()
        if cur_idx == 0:
            self.dashboard_view.update_stats()
            self._dirty_views["dashboard"] = False
        elif cur_idx == 1:
            self.table_view.filter_data()
            self._dirty_views["table"] = False
        elif cur_idx == 2:
            self.contracts_view.load_data()
            self._dirty_views["contracts"] = False
        elif cur_idx == 3:
            self.trash_view.load_trash()
            self._dirty_views["trash"] = False
        elif cur_idx == 4:
            self.settings_view.load_settings()
            self._dirty_views["settings"] = False

    def show_toast(self, message: str, toast_type: str = "info"):
        """Status bar orqali chiroyli xabar chiqarish."""
        if hasattr(self, "status_bar") and self.status_bar:
            self.status_bar.showMessage(f"✨ {message}", 4000)

    # ─────────────────────────────────────────────────────────────────────────────
    # ⏰ AVTOMATIK DAVRIY ZAXIRALASH (TASK 5: AUTO-BACKUP SCHEDULER)
    # ─────────────────────────────────────────────────────────────────────────────

    def setup_auto_backup(self):
        """Avtomatlashtirilgan davriy zaxira olish taymerini sozlash."""
        self.backup_timer.timeout.connect(self.trigger_auto_backup)
        self.restart_backup_timer()

    def restart_backup_timer(self):
        """Zaxiralash taymerini sozlamalar asosida qayta ishga tushirish."""
        settings = self.data_manager.settings
        enabled = settings.get("auto_backup_enabled", True)
        interval_mins = int(settings.get("auto_backup_interval_mins", 60))

        if self.backup_timer.isActive():
            self.backup_timer.stop()

        if enabled and interval_mins > 0:
            interval_ms = interval_mins * 60 * 1000
            self.backup_timer.start(interval_ms)
            logger.info(f"[AUTO-BACKUP] Avto-zaxiralash faol: har {interval_mins} daqiqada.")
        else:
            logger.info("[AUTO-BACKUP] Avto-zaxiralash o'chirilgan.")

    def trigger_auto_backup(self, is_manual: bool = False):
        """Fonda asinxron avtomatik zaxira nusxa yaratish (UI qotmaydi)."""
        if self._backup_worker and self._backup_worker.isRunning():
            logger.debug("[AUTO-BACKUP] Oldingi zaxira jarayoni hali davom etmoqda.")
            return

        def _task():
            return self.data_manager.backup_data()

        self._backup_worker = WorkerThread(_task, parent=self)
        self._backup_worker.result_ready.connect(lambda res: self._on_auto_backup_done(res, is_manual))
        self._backup_worker.error_occurred.connect(lambda err: logger.error(f"[AUTO-BACKUP] Xatolik: {err}"))
        self._backup_worker.start()

    def _on_auto_backup_done(self, res: Any, is_manual: bool):
        now_str = (res.get("timestamp") if isinstance(res, dict) else "") or time.strftime("%Y-%m-%d %H:%M:%S")
        self.data_manager.settings["last_auto_backup"] = now_str
        self.data_manager.save_settings()
        logger.info(f"[AUTO-BACKUP] Muvaffaqiyatli yakunlandi: {now_str}")
        if is_manual:
            self.show_toast("📦 Zaxira nusxa muvaffaqiyatli yaratildi!", "success")
        else:
            self.show_toast(f"⏰ Avtomatik zaxira olindi ({time.strftime('%H:%M')})", "info")

        if hasattr(self, "settings_view") and hasattr(self.settings_view, "update_last_backup_display"):
            self.settings_view.update_last_backup_display(now_str)

    def closeEvent(self, event):
        """Dastur yopilayotganda avtomatik zaxira nusxa yaratish va botni to'xtatish."""
        if hasattr(self, "backup_timer") and self.backup_timer.isActive():
            self.backup_timer.stop()
        if hasattr(self, "_backup_worker") and self._backup_worker and self._backup_worker.isRunning():
            try:
                self._backup_worker.wait(1000)
            except Exception:
                pass
        self.stop_background_bot()
        logger.info("[QT] Dastur yopilmoqda. SQLite avtomatik zaxira nusxa olinmoqda...")
        try:
            self.data_manager.backup_data()
        except Exception as e:
            logger.warning(f"Zaxira olishda ogohlantirish: {e}")
        event.accept()

def run_qt_app():
    """PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Single Instance himoyasi bilan)."""
    # Windows taskbar uchun alohida ilova identifikatorini o'rnatish
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("poptuman.tashkilot.inn.v4")
        except Exception:
            pass

    # High-DPI masshtab
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Pop Tuman Tizimi")

    # Global ilova ikonasi (barcha oyna va modal dialoglar uchun)
    app_icon = QIcon()
    if os.path.exists(ICON_ICO_PATH):
        app_icon.addFile(ICON_ICO_PATH)
    if os.path.exists(ICON_PATH):
        app_icon.addFile(ICON_PATH)
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    # Yagona nusxa (Single Instance Guard) tekshiruvi:
    # Bir vaqtning o'zida bir nechta dastur ochilishini, DB konfliktini va Telegram Bot 409 xatosini oldini olish
    import tempfile
    lock_path = os.path.join(tempfile.gettempdir(), "pop_tuman_tizimi.lock")
    lock_file = QLockFile(lock_path)
    lock_file.setStaleLockTime(5000)

    if not lock_file.tryLock(100):
        logger.warning(f"[SINGLE INSTANCE] Dastur allaqachon ishga tushirilgan! Qulflangan fayl: {lock_path}")
        if os.environ.get("QT_QPA_PLATFORM") != "offscreen":
            QMessageBox.warning(
                None,
                "Dastur allaqachon ochiq",
                "⚠️ Pop Tuman Tizimi dasturining boshqa nusxasi allaqachon ishlab turibdi.\n\n"
                "Iltimos, ochiq turgan dastur oynasidan foydalaning."
            )
        return 0

    # app obyektiga qulfni biriktirib qo'yish (Garbage collection o'chirib yubormasligi uchun)
    app._lock_file = lock_file

    try:
        window = MainWindow()
        window.show()
        ret = app.exec_()
    finally:
        try:
            lock_file.unlock()
        except Exception:
            pass

    return ret
