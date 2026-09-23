"""
ui_qt.views.import_dialog: Excel va CSV fayllardan ommaviy import qilish dialogi (PyQt5).
Faylni tahlil qilish, oldindan ko'rish va ma'lumotlar bazasiga xavfsiz qo'shish.
"""
from typing import Optional, Any, List, Dict
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt
from services.excel_service import import_organizations_from_file
from ui_qt.styles import get_stylesheet
from core.logger import logger
from core.threading_utils import WorkerThread

class ImportDialog(QDialog):
    """Excel / CSV ommaviy import dialog oynasi."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_theme = getattr(app, "current_theme", "dark")
        self.imported_items: List[Dict[str, Any]] = []

        self.setWindowTitle("📥 Excel / CSV Ommaviy Import")
        self.resize(780, 480)
        self.setMinimumSize(620, 380)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header
        head = QVBoxLayout()
        head.setSpacing(2)
        title = QLabel("📥 Excel va CSV dan Ommaviy Import")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #059669;" if is_light else "font-size: 15px; font-weight: 800; color: #10b981;")
        sub = QLabel("Excel (.xlsx, .xls) yoki CSV faylini tanlang va tizimga integratsiya qiling")
        sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        head.addWidget(title)
        head.addWidget(sub)
        layout.addLayout(head)

        # Fayl tanlash paneli
        file_box = QHBoxLayout()
        self.lbl_file = QLabel("Fayl tanlanmagan")
        file_bg = "#ffffff" if is_light else "#1e293b"
        file_fg = "#0f172a" if is_light else "#f8fafc"
        file_border = "#cbd5e1" if is_light else "#334155"
        self.lbl_file.setStyleSheet(f"font-size: 11.5px; color: {file_fg}; background: {file_bg}; border: 1px solid {file_border}; padding: 5px 10px; border-radius: 6px;")
        file_box.addWidget(self.lbl_file, 1)

        btn_browse = QPushButton("📁 Faylni Tanlash...")
        btn_browse.setStyleSheet("""
            background: #2563eb; color: white; font-weight: 700; padding: 5px 12px; border-radius: 6px; font-size: 11.5px;
        """)
        btn_browse.clicked.connect(self.browse_file)
        file_box.addWidget(btn_browse)
        layout.addLayout(file_box)

        # Oldindan ko'rish jadvali
        self.lbl_preview = QLabel("Oldindan ko'rish (Import qilinadigan qatorlar):")
        self.lbl_preview.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {'#334155' if is_light else '#cbd5e1'};")
        layout.addWidget(self.lbl_preview)

        self.table_preview = QTableWidget()
        self.table_preview.setColumnCount(6)
        self.table_preview.setHorizontalHeaderLabels(["№", "Turi", "Tashkilot Nomi", "F.I.SH", "Telefon", "INN"])
        self.table_preview.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_preview.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_preview.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        layout.addWidget(self.table_preview, 1)

        # Footer
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Topilgan yozuvlar: 0 ta")
        self.lbl_count.setStyleSheet(f"font-size: 12px; color: {'#059669' if is_light else '#10b981'}; font-weight: 700;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()

        self.btn_import = QPushButton("✅ Bazaga Saqlash")
        self.btn_import.setEnabled(False)
        self.btn_import.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
            color: white; font-weight: 700; padding: 10px 20px; border-radius: 8px;
        """)
        self.btn_import.clicked.connect(self.commit_import)
        footer.addWidget(self.btn_import)

        self.btn_close = QPushButton("Yopish")
        self.btn_close.clicked.connect(self.reject)
        footer.addWidget(self.btn_close)

        layout.addLayout(footer)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excel yoki CSV faylni tanlang", "",
            "Jadvallar (*.xlsx *.xls *.csv);;Barcha fayllar (*.*)"
        )
        if not file_path:
            return

        self.lbl_file.setText(os.path.basename(file_path))
        self.lbl_count.setText("⏳ Fayl o'qilmoqda...")
        self.btn_choose.setEnabled(False)
        self.btn_import.setEnabled(False)

        def _read_file():
            return import_organizations_from_file(file_path)

        self._read_worker = WorkerThread(_read_file, parent=self)
        self._read_worker.result_ready.connect(self._on_file_loaded)
        self._read_worker.error_occurred.connect(self._on_file_read_error)
        self._read_worker.start()

    def _on_file_loaded(self, res):
        self.btn_choose.setEnabled(True)
        items, warnings = res
        self.imported_items = items
        self.lbl_count.setText(f"Topilgan yozuvlar: {len(items)} ta")
        self.btn_import.setEnabled(bool(items))

        # Jadvalni to'ldirish
        self.table_preview.setUpdatesEnabled(False)
        try:
            self.table_preview.setRowCount(len(items))
            for idx, it in enumerate(items):
                self.table_preview.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
                self.table_preview.setItem(idx, 1, QTableWidgetItem(str(it.get("s", "-"))))
                self.table_preview.setItem(idx, 2, QTableWidgetItem(str(it.get("m", "-"))))
                self.table_preview.setItem(idx, 3, QTableWidgetItem(str(it.get("f", "-"))))
                self.table_preview.setItem(idx, 4, QTableWidgetItem(str(it.get("t", "-"))))
                self.table_preview.setItem(idx, 5, QTableWidgetItem(str(it.get("inn", "-"))))
        finally:
            self.table_preview.setUpdatesEnabled(True)

    def _on_file_read_error(self, err_msg: str):
        self.btn_choose.setEnabled(True)
        self.btn_import.setEnabled(False)
        self.lbl_count.setText("❌ Faylni o'qishda xatolik yuz berdi")
        QMessageBox.critical(self, "Xatolik", f"Faylni o'qishda xatolik yuz berdi:\n{err_msg}")

    def commit_import(self):
        if not self.imported_items:
            return

        reply = QMessageBox.question(
            self, "Tasdiqlash",
            f"{len(self.imported_items)} ta yangi tashkilot bazaga qo'shilsinmi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        if self.app and hasattr(self.app, "data_manager"):
            existing_inns = {str(i.get("inn", "")).strip() for i in self.app.data if i.get("inn")}
            added = 0
            for item in self.imported_items:
                inn = str(item.get("inn", "")).strip()
                if inn and inn in existing_inns:
                    continue  # Dublikatlarni o'tkazib yuborish
                self.app.data_manager.data.append(item)
                added += 1

            self.app.data_manager.save_data()
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            elif hasattr(self.app, "filter_data"):
                self.app.filter_data()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(f"📥 {added} ta yangi tashkilot import qilindi!", "success")

            QMessageBox.information(self, "Bajarildi", f"{added} ta yangi yozuv muvaffaqiyatli bazaga qo'shildi!")
            self.accept()

def open_batch_import_dialog(app: Any) -> None:
    dlg = ImportDialog(parent=app, app=app)
    dlg.exec_()
