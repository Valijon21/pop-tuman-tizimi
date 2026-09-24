"""
ui_qt.views.org_edit_dialog: Tashkilot qo'shish va tahrirlash dialogi (PyQt5).
Senior darajadagi validatsiya, to'liq Dark/Light mavzu, Buxgalter va kadrlar tarixi integratsiyasi.
"""
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QComboBox, QTextEdit, QPushButton, QMessageBox,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt
from core.validators import (
    validate_inn, validate_phone, clean_inn, clean_phone,
    validate_jshshir, validate_passport_series
)
from ui_qt.styles import get_stylesheet
from core.logger import logger

class OrgEditDialog(QDialog):
    """Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi."""

    def __init__(self, parent=None, app=None, item: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.app = app
        self.item = item or {}
        self.is_edit = bool(item and not item.get("_is_new"))
        self.current_theme = getattr(app, "current_theme", "dark")

        self.setWindowTitle("Tashkilotni Tahrirlash" if self.is_edit else "Yangi Tashkilot Qo'shish")
        self.resize(520, 520)
        self.setMinimumSize(450, 400)
        self.setModal(True)

        # Mavzuni qo'llash
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()
        if self.item:
            self.load_data()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # Sarlavha
        head_layout = QVBoxLayout()
        head_layout.setSpacing(2)
        title_lbl = QLabel("Tashkilotni Tahrirlash" if self.is_edit else "Yangi Tashkilot Qo'shish")
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #0284c7;" if is_light else "font-size: 15px; font-weight: 800; color: #38bdf8;")
        sub_lbl = QLabel("Kerakli ma'lumotlarni to'ldiring va saqlash tugmasini bosing")
        sub_lbl.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
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
        categories = ["Mahalla (MFY)", "Maktab", "Bog'cha (MTT)", "Hokim yordamchisi", "Yoshlar yetakchisi", "Xotin qizlar", "Ijtimoiy xodim", "Profilaktika inspektori", "Soliq inspektori", "Boshqa"]
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

        # 6. Buxgalter Telefoni
        form_grid.addWidget(QLabel("Buxgalter Telefoni:"), 5, 0)
        self.edit_bux_tel = QLineEdit()
        self.edit_bux_tel.setPlaceholderText("Masalan: 94 592 60 04")
        form_grid.addWidget(self.edit_bux_tel, 5, 1)

        # 7. INN (9 xonali)
        form_grid.addWidget(QLabel("INN (9 raqam):"), 6, 0)
        self.edit_inn = QLineEdit()
        self.edit_inn.setPlaceholderText("Masalan: 203599806")
        form_grid.addWidget(self.edit_inn, 6, 1)

        # 8. JSHSHIR (14 xonali PINFL)
        form_grid.addWidget(QLabel("JSHSHIR (PINFL 14 raqam):"), 7, 0)
        self.edit_jshr = QLineEdit()
        self.edit_jshr.setPlaceholderText("Masalan: 30807995910027")
        form_grid.addWidget(self.edit_jshr, 7, 1)

        # 9. Pasport Seriya (AB1234567)
        form_grid.addWidget(QLabel("Pasport Seriya:"), 8, 0)
        self.edit_seriya = QLineEdit()
        self.edit_seriya.setPlaceholderText("Masalan: AB4561091")
        form_grid.addWidget(self.edit_seriya, 8, 1)

        # 10. Izoh
        form_grid.addWidget(QLabel("Izoh:"), 9, 0)
        self.edit_izoh = QTextEdit()
        self.edit_izoh.setPlaceholderText("Qo'shimcha ma'lumotlar...")
        self.edit_izoh.setMaximumHeight(48)
        form_grid.addWidget(self.edit_izoh, 9, 1)

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
        self.btn_cancel.setProperty("class", "btn_secondary")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("💾 Saqlash")
        self.btn_save.setProperty("class", "btn_primary")
        self.btn_save.setCursor(Qt.PointingHandCursor)
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
        self.edit_bux_tel.setText(str(self.item.get("bux_tel", "") or ""))
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
        if inn:
            is_valid, msg_or_cleaned = validate_inn(inn)
            if not is_valid:
                QMessageBox.warning(self, "Ogohlantirish", f"INN formati noto'g'ri: {msg_or_cleaned}")
                self.edit_inn.setFocus()
                return
            inn = msg_or_cleaned

        jshr = self.edit_jshr.text().strip()
        if jshr:
            is_valid, msg_or_cleaned = validate_jshshir(jshr)
            if not is_valid:
                QMessageBox.warning(self, "Ogohlantirish", f"JSHSHIR noto'g'ri: {msg_or_cleaned}")
                self.edit_jshr.setFocus()
                return
            jshr = msg_or_cleaned

        seriya = self.edit_seriya.text().strip().upper()
        if seriya:
            is_valid, msg_or_cleaned = validate_passport_series(seriya)
            if not is_valid:
                QMessageBox.warning(self, "Ogohlantirish", f"Pasport seriya formati noto'g'ri: {msg_or_cleaned}")
                self.edit_seriya.setFocus()
                return
            seriya = msg_or_cleaned

        phone = self.edit_phone.text().strip()
        bux_tel = self.edit_bux_tel.text().strip()

        # O'zgarishlarni tayyorlash
        data_to_save = {
            "s": self.combo_type.currentText().strip(),
            "m": name,
            "f": self.edit_fio.text().strip(),
            "lavozim": self.edit_lavozim.text().strip(),
            "t": phone,
            "bux_tel": bux_tel,
            "inn": inn,
            "jshr": jshr,
            "seriya": seriya,
            "izoh": self.edit_izoh.toPlainText().strip()
        }

        if self.is_edit:
            data_to_save["id"] = self.item.get("id")
            # Kadrlar almashinuvi auditini tekshirish
            old_f = self.item.get("f", "")
            new_f = data_to_save["f"]
            old_t = self.item.get("t", "")
            new_t = data_to_save["t"]

            if (old_f and new_f and old_f != new_f) or (old_t and new_t and old_t != new_t):
                if hasattr(self.app, "data_manager") and hasattr(self.app.data_manager, "sqlite"):
                    self.app.data_manager.sqlite.add_staff_history(
                        org_id=self.item.get("id", ""),
                        mahalla=name,
                        role=data_to_save["lavozim"] or data_to_save["s"],
                        full_name=new_f,
                        phone=new_t,
                        inn=inn,
                        jshr=jshr,
                        seriya=seriya,
                        old_fio=old_f,
                        new_fio=new_f,
                        old_phone=old_t,
                        new_phone=new_t,
                        changed_by="ADMIN (UI)",
                        reason="Tahrirlash oynasi orqali o'zgartirildi"
                    )

            if hasattr(self.app, "data_manager"):
                self.app.data_manager.update_organization(data_to_save)
        else:
            if hasattr(self.app, "data_manager"):
                self.app.data_manager.add_organization(data_to_save)

        self.accept()
