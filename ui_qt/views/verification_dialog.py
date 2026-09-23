"""
ui_qt.views.verification_dialog: 'Verifikatsiya so'rovi' shablonini generatsiya qilish,
nusxalash va Telegram orqali yuborish dialogi (PyQt5).
To'liq Dark va Light rejimini qo'llab-quvvatlaydi, High-DPI va tezkor yuklanish.
"""
import pyperclip
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QComboBox, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt
from services.verification_service import build_verification_text
from ui_qt.styles import get_stylesheet
from core.logger import logger

class VerificationDialog(QDialog):
    """Verifikatsiya so'rovi shablon oynasi."""

    def __init__(self, parent=None, app=None, item: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.app = app
        self.item = item
        self.current_theme = getattr(app, "current_theme", "dark")

        self.setWindowTitle("🛡 Verifikatsiya So'rovi Shablon")
        self.resize(490, 410)
        self.setMinimumSize(420, 320)
        self.setModal(True)

        # Mavzuni qo'llash
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()
        if self.item:
            self.load_item(self.item)

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Sarlavha
        title_lbl = QLabel("🛡 Verifikatsiya So'rovi")
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #0284c7;" if is_light else "font-size: 15px; font-weight: 800; color: #38bdf8;")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel("Tashkilot mas'ul xodimi uchun verifikatsiya so'rov matni:")
        desc_lbl.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        layout.addWidget(desc_lbl)

        # Tashkilot tanlash (tezkor blockSignals bilan)
        select_layout = QHBoxLayout()
        lbl_org = QLabel("Tashkilot:")
        lbl_org.setStyleSheet("font-weight: 600;")
        select_layout.addWidget(lbl_org)

        self.combo_orgs = QComboBox()
        self.combo_orgs.setEditable(True)
        self.combo_orgs.blockSignals(True)
        if self.app and hasattr(self.app, "data"):
            for org in self.app.data:
                display_name = f"{org.get('m', '')} (INN: {org.get('inn', '-')})"
                self.combo_orgs.addItem(display_name, org)
        self.combo_orgs.blockSignals(False)
        self.combo_orgs.currentIndexChanged.connect(self.on_org_changed)
        select_layout.addWidget(self.combo_orgs, 1)
        layout.addLayout(select_layout)

        # Matn maydoni (Mavzuga mos konsol/shablon dizayni)
        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(False)
        bg = "#f8fafc" if is_light else "#1e293b"
        fg = "#0369a1" if is_light else "#38bdf8"
        border = "#cbd5e1" if is_light else "#334155"
        self.txt_preview.setStyleSheet(f"""
            QTextEdit {{
                font-family: 'Consolas', 'Segoe UI', monospace;
                font-size: 12px;
                background-color: {bg};
                color: {fg};
                border: 1.5px solid {border};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        layout.addWidget(self.txt_preview, 1)

        # Tugmalar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_copy = QPushButton("📋 Nusxalash")
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
                color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px; font-size: 11.5px;
            }
            QPushButton:hover { background-color: #0369a1; }
        """)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)

        self.btn_telegram = QPushButton("✈ Telegramga Yuborish")
        self.btn_telegram.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6);
                color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px; font-size: 11.5px;
            }
            QPushButton:hover { background-color: #1d4ed8; }
        """)
        self.btn_telegram.clicked.connect(self.send_to_telegram)

        self.btn_close = QPushButton("Yopish")
        close_bg = "#e2e8f0" if is_light else "#334155"
        close_fg = "#334155" if is_light else "#f8fafc"
        self.btn_close.setStyleSheet(f"background: {close_bg}; color: {close_fg}; font-weight: 700; padding: 6px 14px; border-radius: 6px; font-size: 11.5px;")
        self.btn_close.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_telegram)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

    def load_item(self, item: Dict[str, Any]):
        """Tanlangan tashkilot ma'lumotlarini yuklash."""
        self.item = item
        text = build_verification_text(item)
        self.txt_preview.setPlainText(text)

        inn = item.get("inn", "")
        for idx in range(self.combo_orgs.count()):
            org = self.combo_orgs.itemData(idx)
            if org and org.get("inn") == inn and org.get("m") == item.get("m"):
                self.combo_orgs.setCurrentIndex(idx)
                break

    def on_org_changed(self, idx: int):
        org = self.combo_orgs.itemData(idx)
        if org:
            self.item = org
            text = build_verification_text(org)
            self.txt_preview.setPlainText(text)

    def copy_to_clipboard(self):
        text = self.txt_preview.toPlainText()
        if text.strip():
            pyperclip.copy(text)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("Verifikatsiya so'rovi nusxalandi! 📋", "success")
            QMessageBox.information(self, "Nusxalandi", "Verifikatsiya so'rov matni xotiraga nusxalandi! 📋")

    def send_to_telegram(self):
        text = self.txt_preview.toPlainText()
        if not text.strip():
            return

        try:
            from services.telegram_bot import TelegramBotService
            token = ""
            if self.app and hasattr(self.app, "data_manager"):
                token = self.app.data_manager.settings.get("telegram_bot_token", "")
            if token:
                bot = TelegramBotService(token)
                res = bot.broadcast_message(text)
                sent = res.get("sent", 0)
                if sent > 0:
                    QMessageBox.information(self, "Telegram", f"Xabar {sent} ta Telegram bot obunachisiga yuborildi! ✈")
                else:
                    QMessageBox.warning(self, "Telegram", "Bot obunachilari mavjud emas. Avval botga /start bosing.")
            else:
                QMessageBox.information(self, "Telegram", "Telegram bot tokeni sozlanmagan. Sozlamalar menyusida botni ulang.")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Telegram yuborishda xatolik: {e}")

def copy_verification_quick(app: Any, item: Optional[Dict[str, Any]] = None) -> None:
    """Oynani ochmasdan tezkor nusxalash."""
    if not item:
        return
    text = build_verification_text(item)
    pyperclip.copy(text)
    if hasattr(app, "show_toast"):
        app.show_toast(f"🛡 {item.get('m', 'Tashkilot')} verifikatsiya matni nusxalandi!", "success")
    logger.info(f"[QT] Tezkor verifikatsiya matni nusxalandi: {item.get('m')}")

def open_verification_dialog(app: Any, item: Optional[Dict[str, Any]] = None) -> None:
    dialog = VerificationDialog(parent=app, app=app, item=item)
    dialog.exec_()
