"""
ui_qt.views.settings_view: Tizim sozlamalari sahifasi (PyQt5).
SQLite bazasini boshqarish, Telegram bot integratsiyasi, xavfsizlik va zaxira nusxalar.
"""
from typing import Any
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QSpinBox, QGroupBox,
    QMessageBox, QFileDialog, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from core.security import hash_password
from core.logger import logger

class SettingsView(QWidget):
    """Tizim sozlamalari ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(18)

        # Header
        head = QVBoxLayout()
        title = QLabel("⚙ Tizim Sozlamalari")
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: #38bdf8;")
        sub = QLabel("Xavfsizlik, SQLite ma'lumotlar bazasi zaxirasi va Telegram Bot sozlamalari")
        sub.setStyleSheet("font-size: 13px; color: #94a3b8;")
        head.addWidget(title)
        head.addWidget(sub)
        main_layout.addLayout(head)

        # Skroll maydoni
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        c_layout = QVBoxLayout(container)
        c_layout.setSpacing(20)

        # 1. SQLITE BAZA VA ZAXIRA
        grp_db = QGroupBox("💾 SQLite Ma'lumotlar Bazasi va Zaxira")
        grp_db.setStyleSheet("QGroupBox { font-size: 14px; font-weight: 700; color: #10b981; }")
        db_layout = QVBoxLayout(grp_db)
        db_layout.setSpacing(12)

        self.lbl_db_info = QLabel("Baza joylashuvi: mahalla_tizimi.db")
        self.lbl_db_info.setStyleSheet("color: #94a3b8; font-size: 12px;")
        db_layout.addWidget(self.lbl_db_info)

        db_btns = QHBoxLayout()
        btn_backup = QPushButton("📦 Zaxira Nusxa Yaratish (Backup)")
        btn_backup.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            color: white; font-weight: 700; padding: 10px 18px; border-radius: 8px;
        """)
        btn_backup.clicked.connect(self.create_backup)
        db_btns.addWidget(btn_backup)

        btn_restore = QPushButton("🔄 Zaxiradan Tiklash (Restore)")
        btn_restore.setStyleSheet("""
            background: #334155; color: #cbd5e1; font-weight: 700; padding: 10px 18px; border-radius: 8px;
        """)
        btn_restore.clicked.connect(self.restore_backup)
        db_btns.addWidget(btn_restore)
        db_btns.addStretch()

        db_layout.addLayout(db_btns)
        c_layout.addWidget(grp_db)

        # 2. TELEGRAM BOT INTEGRATSIYASI
        grp_tg = QGroupBox("✈ Telegram Bot Integratsiyasi")
        grp_tg.setStyleSheet("QGroupBox { font-size: 14px; font-weight: 700; color: #0284c7; }")
        tg_layout = QVBoxLayout(grp_tg)
        tg_layout.setSpacing(10)

        tg_grid = QGridLayout()
        tg_grid.addWidget(QLabel("Bot Tokeni:"), 0, 0)
        self.edit_bot_token = QLineEdit()
        self.edit_bot_token.setPlaceholderText("Masalan: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ...")
        tg_grid.addWidget(self.edit_bot_token, 0, 1)

        tg_layout.addLayout(tg_grid)

        tg_btns = QHBoxLayout()
        btn_save_bot = QPushButton("💾 Tokenni Saqlash")
        btn_save_bot.setStyleSheet("background: #0284c7; color: white; font-weight: 700; padding: 8px 16px; border-radius: 8px;")
        btn_save_bot.clicked.connect(self.save_bot_token)
        tg_btns.addWidget(btn_save_bot)

        self.lbl_bot_status = QLabel("Holat: Sozlanmagan")
        self.lbl_bot_status.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")
        tg_btns.addWidget(self.lbl_bot_status)
        tg_btns.addStretch()

        tg_layout.addLayout(tg_btns)
        c_layout.addWidget(grp_tg)

        # 3. XAVFSIZLIK VA PAROL
        grp_sec = QGroupBox("🔒 Xavfsizlik va Admin Paroli")
        grp_sec.setStyleSheet("QGroupBox { font-size: 14px; font-weight: 700; color: #ef4444; }")
        sec_layout = QGridLayout(grp_sec)
        sec_layout.setSpacing(10)

        sec_layout.addWidget(QLabel("Yangi Admin Paroli:"), 0, 0)
        self.edit_new_pass = QLineEdit()
        self.edit_new_pass.setEchoMode(QLineEdit.Password)
        self.edit_new_pass.setPlaceholderText("Yangi parolni kiriting...")
        sec_layout.addWidget(self.edit_new_pass, 0, 1)

        btn_pass = QPushButton("🔑 Parolni Yangilash")
        btn_pass.setStyleSheet("background: #dc2626; color: white; font-weight: 700; padding: 8px 16px; border-radius: 8px;")
        btn_pass.clicked.connect(self.update_password)
        sec_layout.addWidget(btn_pass, 0, 2)

        c_layout.addWidget(grp_sec)

        # 4. KO'RINISH VA SHRIFT
        grp_ui = QGroupBox("🎨 Interfeys Sozlamalari")
        grp_ui.setStyleSheet("QGroupBox { font-size: 14px; font-weight: 700; color: #f59e0b; }")
        ui_layout = QHBoxLayout(grp_ui)

        ui_layout.addWidget(QLabel("Mavzu:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["🌙 Tungi (Dark)", "☀ Kunduzi (Light)"])
        self.combo_theme.currentIndexChanged.connect(self.on_theme_changed)
        ui_layout.addWidget(self.combo_theme)

        ui_layout.addSpacing(20)
        ui_layout.addWidget(QLabel("Shrift O'lchami:"))
        self.spin_font = QSpinBox()
        self.spin_font.setRange(11, 22)
        self.spin_font.setValue(13)
        self.spin_font.valueChanged.connect(self.on_font_changed)
        ui_layout.addWidget(self.spin_font)

        ui_layout.addStretch()
        c_layout.addWidget(grp_ui)

        c_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)

    def load_settings(self):
        """Mavjud sozlamalarni yuklash."""
        if not self.app or not hasattr(self.app, "data_manager"):
            return

        settings = self.app.data_manager.settings
        # Bot token
        token = settings.get("telegram_bot_token", "")
        self.edit_bot_token.setText(token)
        if token:
            self.lbl_bot_status.setText("Holat: Token sozlangan 🟢")
            self.lbl_bot_status.setStyleSheet("color: #10b981; font-weight: 700;")

        # Shrift
        font_size = settings.get("font_size", 13)
        self.spin_font.setValue(font_size)

        # SQLite hajmi
        db_path = getattr(self.app.data_manager.sqlite, "db_path", "mahalla_tizimi.db")
        if os.path.exists(db_path):
            size_kb = os.path.getsize(db_path) / 1024
            self.lbl_db_info.setText(f"SQLite Baza: {db_path} ({size_kb:.1f} KB) | Rejim: WAL (ACID)")

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
            if hasattr(self.app, "filter_data"):
                self.app.filter_data()
            QMessageBox.information(self, "Muvaffaqiyatli", "Baza zaxiradan muvaffaqiyatli tiklandi!")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Tiklashda xatolik: {e}")

    def save_bot_token(self):
        token = self.edit_bot_token.text().strip()
        self.app.data_manager.settings["telegram_bot_token"] = token
        self.app.data_manager.save_settings()
        self.lbl_bot_status.setText("Holat: Token saqlandi 🟢" if token else "Holat: Token o'chirildi ⚪")
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Telegram token saqlandi!", "success")

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

def render_settings(parent: Any, app: Any):
    view = SettingsView(parent=parent, app=app)
    return view
