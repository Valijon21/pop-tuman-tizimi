"""
ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5).
Tanlangan guruhlarga (Mahalla raislari, hokim yordamchilari, maktablar) bir bosishda
shablon yoki favqulodda xabarlarni yuborish.
"""
from typing import Optional, Dict, Any, List
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QComboBox, QTextEdit, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox, QCheckBox
)
from PyQt5.QtCore import Qt
from services.broadcast_service import BroadcastService, SMS_TEMPLATES
from core.logger import logger

class BroadcastView(QDialog):
    """Ommaviy xabarnoma dialog oynasi."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle("📢 Ommaviy Xabarnoma (SMS / Telegram)")
        self.resize(740, 510)
        self.setMinimumSize(620, 390)
        self.setModal(True)

        self.setup_ui()
        self.update_recipients()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(8)

        # Header
        head = QVBoxLayout()
        head.setSpacing(2)
        title = QLabel("📢 Ommaviy Xabarnoma Tarqatish Tizimi")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #38bdf8;")
        sub = QLabel("Mahalla raislari, hokim yordamchilari yoki boshqa tashkilotlarga tezkor xabar yuborish")
        sub.setStyleSheet("font-size: 11px; color: #94a3b8;")
        head.addWidget(title)
        head.addWidget(sub)
        main_layout.addLayout(head)

        # Yuqori parametrlar paneli
        top_grid = QGridLayout()
        top_grid.setSpacing(6)

        # 1. Auditoriya tanlash
        top_grid.addWidget(QLabel("Auditoriya:"), 0, 0)
        self.combo_target = QComboBox()
        self.combo_target.addItems([
            "Barcha Mahallalar (MFY)",
            "Faqat Mahalla Raislari",
            "Faqat Hokim Yordamchilari",
            "Barcha Maktablar",
            "Barcha Bog'chalar (MTT)",
            "Barcha Tashkilotlar",
        ])
        self.combo_target.currentIndexChanged.connect(self.update_recipients)
        top_grid.addWidget(self.combo_target, 0, 1)

        # 2. Shablon tanlash
        top_grid.addWidget(QLabel("Xabar Shabloni:"), 1, 0)
        self.combo_template = QComboBox()
        self.combo_template.addItems(list(SMS_TEMPLATES.keys()))
        self.combo_template.currentIndexChanged.connect(self.on_template_changed)
        top_grid.addWidget(self.combo_template, 1, 1)

        main_layout.addLayout(top_grid)

        # Xabar matni
        lbl_msg = QLabel("Xabar Matni ({nomi}, {fio}, {lavozim} teglari avtomatik to'ldiriladi):")
        lbl_msg.setStyleSheet("font-size: 11px; font-weight: 600; color: #cbd5e1;")
        main_layout.addWidget(lbl_msg)

        self.txt_message = QTextEdit()
        self.txt_message.setPlaceholderText("Xabar matnini kiriting...")
        self.txt_message.setStyleSheet("""
            font-size: 11.5px;
            background-color: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 6px;
        """)
        self.txt_message.setMaximumHeight(70)
        self.txt_message.setPlainText(SMS_TEMPLATES.get(self.combo_template.currentText(), ""))
        main_layout.addWidget(self.txt_message)

        # Qabul qiluvchilar jadvali
        self.lbl_recipients_count = QLabel("Qabul qiluvchilar: 0 ta")
        self.lbl_recipients_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #38bdf8;")
        main_layout.addWidget(self.lbl_recipients_count)

        self.table_recipients = QTableWidget()
        self.table_recipients.setColumnCount(4)
        self.table_recipients.setHorizontalHeaderLabels(["№", "Tashkilot / Mahalla", "Mas'ul F.I.SH", "Telefon"])
        self.table_recipients.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_recipients.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_recipients.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_recipients.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        main_layout.addWidget(self.table_recipients, 1)

        # Yuborish kanallari va tugmalar
        footer = QHBoxLayout()
        footer.setSpacing(12)

        self.chk_telegram = QCheckBox("✈ Telegram Bot orqali")
        self.chk_telegram.setChecked(True)
        self.chk_sms = QCheckBox("📱 SMS orqali")
        self.chk_sms.setChecked(True)

        footer.addWidget(self.chk_telegram)
        footer.addWidget(self.chk_sms)
        footer.addStretch()

        self.btn_send = QPushButton("🚀 Xabarnomani Yuborish")
        self.btn_send.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
            color: white; font-weight: 700; padding: 10px 22px; border-radius: 8px; font-size: 13px;
        """)
        self.btn_send.clicked.connect(self.send_broadcast)
        footer.addWidget(self.btn_send)

        self.btn_close = QPushButton("Yopish")
        self.btn_close.clicked.connect(self.accept)
        footer.addWidget(self.btn_close)

        main_layout.addLayout(footer)

    def on_template_changed(self, idx: int):
        template_name = self.combo_template.currentText()
        if template_name in SMS_TEMPLATES:
            self.txt_message.setPlainText(SMS_TEMPLATES[template_name])

    def update_recipients(self):
        """Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish."""
        if not self.app or not hasattr(self.app, "data"):
            return

        target = self.combo_target.currentText()
        all_data = self.app.data
        filtered = []

        for item in all_data:
            s_val = str(item.get("s", "")).strip()
            lavozim = str(item.get("lavozim", "")).strip().lower()
            izoh = str(item.get("izoh", "")).strip().lower()

            if "Barcha Mahallalar" in target:
                if "Mahalla" in s_val or "MFY" in s_val:
                    filtered.append(item)
            elif "Faqat Mahalla Raislari" in target:
                if ("Mahalla" in s_val or "MFY" in s_val) and ("rais" in lavozim or "rais" in izoh or not lavozim):
                    filtered.append(item)
            elif "Faqat Hokim Yordamchilari" in target:
                if "yordamchi" in lavozim or "yordamchi" in izoh or "hokim" in lavozim:
                    filtered.append(item)
            elif "Barcha Maktablar" in target:
                if "Maktab" in s_val:
                    filtered.append(item)
            elif "Barcha Bog'chalar" in target:
                if "Bog'cha" in s_val or "MTT" in s_val:
                    filtered.append(item)
            else:
                filtered.append(item)

        self.current_recipients = filtered
        self.lbl_recipients_count.setText(f"Qabul qiluvchilar soni: {len(filtered)} ta mas'ul xodim")

        self.table_recipients.setRowCount(len(filtered))
        for r_idx, it in enumerate(filtered):
            self.table_recipients.setItem(r_idx, 0, QTableWidgetItem(str(r_idx + 1)))
            self.table_recipients.setItem(r_idx, 1, QTableWidgetItem(str(it.get("m", "-"))))
            self.table_recipients.setItem(r_idx, 2, QTableWidgetItem(str(it.get("f", "-"))))
            self.table_recipients.setItem(r_idx, 3, QTableWidgetItem(str(it.get("t", "-"))))

    def send_broadcast(self):
        msg_template = self.txt_message.toPlainText().strip()
        if not msg_template:
            QMessageBox.warning(self, "Xatolik", "Xabar matnini kiriting!")
            return

        if not self.current_recipients:
            QMessageBox.warning(self, "Xatolik", "Tanlangan auditoriyada qabul qiluvchilar yo'q!")
            return

        reply = QMessageBox.question(
            self, "Tasdiqlash",
            f"Rostdan ham {len(self.current_recipients)} ta mas'ulga ushbu xabarni yubormoqchimisiz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # Yuborish xizmatini chaqirish
        use_tg = self.chk_telegram.isChecked()
        use_sms = self.chk_sms.isChecked()

        result = BroadcastService.send_broadcast(
            recipients=self.current_recipients,
            template=msg_template,
            channels={"telegram": use_tg, "sms": use_sms}
        )

        sent_count = result.get("sent", len(self.current_recipients))
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"📢 Xabarnoma {sent_count} ta manzilga yuborildi!", "success")

        QMessageBox.information(
            self, "Yuborildi",
            f"Ommaviy xabarnoma muvaffaqiyatli tarqatildi!\n"
            f"Jami yuborildi: {sent_count} ta\n"
            f"Kanal: {'Telegram ' if use_tg else ''}{'SMS' if use_sms else ''}"
        )
        self.accept()

def open_broadcast_dialog(app: Any) -> None:
    dlg = BroadcastView(parent=app, app=app)
    dlg.exec_()
