"""
ui_qt.views.settings_view: Tizim sozlamalari sahifasi (PyQt5).
SQLite bazasini boshqarish, Telegram bot integratsiyasi, xavfsizlik va zaxira nusxalar.
"""
from typing import Any
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QSpinBox, QGroupBox,
    QMessageBox, QFileDialog, QScrollArea, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
from core.security import hash_password
from core.logger import logger
from core.threading_utils import WorkerThread
from services.gsheet_service import (
    get_gspread_client, upload_data_to_sheet, download_data_from_sheet,
    is_service_account_available
)

class SettingsView(QWidget):
    """Tizim sozlamalari ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(10)

        # Header
        head = QVBoxLayout()
        head.setSpacing(2)
        self.title_lbl = QLabel("⚙ Tizim Sozlamalari")
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #38bdf8;")
        self.sub_lbl = QLabel("Xavfsizlik, SQLite ma'lumotlar bazasi zaxirasi va Telegram Bot sozlamalari")
        self.sub_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")
        head.addWidget(self.title_lbl)
        head.addWidget(self.sub_lbl)
        main_layout.addLayout(head)

        # Skroll maydoni
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        c_layout = QVBoxLayout(container)
        c_layout.setSpacing(12)

        # 1. SQLITE BAZA VA ZAXIRA
        self.grp_db = QGroupBox("💾 SQLite Ma'lumotlar Bazasi va Zaxira")
        self.grp_db.setStyleSheet("QGroupBox { font-size: 14px; font-weight: 700; color: #10b981; }")
        db_layout = QVBoxLayout(self.grp_db)
        db_layout.setSpacing(12)

        self.lbl_db_info = QLabel("Baza joylashuvi: mahalla_tizimi.db")
        self.lbl_db_info.setStyleSheet("color: #94a3b8; font-size: 12px;")
        db_layout.addWidget(self.lbl_db_info)

        db_btns = QHBoxLayout()
        btn_backup = QPushButton("📦 Zaxira Nusxa Yaratish (Backup)")
        btn_backup.setProperty("class", "btn_success")
        btn_backup.clicked.connect(self.create_backup)
        db_btns.addWidget(btn_backup)

        btn_restore_db = QPushButton("🔄 Zaxiradan Tiklash (Restore)")
        btn_restore_db.setObjectName("btn_restore_db")
        btn_restore_db.setProperty("class", "btn_secondary")
        btn_restore_db.clicked.connect(self.restore_backup)
        self.btn_restore_db = btn_restore_db
        db_btns.addWidget(btn_restore_db)
        db_btns.addStretch()

        db_layout.addLayout(db_btns)

        # ⏰ Avtomatik davriy zaxira boshqaruvi (Auto-Backup Scheduler)
        self.auto_backup_frame = QFrame()
        self.auto_backup_frame.setStyleSheet("background: rgba(15, 23, 42, 0.4); border: 1px solid #334155; border-radius: 8px; padding: 6px;")
        auto_layout = QVBoxLayout(self.auto_backup_frame)
        auto_layout.setContentsMargins(8, 8, 8, 8)
        auto_layout.setSpacing(8)

        auto_head = QHBoxLayout()
        self.chk_auto_backup = QCheckBox("Avtomatlashtirilgan davriy zaxira (Auto-Backup Scheduler)")
        self.chk_auto_backup.setChecked(True)
        self.chk_auto_backup.setCursor(Qt.PointingHandCursor)
        self.chk_auto_backup.setStyleSheet("font-size: 11.5px; font-weight: 700; color: #38bdf8;")
        self.chk_auto_backup.stateChanged.connect(self.on_auto_backup_toggled)
        auto_head.addWidget(self.chk_auto_backup)

        auto_head.addStretch()
        lbl_oraliq = QLabel("Oraliq:")
        lbl_oraliq.setStyleSheet("font-size: 11px; font-weight: 600;")
        auto_head.addWidget(lbl_oraliq)

        self.combo_backup_interval = QComboBox()
        self.combo_backup_interval.addItems([
            "15 daqiqa", "30 daqiqa", "1 soat (Tavsiya)", "2 soat", "6 soat", "12 soat", "24 soat"
        ])
        self.combo_backup_interval.currentIndexChanged.connect(self.on_backup_interval_changed)
        auto_head.addWidget(self.combo_backup_interval)
        auto_layout.addLayout(auto_head)

        auto_foot = QHBoxLayout()
        self.lbl_last_backup = QLabel("Oxirgi avto-zaxira: Noma'lum")
        self.lbl_last_backup.setStyleSheet("color: #94a3b8; font-size: 11px;")
        auto_foot.addWidget(self.lbl_last_backup)
        auto_foot.addStretch()

        self.btn_auto_now = QPushButton("⚡ Fonda Sinab Ko'rish")
        self.btn_auto_now.setProperty("class", "btn_primary")
        self.btn_auto_now.setCursor(Qt.PointingHandCursor)
        self.btn_auto_now.setStyleSheet("font-size: 11px; padding: 4px 10px;")
        self.btn_auto_now.clicked.connect(self.trigger_manual_auto_backup)
        auto_foot.addWidget(self.btn_auto_now)
        auto_layout.addLayout(auto_foot)

        db_layout.addWidget(self.auto_backup_frame)
        c_layout.addWidget(self.grp_db)

        # 2. GOOGLE SHEETS BULUTLI SINXRONIZATSIYA
        self.grp_gsheet = QGroupBox("☁ Google Sheets Bulutli Sinxronizatsiya")
        gsheet_layout = QVBoxLayout(self.grp_gsheet)
        gsheet_layout.setSpacing(10)

        gsheet_grid = QGridLayout()
        gsheet_grid.addWidget(QLabel("Google Sheet Nomi / URL:"), 0, 0)
        self.edit_sheet_id = QLineEdit()
        self.edit_sheet_id.setPlaceholderText("Jadval nomi yoki to'liq URL (masalan: Tashkilotlar Bazasi)...")
        gsheet_grid.addWidget(self.edit_sheet_id, 0, 1)

        gsheet_layout.addLayout(gsheet_grid)

        gsheet_btns = QHBoxLayout()
        self.btn_gsheet_upload = QPushButton("☁ Bulutga Yuklash (Upload)")
        self.btn_gsheet_upload.setProperty("class", "btn_success")
        self.btn_gsheet_upload.clicked.connect(self.upload_to_google_sheet)
        gsheet_btns.addWidget(self.btn_gsheet_upload)

        self.btn_gsheet_download = QPushButton("📥 Bulutdan Yuklab Olish (Download)")
        self.btn_gsheet_download.setProperty("class", "btn_primary")
        self.btn_gsheet_download.clicked.connect(self.download_from_google_sheet)
        gsheet_btns.addWidget(self.btn_gsheet_download)

        self.lbl_gsheet_status = QLabel("Holat: Tekshirilmoqda...")
        self.lbl_gsheet_status.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")
        gsheet_btns.addWidget(self.lbl_gsheet_status)
        gsheet_btns.addStretch()

        gsheet_layout.addLayout(gsheet_btns)
        c_layout.addWidget(self.grp_gsheet)

        # 3. TELEGRAM BOT INTEGRATSIYASI
        self.grp_tg = QGroupBox("✈ Telegram Bot Integratsiyasi")
        tg_layout = QVBoxLayout(self.grp_tg)
        tg_layout.setSpacing(10)

        tg_grid = QGridLayout()
        tg_grid.addWidget(QLabel("Bot Tokeni:"), 0, 0)
        self.edit_bot_token = QLineEdit()
        self.edit_bot_token.setPlaceholderText("Masalan: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ...")
        tg_grid.addWidget(self.edit_bot_token, 0, 1)

        tg_layout.addLayout(tg_grid)

        tg_btns = QHBoxLayout()
        btn_save_bot = QPushButton("💾 Tokenni Saqlash")
        btn_save_bot.setProperty("class", "btn_primary")
        btn_save_bot.clicked.connect(self.save_bot_token)
        tg_btns.addWidget(btn_save_bot)

        btn_restart_bot = QPushButton("🔄 Qayta Ishga Tushirish")
        btn_restart_bot.setProperty("class", "btn_success")
        btn_restart_bot.clicked.connect(self.restart_bot)
        tg_btns.addWidget(btn_restart_bot)

        self.lbl_bot_status = QLabel("Holat: Sozlanmagan")
        self.lbl_bot_status.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")
        tg_btns.addWidget(self.lbl_bot_status)
        tg_btns.addStretch()

        tg_layout.addLayout(tg_btns)
        c_layout.addWidget(self.grp_tg)

        # 3. XAVFSIZLIK VA PAROL
        self.grp_sec = QGroupBox("🔒 Xavfsizlik va Admin Paroli")
        sec_layout = QGridLayout(self.grp_sec)
        sec_layout.setSpacing(10)

        sec_layout.addWidget(QLabel("Yangi Admin Paroli:"), 0, 0)
        self.edit_new_pass = QLineEdit()
        self.edit_new_pass.setEchoMode(QLineEdit.Password)
        self.edit_new_pass.setPlaceholderText("Yangi parolni kiriting...")
        sec_layout.addWidget(self.edit_new_pass, 0, 1)

        btn_pass = QPushButton("🔑 Parolni Yangilash")
        btn_pass.setProperty("class", "btn_danger")
        btn_pass.clicked.connect(self.update_password)
        sec_layout.addWidget(btn_pass, 0, 2)

        c_layout.addWidget(self.grp_sec)

        # 4. KO'RINISH VA SHRIFT
        self.grp_ui = QGroupBox("🎨 Interfeys Sozlamalari")
        self.grp_ui.setStyleSheet("QGroupBox { font-size: 14px; font-weight: 700; color: #f59e0b; }")
        ui_layout = QHBoxLayout(self.grp_ui)

        ui_layout.addWidget(QLabel("Mavzu:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["🌙 Tungi (Dark)", "☀ Kunduzi (Light)"])
        self.combo_theme.currentIndexChanged.connect(self.on_theme_changed)
        ui_layout.addWidget(self.combo_theme)

        ui_layout.addSpacing(20)
        ui_layout.addWidget(QLabel("Shrift O'lchami:"))
        self.spin_font = QSpinBox()
        self.spin_font.setRange(10, 18)
        self.spin_font.setValue(12)
        self.spin_font.valueChanged.connect(self.on_font_changed)
        ui_layout.addWidget(self.spin_font)

        ui_layout.addStretch()
        c_layout.addWidget(self.grp_ui)

        c_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)

    def set_theme(self, theme: str):
        """Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish."""
        is_light = (theme == "light")

        # Sarlavha rangi
        self.title_lbl.setStyleSheet(
            f"font-size: 15px; font-weight: 800; color: {'#0284c7' if is_light else '#38bdf8'};"
        )
        self.sub_lbl.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        self.lbl_db_info.setStyleSheet(f"color: {'#64748b' if is_light else '#94a3b8'}; font-size: 12px;")
        self.lbl_bot_status.setStyleSheet(f"color: {'#64748b' if is_light else '#94a3b8'}; font-size: 12px; font-weight: 600;")
        self.lbl_gsheet_status.setStyleSheet(f"color: {'#64748b' if is_light else '#94a3b8'}; font-size: 12px; font-weight: 600;")

        if hasattr(self, "auto_backup_frame"):
            bg_card = "#f1f5f9" if is_light else "rgba(15, 23, 42, 0.4)"
            border_card = "#cbd5e1" if is_light else "#334155"
            self.auto_backup_frame.setStyleSheet(f"background: {bg_card}; border: 1px solid {border_card}; border-radius: 8px; padding: 6px;")
        if hasattr(self, "chk_auto_backup"):
            chk_color = "#0284c7" if is_light else "#38bdf8"
            self.chk_auto_backup.setStyleSheet(f"font-size: 11.5px; font-weight: 700; color: {chk_color};")
        if hasattr(self, "lbl_last_backup"):
            self.lbl_last_backup.setStyleSheet(f"color: {'#64748b' if is_light else '#94a3b8'}; font-size: 11px;")

        if hasattr(self, "combo_theme"):
            self.combo_theme.blockSignals(True)
            self.combo_theme.setCurrentIndex(0 if theme == "dark" else 1)
            self.combo_theme.blockSignals(False)

    def load_settings(self):
        """Mavjud sozlamalarni yuklash."""
        if not self.app or not hasattr(self.app, "data_manager"):
            return

        settings = self.app.data_manager.settings
        # Bot token va holati
        token = settings.get("telegram_bot_token", "")
        self.edit_bot_token.setText(token)
        bot_running = bool(getattr(self.app, "bot_service", None) and self.app.bot_service.running)
        if token:
            if bot_running:
                self.lbl_bot_status.setText("Holat: Bot faol (Fonda ishlamoqda) 🟢")
                self.lbl_bot_status.setStyleSheet("color: #10b981; font-weight: 700;")
            else:
                self.lbl_bot_status.setText("Holat: Token bor, lekin bot to'xtatilgan 🟡")
                self.lbl_bot_status.setStyleSheet("color: #f59e0b; font-weight: 700;")
        else:
            self.lbl_bot_status.setText("Holat: Token kiritilmagan ⚪")
            self.lbl_bot_status.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")

        # Google Sheets sozlamalari
        sheet_name = settings.get("google_sheet_name", "")
        if hasattr(self, "edit_sheet_id"):
            self.edit_sheet_id.setText(sheet_name)
        if hasattr(self, "lbl_gsheet_status"):
            if is_service_account_available():
                self.lbl_gsheet_status.setText("Kalit: Mavjud 🟢" if not sheet_name else f"Ulangan: '{sheet_name}' 🟢")
                self.lbl_gsheet_status.setStyleSheet("color: #10b981; font-weight: 600;")
            else:
                self.lbl_gsheet_status.setText("Kalit fayl yo'q (service_account.json) ⚪")
                self.lbl_gsheet_status.setStyleSheet("color: #94a3b8; font-weight: 600;")

        # Shrift
        font_size = settings.get("font_size", 13)
        self.spin_font.blockSignals(True)
        self.spin_font.setValue(font_size)
        self.spin_font.blockSignals(False)

        # SQLite hajmi
        db_path = getattr(self.app.data_manager.sqlite, "db_path", "mahalla_tizimi.db")
        if os.path.exists(db_path):
            size_kb = os.path.getsize(db_path) / 1024
            self.lbl_db_info.setText(f"SQLite Baza: {db_path} ({size_kb:.1f} KB) | Rejim: WAL (ACID)")

        # Avtomatik zaxira sozlamalari
        if hasattr(self, "chk_auto_backup"):
            auto_en = settings.get("auto_backup_enabled", True)
            self.chk_auto_backup.blockSignals(True)
            self.chk_auto_backup.setChecked(bool(auto_en))
            self.chk_auto_backup.blockSignals(False)

        if hasattr(self, "combo_backup_interval"):
            mins = int(settings.get("auto_backup_interval_mins", 60))
            min_map = {15: 0, 30: 1, 60: 2, 120: 3, 360: 4, 720: 5, 1440: 6}
            idx = min_map.get(mins, 2)
            self.combo_backup_interval.blockSignals(True)
            self.combo_backup_interval.setCurrentIndex(idx)
            self.combo_backup_interval.blockSignals(False)

        if hasattr(self, "lbl_last_backup"):
            last_bak = settings.get("last_auto_backup", "")
            if last_bak:
                self.lbl_last_backup.setText(f"Oxirgi avto-zaxira: {last_bak} ✅")
            else:
                self.lbl_last_backup.setText("Oxirgi avto-zaxira: Hali olinmagan")

    def on_auto_backup_toggled(self, state: int):
        """Avtomatik zaxira yoqilgan/o'chirilganda sozlamani yangilash."""
        if not self.app or not hasattr(self.app, "data_manager"):
            return
        enabled = bool(state == Qt.Checked)
        self.app.data_manager.settings["auto_backup_enabled"] = enabled
        self.app.data_manager.save_settings()
        if hasattr(self.app, "restart_backup_timer"):
            self.app.restart_backup_timer()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"Avtomatik zaxira: {'Yoqildi ✅' if enabled else 'O‘chirildi ⏸'}", "info")

    def on_backup_interval_changed(self, idx: int):
        """Zaxiralash vaqt oralig'i o'zgarganda."""
        if not self.app or not hasattr(self.app, "data_manager"):
            return
        intervals = [15, 30, 60, 120, 360, 720, 1440]
        mins = intervals[idx] if 0 <= idx < len(intervals) else 60
        self.app.data_manager.settings["auto_backup_interval_mins"] = mins
        self.app.data_manager.save_settings()
        if hasattr(self.app, "restart_backup_timer"):
            self.app.restart_backup_timer()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"Zaxiralash oralig'i: har {mins} daqiqaga o'rnatildi", "info")

    def trigger_manual_auto_backup(self):
        """Fonda zaxiralashni hoziroq sinab ko'rish."""
        if hasattr(self.app, "trigger_auto_backup"):
            self.app.trigger_auto_backup(is_manual=True)
        else:
            self.create_backup()

    def update_last_backup_display(self, timestamp: str):
        """MainWindow dan chaqiriladigan oxirgi zaxira vaqti ko'rsatkichi."""
        if hasattr(self, "lbl_last_backup"):
            self.lbl_last_backup.setText(f"Oxirgi avto-zaxira: {timestamp} ✅")

    def create_backup(self):
        try:
            b_path = self.app.data_manager.sqlite.backup_database()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("📦 SQLite zaxira nusxasi yaratildi!", "success")
            QMessageBox.information(self, "Muvaffaqiyatli", f"Zaxira nusxa yaratildi:\n{b_path}")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Zaxira olishda xatolik: {e}")

    def restore_backup(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "SQLite zaxira faylini tanlang", "backups", "Database Files (*.db);;All Files (*.*)"
        )
        if not file_path:
            return

        reply = QMessageBox.question(
            self, "Tasdiqlash",
            "Zaxiradan tiklash joriy bazani almashtiradi. Davom etasizmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            import shutil
            db_path = self.app.data_manager.sqlite.db_path
            shutil.copy2(file_path, db_path)
            self.app.data_manager.load_data()
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            elif hasattr(self.app, "filter_data"):
                self.app.filter_data()
            QMessageBox.information(self, "Muvaffaqiyatli", "Baza zaxiradan muvaffaqiyatli tiklandi!")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Tiklashda xatolik: {e}")

    def save_bot_token(self):
        token = self.edit_bot_token.text().strip()
        self.app.data_manager.settings["telegram_bot_token"] = token
        self.app.data_manager.save_settings()

        # Botni yangi token bilan yangilash
        if hasattr(self.app, "stop_background_bot"):
            self.app.stop_background_bot()
        if token and hasattr(self.app, "start_background_bot"):
            self.app.start_background_bot()

        self.load_settings()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Telegram token saqlandi va bot yangilandi!", "success")

    def restart_bot(self):
        """Telegram botni qo'lda qayta ishga tushirish."""
        if hasattr(self.app, "stop_background_bot"):
            self.app.stop_background_bot()
        if hasattr(self.app, "start_background_bot"):
            self.app.start_background_bot()
        self.load_settings()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Telegram bot qayta ishga tushirildi! 🔄", "success")

    def update_password(self):
        new_pwd = self.edit_new_pass.text().strip()
        if not new_pwd:
            QMessageBox.warning(self, "Xato", "Parol bo'sh bo'lishi mumkin emas!")
            return

        if "passwords" not in self.app.data_manager.settings:
            self.app.data_manager.settings["passwords"] = {}
        self.app.data_manager.settings["passwords"]["admin"] = hash_password(new_pwd)
        self.app.data_manager.save_settings()
        self.edit_new_pass.clear()
        QMessageBox.information(self, "Muvaffaqiyatli", "Admin paroli muvaffaqiyatli yangilandi!")

    def on_theme_changed(self, idx: int):
        theme = "dark" if idx == 0 else "light"
        if hasattr(self.app, "set_theme"):
            self.app.set_theme(theme)

    def on_font_changed(self, val: int):
        if self.app and hasattr(self.app, "data_manager"):
            self.app.data_manager.settings["font_size"] = val
            self.app.data_manager.save_settings()
        if self.app and hasattr(self.app, "update_font_size"):
            self.app.update_font_size(val)

    def upload_to_google_sheet(self):
        sheet_name = self.edit_sheet_id.text().strip()
        if not sheet_name:
            QMessageBox.warning(self, "Xatolik", "Google Sheet nomi yoki URL sini kiriting!")
            return

        from core.config import SERVICE_ACCOUNT_FILE
        if not is_service_account_available():
            QMessageBox.warning(
                self, "Kalit Topilmadi",
                f"Google Cloud service account kalit fayli ({SERVICE_ACCOUNT_FILE}) topilmadi.\n"
                "Iltimos, service_account.json faylini loyiha papkasiga joylashtiring yoki GOOGLE_APPLICATION_CREDENTIALS muhit o'zgaruvchisini o'rnating."
            )
            return

        self.btn_gsheet_upload.setEnabled(False)
        self.btn_gsheet_download.setEnabled(False)
        self.lbl_gsheet_status.setText("☁ Bulutga yuklanmoqda...")
        self.lbl_gsheet_status.setStyleSheet("color: #f59e0b; font-weight: 700;")

        # Sozlamaga saqlab qo'yish
        if self.app and hasattr(self.app, "data_manager"):
            self.app.data_manager.settings["google_sheet_name"] = sheet_name
            self.app.data_manager.save_settings()

        snapshot = list(self.app.data) if hasattr(self.app, "data") else []

        def _task():
            client = get_gspread_client(SERVICE_ACCOUNT_FILE)
            sheet_id = upload_data_to_sheet(client, sheet_name, snapshot)
            return sheet_id

        self._gsheet_worker = WorkerThread(_task, parent=self)
        self._gsheet_worker.result_ready.connect(self._on_gsheet_upload_done)
        self._gsheet_worker.error_occurred.connect(self._on_gsheet_error)
        self._gsheet_worker.start()

    def _on_gsheet_upload_done(self, sheet_id: str):
        self.btn_gsheet_upload.setEnabled(True)
        self.btn_gsheet_download.setEnabled(True)
        self.lbl_gsheet_status.setText("Holat: Bulutga yuklandi ✅")
        self.lbl_gsheet_status.setStyleSheet("color: #10b981; font-weight: 700;")
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("☁ Ma'lumotlar Google Sheetga yuklandi!", "success")
        reply = QMessageBox.information(
            self, "Muvaffaqiyatli",
            f"Barcha tashkilotlar Google Sheetga muvaffaqiyatli yuklandi!\n\nJadvalni brauzerda ochishni xohlaysizmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                import webbrowser
                webbrowser.open(f"https://docs.google.com/spreadsheets/d/{sheet_id}")
            except Exception:
                pass

    def download_from_google_sheet(self):
        sheet_name = self.edit_sheet_id.text().strip()
        if not sheet_name:
            QMessageBox.warning(self, "Xatolik", "Google Sheet nomi yoki URL sini kiriting!")
            return

        from core.config import SERVICE_ACCOUNT_FILE
        if not is_service_account_available():
            QMessageBox.warning(
                self, "Kalit Topilmadi",
                f"Google Cloud service account kalit fayli ({SERVICE_ACCOUNT_FILE}) topilmadi."
            )
            return

        reply = QMessageBox.question(
            self, "Tasdiqlash",
            "Google Sheetdan yuklab olish mahalliy ma'lumotlar bazasini yangilaydi. Davom etasizmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self.btn_gsheet_upload.setEnabled(False)
        self.btn_gsheet_download.setEnabled(False)
        self.lbl_gsheet_status.setText("📥 Bulutdan yuklab olinmoqda...")
        self.lbl_gsheet_status.setStyleSheet("color: #f59e0b; font-weight: 700;")

        def _task():
            client = get_gspread_client(SERVICE_ACCOUNT_FILE)
            new_data = download_data_from_sheet(client, sheet_name)
            return new_data

        self._gsheet_worker = WorkerThread(_task, parent=self)
        self._gsheet_worker.result_ready.connect(self._on_gsheet_download_done)
        self._gsheet_worker.error_occurred.connect(self._on_gsheet_error)
        self._gsheet_worker.start()

    def _on_gsheet_download_done(self, new_data):
        self.btn_gsheet_upload.setEnabled(True)
        self.btn_gsheet_download.setEnabled(True)
        self.lbl_gsheet_status.setText(f"Holat: {len(new_data)} ta yozuv olindi ✅")
        self.lbl_gsheet_status.setStyleSheet("color: #10b981; font-weight: 700;")

        if new_data:
            if hasattr(self.app, "data"):
                self.app.data = new_data
            if hasattr(self.app, "data_manager"):
                self.app.data_manager.data = new_data
                self.app.data_manager.save_data()
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            elif hasattr(self.app, "filter_data"):
                self.app.filter_data()

            if hasattr(self.app, "show_toast"):
                self.app.show_toast(f"📥 {len(new_data)} ta tashkilot bulutdan yuklandi!", "success")
            QMessageBox.information(self, "Muvaffaqiyatli", f"{len(new_data)} ta tashkilot Google Sheetdan muvaffaqiyatli yuklandi!")
        else:
            QMessageBox.warning(self, "Bo'sh", "Google Sheetda ma'lumot topilmadi.")

    def _on_gsheet_error(self, err_msg: str):
        self.btn_gsheet_upload.setEnabled(True)
        self.btn_gsheet_download.setEnabled(True)
        self.lbl_gsheet_status.setText("Holat: Xatolik yuz berdi ❌")
        self.lbl_gsheet_status.setStyleSheet("color: #ef4444; font-weight: 700;")
        logger.error(f"[GOOGLE SHEETS] Xatolik: {err_msg}")
        QMessageBox.critical(self, "Google Sheets Xatoligi", f"Google Sheets bilan aloqada xatolik yuz berdi:\n\n{err_msg}")

def render_settings(parent: Any, app: Any):
    view = SettingsView(parent=parent, app=app)
    return view
