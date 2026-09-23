"""
ui_qt.views.cabinet_dialog: 'Kabinetga dostup' shablonini generatsiya qilish,
bir bosishda nusxalash va Telegramga yuborish dialogi (PyQt5).
"""
import pyperclip
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QComboBox, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt
from services.cabinet_service import build_cabinet_access_text
from core.logger import logger

class CabinetDialog(QDialog):
    """Kabinetga dostup shablon oynasi."""

    def __init__(self, parent=None, app=None, item: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.app = app
        self.item = item
        self.setWindowTitle("🔑 Kabinetga Dostup Shablon")
        self.setFixedSize(520, 480)
        self.setModal(True)

        self.setup_ui()
        if self.item:
            self.load_item(self.item)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # Sarlavha
        title_lbl = QLabel("🔑 Kabinetga Dostup So'rovi")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #f59e0b;")
        layout.addWidget(title_lbl)

        desc_lbl = QLabel("Soliq yoki davlat xizmatlari kabinetiga kirish uchun standart shablon matni:")
        desc_lbl.setStyleSheet("font-size: 12px; color: #94a3b8;")
        layout.addWidget(desc_lbl)

        # Tashkilot tanlash (agar bittasi tanlanmagan bo'lsa)
        select_layout = QHBoxLayout()
        select_layout.addWidget(QLabel("Tashkilot:"))
        self.combo_orgs = QComboBox()
        self.combo_orgs.setEditable(True)
        if self.app and hasattr(self.app, "data"):
            for org in self.app.data:
                display_name = f"{org.get('m', '')} (INN: {org.get('inn', '-')})"
                self.combo_orgs.addItem(display_name, org)
        self.combo_orgs.currentIndexChanged.connect(self.on_org_changed)
        select_layout.addWidget(self.combo_orgs)
        layout.addLayout(select_layout)

        # Matn maydoni
        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(False)
        self.txt_preview.setStyleSheet("""
            font-family: 'Consolas', 'Segoe UI', monospace;
            font-size: 14px;
            background-color: #1e293b;
            color: #38bdf8;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 12px;
        """)
        layout.addWidget(self.txt_preview)

        # Tugmalar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_copy = QPushButton("📋 Nusxalash")
        self.btn_copy.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d97706, stop:1 #f59e0b);
            color: white; font-weight: 700; padding: 10px 18px; border-radius: 8px;
        """)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)

        self.btn_telegram = QPushButton("✈ Telegramga Yuborish")
        self.btn_telegram.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
            color: white; font-weight: 700; padding: 10px 18px; border-radius: 8px;
        """)
        self.btn_telegram.clicked.connect(self.send_to_telegram)

        self.btn_close = QPushButton("Yopish")
        self.btn_close.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_telegram)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

    def load_item(self, item: Dict[str, Any]):
        """Belgilangan tashkilot bo'yicha matnni generatsiya qilish."""
        text = build_cabinet_access_text(item)
        self.txt_preview.setPlainText(text)
        # Comboboxda mos keluvchi elementni tanlash
        target_inn = item.get("inn", "")
        for idx in range(self.combo_orgs.count()):
            org_data = self.combo_orgs.itemData(idx)
            if org_data and org_data.get("inn") == target_inn:
                self.combo_orgs.setCurrentIndex(idx)
                break

    def on_org_changed(self, index: int):
        org_data = self.combo_orgs.itemData(index)
        if org_data:
            text = build_cabinet_access_text(org_data)
            self.txt_preview.setPlainText(text)

    def copy_to_clipboard(self):
        text = self.txt_preview.toPlainText().strip()
        if text:
            pyperclip.copy(text)
            if self.app and hasattr(self.app, "show_toast"):
                self.app.show_toast("Kabinetga dostup matni nusxalandi! 📋", "success")
            else:
                QMessageBox.information(self, "Muvaffaqiyatli", "Shablon matni xotiraga (clipboard) nusxalandi!")

    def send_to_telegram(self):
        text = self.txt_preview.toPlainText().strip()
        if not text:
            return
        try:
            from services.telegram_bot import get_telegram_bot_service
            bot = get_telegram_bot_service()
            if bot.is_configured():
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

def copy_cabinet_quick(app: Any, item: Optional[Dict[str, Any]] = None) -> None:
    """Oynani ochmasdan tezkor nusxalash."""
    if not item:
        return
    text = build_cabinet_access_text(item)
    pyperclip.copy(text)
    if hasattr(app, "show_toast"):
        app.show_toast(f"🔑 {item.get('m', 'Tashkilot')} kabinet matni nusxalandi!", "success")
    logger.info(f"[QT] Tezkor kabinet matni nusxalandi: {item.get('m')}")

def open_cabinet_dialog(app: Any, item: Optional[Dict[str, Any]] = None) -> None:
    dialog = CabinetDialog(parent=app, app=app, item=item)
    dialog.exec_()
