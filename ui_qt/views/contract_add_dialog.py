"""
ui_qt.views.contract_add_dialog: Shartnoma va Ulanish ma'lumotini qo'shish/tahrirlash dialogi (PyQt5).
Professional Fluent UI dizayn, to'liq Dark/Light mavzu, INN va telefon validatsiyasi.
"""
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QComboBox, QTextEdit, QPushButton, QMessageBox,
    QScrollArea, QWidget, QFrame, QSpinBox
)
from PyQt5.QtCore import Qt
from core.validators import validate_inn, clean_inn
from ui_qt.styles import get_stylesheet
from core.logger import logger


class ContractAddDialog(QDialog):
    """Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi."""

    def __init__(self, parent=None, app=None, item: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.app = app
        self.item = item or {}
        self.is_edit = bool(item and (item.get("id") or item.get("inn") or item.get("m") or item.get("organization_name")))
        self.current_theme = getattr(app, "current_theme", "dark")

        self.setWindowTitle(
            "📑 Shartnoma Ma'lumotini Tahrirlash" if self.is_edit
            else "📑 Yangi Shartnoma / Ulanish Qo'shish"
        )
        self.resize(540, 500)
        self.setMinimumSize(460, 400)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()
        if self.item:
            self.load_data()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # ── Sarlavha ──
        head_layout = QVBoxLayout()
        head_layout.setSpacing(2)

        title_text = (
            "📑 Shartnoma Ma'lumotini Tahrirlash" if self.is_edit
            else "📑 Yangi Shartnoma / Ulanish Qo'shish"
        )
        title_lbl = QLabel(title_text)
        title_color = "#0284c7" if is_light else "#38bdf8"
        title_lbl.setStyleSheet(
            f"font-size: 15px; font-weight: 800; color: {title_color};"
        )

        sub_lbl = QLabel(
            "Tashkilotning shartnoma, apparat shtati va ulanish ma'lumotlarini kiriting"
        )
        sub_color = "#64748b" if is_light else "#94a3b8"
        sub_lbl.setStyleSheet(f"font-size: 11px; color: {sub_color};")

        head_layout.addWidget(title_lbl)
        head_layout.addWidget(sub_lbl)
        layout.addLayout(head_layout)

        # ── Forma (Skroll ichida) ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        form_widget = QWidget()
        form_grid = QGridLayout(form_widget)
        form_grid.setVerticalSpacing(8)
        form_grid.setHorizontalSpacing(10)
        form_grid.setContentsMargins(0, 6, 4, 4)

        row = 0

        # 1. Tashkilot Nomi (*)
        form_grid.addWidget(self._make_label("Tashkilot Nomi (*):"), row, 0)
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("Masalan: Chorkesar MFY yoki 22-sonli maktab")
        form_grid.addWidget(self.edit_name, row, 1)
        row += 1

        # 2. INN
        form_grid.addWidget(self._make_label("INN (9 raqam):"), row, 0)
        self.edit_inn = QLineEdit()
        self.edit_inn.setPlaceholderText("Masalan: 203599806")
        form_grid.addWidget(self.edit_inn, row, 1)
        row += 1

        # 3. Toifasi
        form_grid.addWidget(self._make_label("Toifasi:"), row, 0)
        self.combo_category = QComboBox()
        self.combo_category.setEditable(True)
        categories = [
            "Mahalla (MFY)", "Maktab", "Bog'cha (MTT)",
            "Hokim yordamchisi", "Tibbiyot", "Boshqa"
        ]
        if self.app and hasattr(self.app, "data_manager"):
            categories = self.app.data_manager.categories
        self.combo_category.addItems(categories)
        form_grid.addWidget(self.combo_category, row, 1)
        row += 1

        # 4. Apparat Shtati
        form_grid.addWidget(self._make_label("Apparat Shtati (soni):"), row, 0)
        self.spin_aparat = QSpinBox()
        self.spin_aparat.setRange(0, 9999)
        self.spin_aparat.setValue(0)
        self.spin_aparat.setSpecialValueText("—")
        form_grid.addWidget(self.spin_aparat, row, 1)
        row += 1

        # 5. Ulangan Xodimlar
        form_grid.addWidget(self._make_label("Ulangan Xodimlar (litsenziya):"), row, 0)
        self.spin_ulangan = QSpinBox()
        self.spin_ulangan.setRange(0, 9999)
        self.spin_ulangan.setValue(0)
        self.spin_ulangan.setSpecialValueText("—")
        form_grid.addWidget(self.spin_ulangan, row, 1)
        row += 1

        # 6. Rahbar F.I.SH
        form_grid.addWidget(self._make_label("Rahbar F.I.SH:"), row, 0)
        self.edit_fio = QLineEdit()
        self.edit_fio.setPlaceholderText("Masalan: Yondashev Xojiakbar")
        form_grid.addWidget(self.edit_fio, row, 1)
        row += 1

        # 7. Rahbar Telefoni
        form_grid.addWidget(self._make_label("Rahbar Telefoni:"), row, 0)
        self.edit_phone = QLineEdit()
        self.edit_phone.setPlaceholderText("+998 90 123-45-67")
        form_grid.addWidget(self.edit_phone, row, 1)
        row += 1

        # 8. Buxgalter Telefoni
        form_grid.addWidget(self._make_label("Buxgalter Telefoni:"), row, 0)
        self.edit_bux_tel = QLineEdit()
        self.edit_bux_tel.setPlaceholderText("Masalan: 94 592 60 04")
        form_grid.addWidget(self.edit_bux_tel, row, 1)
        row += 1

        # 9. Izoh
        form_grid.addWidget(self._make_label("Izoh:"), row, 0)
        self.edit_izoh = QTextEdit()
        self.edit_izoh.setPlaceholderText("Qo'shimcha ma'lumotlar yoki eslatmalar...")
        self.edit_izoh.setMaximumHeight(52)
        form_grid.addWidget(self.edit_izoh, row, 1)
        row += 1

        scroll.setWidget(form_widget)
        layout.addWidget(scroll, 1)

        # ── Validatsiya indikatori ──
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("font-size: 10px; color: #f59e0b;")
        layout.addWidget(self.lbl_status)

        # ── Tugmalar paneli ──
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

    def _make_label(self, text: str) -> QLabel:
        """Forma label yaratish (mavzuga mos rang bilan)."""
        lbl = QLabel(text)
        is_light = (self.current_theme == "light")
        color = "#334155" if is_light else "#cbd5e1"
        lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {color};")
        return lbl

    def load_data(self):
        """Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi)."""
        name = self.item.get("m") or self.item.get("organization_name") or ""
        self.edit_name.setText(str(name))
        self.edit_inn.setText(str(self.item.get("inn", "") or ""))

        # Toifani tanlash
        cat_val = self.item.get("s") or self.item.get("category") or ""
        idx = self.combo_category.findText(str(cat_val))
        if idx >= 0:
            self.combo_category.setCurrentIndex(idx)
        else:
            self.combo_category.setEditText(str(cat_val))

        # Apparat va ulangan
        aparat = self.item.get("aparat_soni") if "aparat_soni" in self.item else self.item.get("apparat_count")
        self.spin_aparat.setValue(int(aparat) if aparat is not None else 0)

        ulangan = self.item.get("ulangan_soni") if "ulangan_soni" in self.item else self.item.get("connected_count")
        self.spin_ulangan.setValue(int(ulangan) if ulangan is not None else 0)

        # Kontakt ma'lumotlari
        self.edit_fio.setText(str(self.item.get("f") or self.item.get("leader_name") or ""))
        self.edit_phone.setText(str(self.item.get("t") or self.item.get("phone") or ""))
        self.edit_bux_tel.setText(str(self.item.get("bux_tel") or self.item.get("accountant_phone") or ""))
        self.edit_izoh.setPlainText(str(self.item.get("izoh") or self.item.get("notes") or ""))

    def save(self):
        """Ma'lumotlarni validatsiya qilish va saqlash."""
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(
                self, "Xatolik",
                "Tashkilot nomini kiritish majburiy!"
            )
            self.edit_name.setFocus()
            return

        inn = self.edit_inn.text().strip()
        if inn:
            is_valid, msg_or_cleaned = validate_inn(inn)
            if not is_valid:
                QMessageBox.warning(
                    self, "Ogohlantirish",
                    f"INN formati noto'g'ri: {msg_or_cleaned}"
                )
                self.edit_inn.setFocus()
                return
            inn = msg_or_cleaned

        # Apparat va ulangan qiymatlarini olish
        aparat_val = self.spin_aparat.value() if self.spin_aparat.value() > 0 else None
        ulangan_val = self.spin_ulangan.value() if self.spin_ulangan.value() > 0 else None

        # Ma'lumotlarni tayyorlash
        data_to_save = {
            "s": self.combo_category.currentText().strip(),
            "m": name,
            "f": self.edit_fio.text().strip(),
            "t": self.edit_phone.text().strip(),
            "inn": inn,
            "bux_tel": self.edit_bux_tel.text().strip(),
            "aparat_soni": aparat_val,
            "ulangan_soni": ulangan_val,
            "izoh": self.edit_izoh.toPlainText().strip(),
        }

        if self.is_edit:
            # Mavjud yozuvni yangilash
            data_to_save["id"] = self.item.get("id")

            # item dict ni to'g'ridan-to'g'ri yangilash
            for key, val in data_to_save.items():
                self.item[key] = val

            if hasattr(self.app, "data_manager"):
                self.app.data_manager.update_organization(data_to_save)
                logger.info(
                    f"[SHARTNOMA] Tahrirlandi: {name} (INN: {inn or '-'})"
                )
        else:
            # Yangi yozuv qo'shish
            if hasattr(self.app, "data_manager"):
                self.app.data_manager.add_organization(data_to_save)
                logger.info(
                    f"[SHARTNOMA] Yangi qo'shildi: {name} (INN: {inn or '-'})"
                )

        self.accept()

    def exec_(self) -> int:
        """Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish."""
        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self.parent() or self):
                return QDialog.Rejected
        return super().exec_()
