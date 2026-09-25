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
from core.logger import logger

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
        self.btn_restore.setProperty("class", "btn_success")
        self.btn_restore.setCursor(Qt.PointingHandCursor)
        self.btn_restore.clicked.connect(self.restore_selected)
        head.addWidget(self.btn_restore)

        self.btn_perm_delete = QPushButton("🗑 Butunlay O'chirish")
        self.btn_perm_delete.setProperty("class", "btn_danger")
        self.btn_perm_delete.setCursor(Qt.PointingHandCursor)
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
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table, 1)

        # Footer
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Chiqindidagi yozuvlar: 0 ta")
        self.lbl_count.setStyleSheet("font-size: 12px; color: #94a3b8; font-weight: 600;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()
        self.btn_empty = QPushButton("🧹 Barcha Chiqindini Bo'shatish")
        self.btn_empty.setProperty("class", "btn_secondary")
        self.btn_empty.setCursor(Qt.PointingHandCursor)
        self.btn_empty.setStyleSheet("color: #ef4444; font-weight: 700; padding: 6px 14px;")
        self.btn_empty.clicked.connect(self.empty_trash)
        footer.addWidget(self.btn_empty)

        layout.addLayout(footer)

    def set_theme(self, theme: str):
        """Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish."""
        is_light = (theme == "light")
        self.title_lbl.setStyleSheet(f"font-size: 15px; font-weight: 800; color: {'#dc2626' if is_light else '#ef4444'};")
        self.sub_lbl.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        self.lbl_count.setStyleSheet(f"font-size: 12px; color: {'#475569' if is_light else '#94a3b8'}; font-weight: 700;")

    def load_trash(self):
        """Chiqindi ro'yxatini yuklash (Yuqori unumdorlik: updatesEnabled(False) va blockSignals(True))."""
        trash = []
        if self.app and hasattr(self.app, "data_manager"):
            trash = getattr(self.app.data_manager, "trash", [])

        self.table.setUpdatesEnabled(False)
        self.table.blockSignals(True)
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
            self.table.blockSignals(False)
            self.table.setUpdatesEnabled(True)

    def restore_selected(self):
        """Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash."""
        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self):
                return

        selected_rows = sorted(set(idx.row() for idx in self.table.selectedIndexes()), reverse=True)
        if not selected_rows:
            QMessageBox.information(self, "Ma'lumot", "Qayta tiklash uchun jadvaldan qator tanlang.")
            return

        trash = self.app.data_manager.trash
        restored = 0
        for r in selected_rows:
            if 0 <= r < len(trash):
                item = trash.pop(r)
                if "deleted_at" in item:
                    del item["deleted_at"]
                self.app.data_manager.data.append(item)
                tid = item.get("id")
                if tid:
                    try:
                        self.app.data_manager.sqlite.delete_trash_item(str(tid))
                    except Exception as e:
                        logger.error(f"[SQLITE XATO] delete_trash_item: {e}")
                restored += 1

        self.app.data_manager.save_data()
        self.app.data_manager.save_trash()
        self.load_trash()
        if hasattr(self.app, "refresh_all_views"):
            self.app.refresh_all_views()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"♻ {restored} ta tashkilot bazaga tiklandi!", "success")

    def perm_delete_selected(self):
        """Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish."""
        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self):
                return

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
        deleted_count = 0
        for r in selected_rows:
            if 0 <= r < len(trash):
                item = trash.pop(r)
                tid = item.get("id")
                if tid:
                    try:
                        self.app.data_manager.sqlite.delete_trash_item(str(tid))
                    except Exception as e:
                        logger.error(f"[SQLITE XATO] delete_trash_item: {e}")
                deleted_count += 1

        self.app.data_manager.save_trash()
        self.load_trash()
        if hasattr(self.app, "refresh_all_views"):
            self.app.refresh_all_views()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"🗑 {deleted_count} ta yozuv butunlay o'chirildi.", "warning")

    def empty_trash(self):
        """Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLite)."""
        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self):
                return

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

        for it in list(trash):
            tid = it.get("id")
            if tid:
                try:
                    self.app.data_manager.sqlite.delete_trash_item(str(tid))
                except Exception as e:
                    logger.error(f"[SQLITE XATO] delete_trash_item: {e}")
        trash.clear()
        self.app.data_manager.save_trash()

        self.load_trash()
        if hasattr(self.app, "refresh_all_views"):
            self.app.refresh_all_views()
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Chiqindi qutisi to'liq tozalandi.", "warning")

def render_trash(parent: Any, app: Any):
    view = TrashView(parent=parent, app=app)
    return view
