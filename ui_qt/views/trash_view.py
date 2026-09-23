"""
ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5).
O'chirilgan yozuvlarni ko'rish, bazaga qayta tiklash yoki butunlay o'chirish.
"""
from typing import Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class TrashView(QWidget):
    """Chiqindi qutisi ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.load_trash()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Header
        head = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        self.title_lbl = QLabel("🗑 Chiqindi Qutisi")
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #ef4444;")
        self.sub_lbl = QLabel("Bu yerdan o'chirilgan tashkilotlarni qayta tiklashingiz yoki butunlay o'chirishingiz mumkin")
        self.sub_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")
        title_box.addWidget(self.title_lbl)
        title_box.addWidget(self.sub_lbl)
        head.addLayout(title_box)

        head.addStretch()

        # Amallar
        self.btn_restore = QPushButton("♻ Qayta Tiklash")
        self.btn_restore.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            color: white; font-weight: 700; padding: 5px 12px; border-radius: 6px; font-size: 11.5px;
        """)
        self.btn_restore.clicked.connect(self.restore_selected)
        head.addWidget(self.btn_restore)

        self.btn_perm_delete = QPushButton("🗑 Butunlay O'chirish")
        self.btn_perm_delete.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #ef4444);
            color: white; font-weight: 700; padding: 5px 12px; border-radius: 6px; font-size: 11.5px;
        """)
        self.btn_perm_delete.clicked.connect(self.perm_delete_selected)
        head.addWidget(self.btn_perm_delete)

        layout.addLayout(head)

        # Jadval
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["№", "Turi", "Tashkilot Nomi", "Mas'ul F.I.SH", "Telefon", "INN"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        layout.addWidget(self.table, 1)

        # Footer
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Chiqindidagi yozuvlar: 0 ta")
        self.lbl_count.setStyleSheet("font-size: 13px; color: #94a3b8; font-weight: 600;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()
        self.btn_empty = QPushButton("🧹 Barcha Chiqindini Bo'shatish")
        self.btn_empty.setStyleSheet("background: #334155; color: #ef4444; font-weight: 700; padding: 8px 16px; border-radius: 8px;")
        self.btn_empty.clicked.connect(self.empty_trash)
        footer.addWidget(self.btn_empty)

        layout.addLayout(footer)

    def set_theme(self, theme: str):
        """Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish."""
        is_light = (theme == "light")
        self.sub_lbl.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        self.lbl_count.setStyleSheet(f"font-size: 13px; color: {'#475569' if is_light else '#94a3b8'}; font-weight: 600;")
        if is_light:
            self.btn_empty.setStyleSheet("background: #e2e8f0; color: #ef4444; font-weight: 700; padding: 8px 16px; border-radius: 8px;")
        else:
            self.btn_empty.setStyleSheet("background: #334155; color: #ef4444; font-weight: 700; padding: 8px 16px; border-radius: 8px;")

    def load_trash(self):
        """Chiqindi ro'yxatini yuklash."""
        trash = []
        if self.app and hasattr(self.app, "data_manager"):
            trash = getattr(self.app.data_manager, "trash", [])

        self.table.setUpdatesEnabled(False)
        try:
            self.table.setRowCount(len(trash))
            for idx, it in enumerate(trash):
                self.table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
                self.table.setItem(idx, 1, QTableWidgetItem(str(it.get("s", "-"))))
                self.table.setItem(idx, 2, QTableWidgetItem(str(it.get("m", "-"))))
                self.table.setItem(idx, 3, QTableWidgetItem(str(it.get("f", "-"))))
                self.table.setItem(idx, 4, QTableWidgetItem(str(it.get("t", "-"))))
                self.table.setItem(idx, 5, QTableWidgetItem(str(it.get("inn", "-"))))

            self.lbl_count.setText(f"Chiqindidagi yozuvlar soni: {len(trash)} ta")
        finally:
            self.table.setUpdatesEnabled(True)

    def restore_selected(self):
        selected_rows = sorted(set(idx.row() for idx in self.table.selectedIndexes()), reverse=True)
        if not selected_rows:
            QMessageBox.information(self, "Ma'lumot", "Qayta tiklash uchun jadvaldan qator tanlang.")
            return

        trash = self.app.data_manager.trash
        restored = 0
        for r in selected_rows:
            if 0 <= r < len(trash):
                item = trash[r]
                self.app.data_manager.restore_from_trash(item)
                restored += 1

        self.load_trash()
        if hasattr(self.app, "filter_data"):
            self.app.filter_data()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"♻ {restored} ta tashkilot bazaga tiklandi!", "success")

    def perm_delete_selected(self):
        selected_rows = sorted(set(idx.row() for idx in self.table.selectedIndexes()), reverse=True)
        if not selected_rows:
            QMessageBox.information(self, "Ma'lumot", "O'chirish uchun jadvaldan qator tanlang.")
            return

        reply = QMessageBox.question(
            self, "Tasdiqlash",
            f"{len(selected_rows)} ta yozuvni butunlay o'chirmoqchimisiz? Bu amalni qaytarib bo'lmaydi!",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        trash = self.app.data_manager.trash
        for r in selected_rows:
            if 0 <= r < len(trash):
                item = trash[r]
                self.app.data_manager.permanent_delete(item)

        self.load_trash()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Yozuv butunlay o'chirildi.", "warning")

    def empty_trash(self):
        trash = self.app.data_manager.trash
        if not trash:
            return

        reply = QMessageBox.question(
            self, "DIQQAT!",
            "Chiqindi qutisidagi BARCHA ma'lumotlar butunlay o'chirilsinmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        while trash:
            self.app.data_manager.permanent_delete(trash[0])

        self.load_trash()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Chiqindi qutisi to'liq tozalandi.", "warning")

def render_trash(parent: Any, app: Any):
    view = TrashView(parent=parent, app=app)
    return view
