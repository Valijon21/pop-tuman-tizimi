"""
ui_qt.views.org_edit_dialog: Tashkilot qo'shish va tahrirlash dialogi.
Maydonlarni real-vaqtda tekshirish (INN 9 raqam, JSHSHIR 14 raqam, Pasport formati).
"""
import uuid
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QComboBox, QTextEdit, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from core.validators import (
    validate_inn, validate_phone, clean_inn,
    validate_jshshir, validate_passport_series
)
from core.logger import logger

class OrgEditDialog(QDialog):
    """Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi."""

    def __init__(self, parent=None, app=None, item: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.app = app
        self.item = item or {}
        self.is_edit = bool(item)

        self.setWindowTitle("Tashkilotni Tahrirlash" if self.is_edit else "Yangi Tashkilot Qo'shish")
        self.resize(500, 500)
        self.setMinimumSize(440, 380)
        self.setModal(True)

        self.setup_ui()
        if self.is_edit:
            self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # Sarlavha
        head_layout = QVBoxLayout()
        head_layout.setSpacing(2)
        title_lbl = QLabel("Tashkilotni Tahrirlash" if self.is_edit else "Yangi Tashkilot Qo'shish")
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #38bdf8;")
        sub_lbl = QLabel("Kerakli ma'lumotlarni to'ldiring va saqlash tugmasini bosing")
        sub_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")
        head_layout.addWidget(title_lbl)
        head_layout.addWidget(sub_lbl)
        layout.addLayout(head_layout)

        # Skroll maydoni forma uchun
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        form_widget = QWidget()
        form_grid = QGridLayout(form_widget)
        form_grid.setVerticalSpacing(6)
        form_grid.setHorizontalSpacing(10)
        form_grid.setContentsMargins(0, 4, 4, 4)

        # 1. Turi (Kategoriya)
        form_grid.addWidget(QLabel("Tashkilot Turi:"), 0, 0)
        self.combo_type = QComboBox()
        self.combo_type.setEditable(True)
        categories = ["Mahalla (MFY)", "Maktab", "Bog'cha (MTT)", "Tibbiyot", "Boshqa"]
        if self.app and hasattr(self.app, "data_manager"):
            categories = self.app.data_manager.categories
        self.combo_type.addItems(categories)
        form_grid.addWidget(self.combo_type, 0, 1)

        # 2. Tashkilot Nomi
        form_grid.addWidget(QLabel("Tashkilot Nomi (*):"), 1, 0)
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("Masalan: Chorkesar MFY yoki 22-sonli maktab")
        form_grid.addWidget(self.edit_name, 1, 1)

        # 3. Mas'ul F.I.SH
        form_grid.addWidget(QLabel("Rahbar / Mas'ul (F.I.SH):"), 2, 0)
        self.edit_fio = QLineEdit()
        self.edit_fio.setPlaceholderText("Masalan: Yondashev Xojiakbar")
        form_grid.addWidget(self.edit_fio, 2, 1)

        # 4. Lavozimi
        form_grid.addWidget(QLabel("Lavozimi:"), 3, 0)
        self.edit_lavozim = QLineEdit()
        self.edit_lavozim.setPlaceholderText("Masalan: Rais, Hokim yordamchisi, Direktor")
        form_grid.addWidget(self.edit_lavozim, 3, 1)

        # 5. Telefon
        form_grid.addWidget(QLabel("Telefon:"), 4, 0)
        self.edit_phone = QLineEdit()
        self.edit_phone.setPlaceholderText("+998 90 123-45-67")
        form_grid.addWidget(self.edit_phone, 4, 1)

        # 6. INN (9 xonali)
        form_grid.addWidget(QLabel("INN (9 raqam):"), 5, 0)
        self.edit_inn = QLineEdit()
        self.edit_inn.setPlaceholderText("Masalan: 203599806")
        form_grid.addWidget(self.edit_inn, 5, 1)

        # 7. JSHSHIR (14 xonali PINFL)
        form_grid.addWidget(QLabel("JSHSHIR (PINFL 14 raqam):"), 6, 0)
        self.edit_jshr = QLineEdit()
        self.edit_jshr.setPlaceholderText("Masalan: 30807995910027")
        form_grid.addWidget(self.edit_jshr, 6, 1)

        # 8. Pasport Seriya (AB1234567)
        form_grid.addWidget(QLabel("Pasport Seriya:"), 7, 0)
        self.edit_seriya = QLineEdit()
        self.edit_seriya.setPlaceholderText("Masalan: AB4561091")
        form_grid.addWidget(self.edit_seriya, 7, 1)

        # 9. Izoh
        form_grid.addWidget(QLabel("Izoh:"), 8, 0)
        self.edit_izoh = QTextEdit()
        self.edit_izoh.setPlaceholderText("Qo'shimcha ma'lumotlar...")
        self.edit_izoh.setMaximumHeight(48)
        form_grid.addWidget(self.edit_izoh, 8, 1)

        scroll.setWidget(form_widget)
        layout.addWidget(scroll, 1)

        # Validatsiya indikatori
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("font-size: 10px; color: #f59e0b;")
        layout.addWidget(self.lbl_status)

        # Tugmalar paneli
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_cancel = QPushButton("Bekor Qilish")
        self.btn_cancel.setStyleSheet("padding: 6px 14px; border-radius: 6px; font-size: 11.5px;")
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("💾 Saqlash")
        self.btn_save.setProperty("class", "btn_primary")
        self.btn_save.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6); color: white; font-weight: 700; padding: 6px 18px; border-radius: 6px; font-size: 11.5px;")
        self.btn_save.clicked.connect(self.save)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def load_data(self):
        """Mavjud ma'lumotlarni formaga yuklash."""
        t_val = self.item.get("s", "")
        idx = self.combo_type.findText(t_val)
        if idx >= 0:
            self.combo_type.setCurrentIndex(idx)
        else:
            self.combo_type.setEditText(t_val)

        self.edit_name.setText(str(self.item.get("m", "") or ""))
        self.edit_fio.setText(str(self.item.get("f", "") or ""))
        self.edit_lavozim.setText(str(self.item.get("lavozim", "") or ""))
        self.edit_phone.setText(str(self.item.get("t", "") or ""))
        self.edit_inn.setText(str(self.item.get("inn", "") or ""))
        self.edit_jshr.setText(str(self.item.get("jshr", "") or ""))
        self.edit_seriya.setText(str(self.item.get("seriya", "") or ""))
        self.edit_izoh.setPlainText(str(self.item.get("izoh", "") or ""))

    def save(self):
        """Ma'lumotlarni validatsiya qilish va saqlash."""
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Xatolik", "Tashkilot nomini kiritish majburiy!")
            self.edit_name.setFocus()
            return

        inn = self.edit_inn.text().strip()
        if inn and not validate_inn(inn):
            QMessageBox.warning(self, "Ogohlantirish", f"INN formati noto'g'ri (9 ta raqam bo'lishi lozim): {inn}")

        jshr = self.edit_jshr.text().strip()
        if jshr and not validate_jshshir(jshr):
            QMessageBox.warning(self, "Ogohlantirish", f"JSHSHIR (PINFL) 14 ta raqamdan iborat bo'lishi lozim: {jshr}")

        seriya = self.edit_seriya.text().strip().upper()
        if seriya and not validate_passport_series(seriya):
            QMessageBox.warning(self, "Ogohlantirish", f"Pasport seriyasi formati noto'g'ri (Masalan: AB1234567): {seriya}")

        phone = self.edit_phone.text().strip()
        fio = self.edit_fio.text().strip()
        lavozim = self.edit_lavozim.text().strip()
        turi = self.combo_type.currentText().strip()
        izoh = self.edit_izoh.toPlainText().strip()

        old_fio = self.item.get("f", "") if self.is_edit else ""

        # Ob'ektni shakllantirish
        self.item["s"] = turi
        self.item["m"] = name
        self.item["f"] = fio
        self.item["lavozim"] = lavozim
        self.item["t"] = phone
        self.item["inn"] = inn
        self.item["jshr"] = jshr
        self.item["seriya"] = seriya
        self.item["izoh"] = izoh

        if not self.is_edit:
            self.item["id"] = str(uuid.uuid4())
            if self.app and hasattr(self.app, "data_manager"):
                self.app.data_manager.data.append(self.item)
                self.app.data_manager.save_data()
                logger.info(f"[QT] Yangi tashkilot qo'shildi: {name}")
        else:
            if self.app and hasattr(self.app, "data_manager"):
                self.app.data_manager.save_data()
                # Agar mas'ul xodim o'zgargan bo'lsa, audit tarixiga kiritish
                if old_fio and fio and old_fio != fio:
                    try:
                        self.app.data_manager.sqlite.log_staff_change(
                            org_id=self.item.get("id"),
                            mahalla=name,
                            role=lavozim or "Mas'ul",
                            old_name=old_fio,
                            new_name=fio,
                            change_reason=f"UI orqali tahrirlandi: {izoh}" if izoh else "Kadr almashinuvi"
                        )
                        logger.info(f"[QT] Kadrlar almashinuvi audit qilindi: {old_fio} -> {fio}")
                    except Exception as e:
                        logger.warning(f"Kadr auditida xatolik: {e}")

        self.accept()
