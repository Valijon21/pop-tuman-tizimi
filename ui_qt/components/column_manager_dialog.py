"""
ui_qt.components.column_manager_dialog: Professional Ustunlarni Boshqarish va Qo'shish Dialogi.
Tashkilotlar bosh jadvali va Shartnoma & ulanishlar monitoringi uchun dinamik ustunlar yaratish,
mavjud tizim maydonlarini yoqish hamda istalgan maxsus ustunlarni qo'shish imkoniyatini beradi.
"""
from typing import List, Dict, Any, Optional
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QComboBox, QSpinBox, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QGroupBox
)
from PyQt5.QtCore import Qt
from ui_qt.styles import get_stylesheet
from services.search_service import transliterate_to_latin

class ColumnManagerDialog(QDialog):
    """Jadvallar uchun dinamik ustunlar qo'shish va sozlash oynasi."""

    SYSTEM_FIELDS_TABLE = [
        ("📞 Buxgalter telefoni", "bux_tel", 140),
        ("👥 Apparat shtati soni", "aparat_soni", 110),
        ("🔗 Ulangan litsenziyalar soni", "ulangan_soni", 110),
        ("💼 Lavozimi", "lavozim", 140),
        ("🆔 JSHSHIR (14 xonali PINFL)", "jshr", 140),
        ("📄 Pasport seriya va raqami", "seriya", 130),
    ]

    SYSTEM_FIELDS_CONTRACTS = [
        ("👤 Rahbar F.I.SH", "f", 200),
        ("📝 Izoh", "izoh", 180),
        ("💼 Lavozimi", "lavozim", 140),
        ("🆔 JSHSHIR (14 xonali PINFL)", "jshr", 140),
        ("📄 Pasport seriya va raqami", "seriya", 130),
    ]

    def __init__(self, view_type: str = "table", current_columns: Optional[List[Dict[str, Any]]] = None, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.view_type = view_type  # "table" yoki "contracts"
        self.current_theme = getattr(app, "current_theme", "dark")
        self.columns: List[Dict[str, Any]] = [dict(c) for c in (current_columns or [])]

        title = "Tashkilotlar Jadvaliga Ustun Qo'shish" if view_type == "table" else "Shartnomalar Jadvaliga Ustun Qo'shish"
        self.setWindowTitle(title)
        self.resize(540, 520)
        self.setMinimumSize(480, 440)
        self.setModal(True)

        self.setStyleSheet(get_stylesheet(self.current_theme))
        self.setup_ui()
        self.render_columns_table()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        # 1. Sarlavha
        head = QVBoxLayout()
        head.setSpacing(2)
        lbl_title = QLabel("⚙ Jadval Ustunlarini Boshqarish")
        lbl_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0284c7;" if is_light else "font-size: 15px; font-weight: 800; color: #38bdf8;")
        lbl_sub = QLabel("Jadvalga tayyor tizim maydonlarini yoki yangi maxsus ustunlarni qo'shing")
        lbl_sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        head.addWidget(lbl_title)
        head.addWidget(lbl_sub)
        layout.addLayout(head)

        # 2. TAYYOR TIZIM MAYDONLARI BLOKI
        sys_box = QGroupBox("📋 1. Tizimda mavjud tayyor maydonlar")
        sys_box.setStyleSheet(f"font-weight: 700; color: {'#0f172a' if is_light else '#f8fafc'};")
        sys_layout = QHBoxLayout(sys_box)
        sys_layout.setContentsMargins(10, 10, 10, 10)
        sys_layout.setSpacing(8)

        self.combo_sys = QComboBox()
        sys_fields = self.SYSTEM_FIELDS_TABLE if self.view_type == "table" else self.SYSTEM_FIELDS_CONTRACTS
        for name, key, width in sys_fields:
            self.combo_sys.addItem(name, {"name": name, "key": key, "width": width})
        sys_layout.addWidget(self.combo_sys, 1)

        self.btn_add_sys = QPushButton("➕ Tanlanganni qo'shish")
        self.btn_add_sys.setProperty("class", "btn_primary")
        self.btn_add_sys.setCursor(Qt.PointingHandCursor)
        self.btn_add_sys.clicked.connect(self.add_system_field)
        sys_layout.addWidget(self.btn_add_sys)

        layout.addWidget(sys_box)

        # 3. MAXSUS YANGI USTUN YARATISH BLOKI
        custom_box = QGroupBox("✏ 2. Yangi maxsus ustun yaratish")
        custom_box.setStyleSheet(f"font-weight: 700; color: {'#0f172a' if is_light else '#f8fafc'};")
        custom_grid = QGridLayout(custom_box)
        custom_grid.setContentsMargins(10, 10, 10, 10)
        custom_grid.setSpacing(8)

        custom_grid.addWidget(QLabel("Ustun nomi:"), 0, 0)
        self.edit_custom_name = QLineEdit()
        self.edit_custom_name.setPlaceholderText("Masalan: Manzil, Elektron pochta, Shartnoma sanasi...")
        custom_grid.addWidget(self.edit_custom_name, 0, 1)

        custom_grid.addWidget(QLabel("Kengligi:"), 1, 0)
        spin_layout = QHBoxLayout()
        self.spin_width = QSpinBox()
        self.spin_width.setRange(70, 450)
        self.spin_width.setValue(150)
        self.spin_width.setSuffix(" px")
        spin_layout.addWidget(self.spin_width)

        self.btn_add_custom = QPushButton("➕ Maxsus ustun qo'shish")
        self.btn_add_custom.setProperty("class", "btn_success")
        self.btn_add_custom.setCursor(Qt.PointingHandCursor)
        self.btn_add_custom.clicked.connect(self.add_custom_field)
        spin_layout.addWidget(self.btn_add_custom)

        custom_grid.addLayout(spin_layout, 1, 1)
        layout.addWidget(custom_box)

        # 4. HOZIRGI QO'SHILGAN USTUNLAR JADVALI
        lbl_list = QLabel("📌 Hozirda qo'shilgan ustunlar ro'yxati:")
        lbl_list.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {'#334155' if is_light else '#cbd5e1'};")
        layout.addWidget(lbl_list)

        self.table_cols = QTableWidget()
        self.table_cols.setColumnCount(4)
        self.table_cols.setHorizontalHeaderLabels(["№", "Ustun Nomi", "Kengligi", "Amal"])
        h = self.table_cols.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_cols.verticalHeader().setVisible(False)
        self.table_cols.setAlternatingRowColors(True)
        layout.addWidget(self.table_cols, 1)

        # 5. DIALOG FOOTER TUGMALARI
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.lbl_info = QLabel("💡 Qo'shilgan ustunlar avtomatik saqlanadi")
        self.lbl_info.setStyleSheet("font-size: 11px; color: #64748b;")
        btn_layout.addWidget(self.lbl_info)
        btn_layout.addStretch()

        self.btn_cancel = QPushButton("Bekor qilish")
        self.btn_cancel.setProperty("class", "btn_secondary")
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("💾 Saqlash va Qo'llash")
        self.btn_save.setProperty("class", "btn_primary")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_and_apply)
        btn_layout.addWidget(self.btn_save)

        layout.addLayout(btn_layout)

    def render_columns_table(self):
        """Hozirgi qo'shilgan ustunlar jadvalini to'ldirish."""
        self.table_cols.setRowCount(len(self.columns))
        for r, col in enumerate(self.columns):
            # 0. №
            it_no = QTableWidgetItem(str(r + 1))
            it_no.setTextAlignment(Qt.AlignCenter)
            self.table_cols.setItem(r, 0, it_no)

            # 1. Nomi
            it_name = QTableWidgetItem(str(col.get("name", "")))
            self.table_cols.setItem(r, 1, it_name)

            # 2. Kengligi
            it_w = QTableWidgetItem(f"{col.get('width', 150)} px")
            it_w.setTextAlignment(Qt.AlignCenter)
            self.table_cols.setItem(r, 2, it_w)

            # 3. O'chirish tugmasi
            btn_del = QPushButton("🗑 O'chirish")
            btn_del.setProperty("class", "btn_danger")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setFixedSize(85, 24)
            btn_del.clicked.connect(lambda _, idx=r: self.remove_column(idx))
            self.table_cols.setCellWidget(r, 3, btn_del)

    def add_system_field(self):
        """Mavjud tizim maydonini ro'yxatga qo'shish."""
        data = self.combo_sys.currentData()
        if not data:
            return

        key = data["key"]
        # Tekshirish: allaqachon qo'shilganmi?
        for c in self.columns:
            if c.get("key") == key:
                QMessageBox.warning(self, "Ogohlantirish", f"'{data['name']}' ustuni allaqachon jadvalga qo'shilgan!")
                return

        self.columns.append({
            "name": data["name"],
            "key": key,
            "width": data["width"]
        })
        self.render_columns_table()

    def add_custom_field(self):
        """Foydalanuvchi kiritgan maxsus ustunni qo'shish."""
        name = self.edit_custom_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Xatolik", "Iltimos, ustun nomini kiriting!")
            return

        # Tekshirish: nom takrorlanmasligi kerak
        for c in self.columns:
            if c.get("name", "").lower() == name.lower():
                QMessageBox.warning(self, "Ogohlantirish", f"'{name}' nomli ustun allaqachon mavjud!")
                return

        # Xavfsiz identifikator kalit (key) yaratish
        latin_name = transliterate_to_latin(name).lower()
        safe_key = "col_" + "".join(c if c.isalnum() else "_" for c in latin_name).strip("_")
        while "__" in safe_key:
            safe_key = safe_key.replace("__", "_")

        width = self.spin_width.value()
        self.columns.append({
            "name": name,
            "key": safe_key,
            "width": width
        })

        self.edit_custom_name.clear()
        self.render_columns_table()

    def remove_column(self, idx: int):
        """Ustunni ro'yxatdan o'chirish."""
        if 0 <= idx < len(self.columns):
            col_name = self.columns[idx].get("name", "")
            del self.columns[idx]
            self.render_columns_table()

    def save_and_apply(self):
        """O'zgarishlarni saqlash va dialogni yopish."""
        # SQLite da yangi ustunlar mavjudligini kafolatlash
        if self.app and hasattr(self.app, "data_manager") and hasattr(self.app.data_manager, "sqlite"):
            sqlite_mgr = self.app.data_manager.sqlite
            for c in self.columns:
                key = c.get("key")
                if key and key.startswith("col_"):
                    sqlite_mgr.ensure_column_exists(key, "TEXT")

        self.accept()

    def get_columns(self) -> List[Dict[str, Any]]:
        """Tasdiqlangan ustunlar konfiguratsiyasini qaytarish."""
        return self.columns
