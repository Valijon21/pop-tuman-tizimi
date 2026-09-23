"""
ui_qt.views.history_view: Kadrlar almashinuvi va rotatsiyasi tarixi dialogi (PyQt5).
SQLite dagi staff_history jadvalidan to'liq audit yozuvlarini ko'rsatish va saralash.
"""
from typing import Optional, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QComboBox,
    QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from ui_qt.styles import get_stylesheet
from core.logger import logger

class HistoryView(QDialog):
    """Kadrlar tarixi dialog oynasi."""

    def __init__(self, parent=None, app=None, org_id: Optional[str] = None, mahalla: Optional[str] = None):
        super().__init__(parent)
        self.app = app
        self.org_id = org_id
        self.mahalla = mahalla
        self.current_theme = getattr(app, "current_theme", "dark")

        self.setWindowTitle("📜 Kadrlar Almashinuvi va Rotatsiyasi Tarixi (Audit)")
        self.resize(800, 500)
        self.setMinimumSize(640, 380)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header
        head = QVBoxLayout()
        head.setSpacing(2)
        title = QLabel("📜 Kadrlar Almashinuvi Tarixi (Audit)")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #7e22ce;" if is_light else "font-size: 15px; font-weight: 800; color: #a855f7;")
        sub = QLabel("Pop tumanidagi tashkilot va mahallalarda xodimlar o'zgarishi qaydnomasi")
        sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        head.addWidget(title)
        head.addWidget(sub)
        layout.addLayout(head)

        # Qidiruv va filtr
        filter_box = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Qidiruv (Mahalla, lavozim, ism-familiya)...")
        self.txt_search.textChanged.connect(self.filter_table)
        filter_box.addWidget(self.txt_search)

        btn_refresh = QPushButton("🔄 Yangilash")
        btn_refresh.clicked.connect(self.load_history)
        filter_box.addWidget(btn_refresh)
        layout.addLayout(filter_box)

        # Jadval
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Sana / Vaqt", "Mahalla / Tashkilot", "Lavozimi",
            "Oldingi Xodim", "Yangi Xodim", "Izoh / Sabab"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        layout.addWidget(self.table, 1)

        # Footer
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Jami yozuvlar: 0 ta")
        self.lbl_count.setStyleSheet(f"font-size: 12px; color: {'#475569' if is_light else '#94a3b8'}; font-weight: 600;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()
        self.btn_close = QPushButton("Yopish")
        self.btn_close.clicked.connect(self.accept)
        footer.addWidget(self.btn_close)
        layout.addLayout(footer)

    def load_history(self):
        """SQLite dan tarix yozuvlarini yuklash."""
        self.all_records = []
        if self.app and hasattr(self.app, "data_manager") and hasattr(self.app.data_manager, "sqlite"):
            try:
                self.all_records = self.app.data_manager.sqlite.get_staff_history(mahalla=self.mahalla)
            except Exception as e:
                logger.error(f"Tarixni olishda xatolik: {e}")

        self.display_records(self.all_records)

    def display_records(self, records):
        self.table.setUpdatesEnabled(False)
        try:
            self.table.setRowCount(len(records))
            for r_idx, row in enumerate(records):
                # row: dict yoki sqlite Row: created_at, mahalla, role, old_name, new_name, change_reason
                created_at = str(row.get("created_at") if isinstance(row, dict) else row["created_at"])
                mahalla = str(row.get("mahalla", "-") if isinstance(row, dict) else row["mahalla"])
                role = str(row.get("role", "-") if isinstance(row, dict) else row["role"])
                old_name = str(row.get("old_name", "-") if isinstance(row, dict) else row["old_name"])
                new_name = str(row.get("new_name", "-") if isinstance(row, dict) else row["new_name"])
                reason = str(row.get("change_reason", "") if isinstance(row, dict) else row["change_reason"])

                self.table.setItem(r_idx, 0, QTableWidgetItem(created_at[:19]))
                self.table.setItem(r_idx, 1, QTableWidgetItem(mahalla))
                self.table.setItem(r_idx, 2, QTableWidgetItem(role))
                self.table.setItem(r_idx, 3, QTableWidgetItem(old_name))
                self.table.setItem(r_idx, 4, QTableWidgetItem(new_name))
                self.table.setItem(r_idx, 5, QTableWidgetItem(reason))

            self.lbl_count.setText(f"Jami yozuvlar: {len(records)} ta")
        finally:
            self.table.setUpdatesEnabled(True)

    def filter_table(self, query: str):
        q = query.strip().lower()
        if not q:
            self.display_records(self.all_records)
            return

        filtered = []
        for r in self.all_records:
            m = str(r.get("mahalla", "") if isinstance(r, dict) else r["mahalla"]).lower()
            role = str(r.get("role", "") if isinstance(r, dict) else r["role"]).lower()
            old_n = str(r.get("old_name", "") if isinstance(r, dict) else r["old_name"]).lower()
            new_n = str(r.get("new_name", "") if isinstance(r, dict) else r["new_name"]).lower()
            if q in m or q in role or q in old_n or q in new_n:
                filtered.append(r)

        self.display_records(filtered)

def open_staff_history_dialog(app: Any, org_id: Optional[str] = None, mahalla: Optional[str] = None) -> None:
    dlg = HistoryView(parent=app, app=app, org_id=org_id, mahalla=mahalla)
    dlg.exec_()
