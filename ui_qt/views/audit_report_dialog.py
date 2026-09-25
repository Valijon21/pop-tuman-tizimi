"""
ui_qt.views.audit_report_dialog: Baza sifatini audit qilish va kamchiliklarni tahlil qilish dialogi (PyQt5).
Enterprise darajasidagi sifat ko'rsatkichlari (Health Index), kamchiliklar monitoringi va Excel eksport.
"""
from typing import Optional, Any, List, Dict
import os
import openpyxl
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QProgressBar, QFrame, QFileDialog, QMessageBox,
    QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from ui_qt.styles import get_stylesheet
from core.logger import logger


class AuditReportDialog(QDialog):
    """Baza ma'lumotlari sifatini audit qilish (Data Quality Auditor) dialog oynasi."""

    def __init__(self, parent=None, app=None, on_filter_defects=None):
        super().__init__(parent)
        self.app = app
        self.on_filter_defects = on_filter_defects
        self.current_theme = getattr(app, "current_theme", "dark")
        self.data: List[Dict[str, Any]] = getattr(app, "data", []) if app else []

        self.setWindowTitle("🛡️ Baza Sifat Audit Hisoboti (Data Quality Auditor)")
        self.resize(680, 520)
        self.setMinimumSize(560, 440)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.calculate_stats()
        self.setup_ui()

    def calculate_stats(self):
        """Baza kamchiliklari statistikasini hisoblash."""
        self.total = len(self.data)
        if self.total == 0:
            self.total = 1  # 0 ga bo'linishdan saqlash

        self.missing_inn = [x for x in self.data if not str(x.get("inn", "")).strip()]
        self.missing_phone = [x for x in self.data if not str(x.get("t", "")).strip()]
        self.missing_bux = [x for x in self.data if not str(x.get("bux_tel", "")).strip()]
        self.missing_fio = [x for x in self.data if not str(x.get("f", "")).strip()]

        # Kamida bitta kamchiligi borlar
        self.all_defective = [
            x for x in self.data
            if not str(x.get("inn", "")).strip()
            or not str(x.get("t", "")).strip()
            or not str(x.get("bux_tel", "")).strip()
            or not str(x.get("f", "")).strip()
        ]

        # Sifat ko'rsatkichi (Health Score, 100 balldan)
        inn_score = (1 - (len(self.missing_inn) / self.total)) * 30
        phone_score = (1 - (len(self.missing_phone) / self.total)) * 30
        bux_score = (1 - (len(self.missing_bux) / self.total)) * 20
        fio_score = (1 - (len(self.missing_fio) / self.total)) * 20
        self.health_score = max(0, min(100, int(round(inn_score + phone_score + bux_score + fio_score))))

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # 1. Header
        head = QVBoxLayout()
        head.setSpacing(2)
        title = QLabel("🛡️ Baza Sifat Audit Hisoboti (Data Quality Auditor)")
        title_color = "#0284c7" if is_light else "#38bdf8"
        title.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {title_color};")
        sub = QLabel(f"Pop tumanidagi {len(self.data)} ta tashkilot ma'lumotlari sifatini to'liq tekshirish natijasi")
        sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        head.addWidget(title)
        head.addWidget(sub)
        layout.addLayout(head)

        # 2. Asosiy Health Score banneri
        banner = QFrame()
        b_bg = "#f0fdf4" if self.health_score >= 80 else ("#fefce8" if self.health_score >= 60 else "#fef2f2")
        b_border = "#86efac" if self.health_score >= 80 else ("#fde047" if self.health_score >= 60 else "#fca5a5")
        if not is_light:
            b_bg = "#064e3b" if self.health_score >= 80 else ("#713f12" if self.health_score >= 60 else "#7f1d1d")
            b_border = "#059669" if self.health_score >= 80 else ("#ca8a04" if self.health_score >= 60 else "#dc2626")

        banner.setStyleSheet(f"background-color: {b_bg}; border: 1.5px solid {b_border}; border-radius: 10px; padding: 10px;")
        b_layout = QHBoxLayout(banner)

        # Score belgisi
        lbl_score_val = QLabel(f"{self.health_score}%")
        lbl_score_val.setStyleSheet("font-size: 32px; font-weight: 900; color: #10b981;" if self.health_score >= 80 else ("font-size: 32px; font-weight: 900; color: #eab308;" if self.health_score >= 60 else "font-size: 32px; font-weight: 900; color: #ef4444;"))
        b_layout.addWidget(lbl_score_val)

        score_desc_box = QVBoxLayout()
        score_desc_box.setSpacing(2)
        score_title = QLabel("Baza Salomatlik Indeksi (Data Health Index)")
        score_title.setStyleSheet("font-size: 13px; font-weight: 800; color: #0f172a;" if is_light else "font-size: 13px; font-weight: 800; color: #f8fafc;")
        
        status_text = "A'lo darajada — ma'lumotlar deyarli to'liq!" if self.health_score >= 90 else (
            "Yaxshi — ayrim kontakt va INN kamchiliklari mavjud" if self.health_score >= 75 else
            "Diqqat talab — ko'p tashkilotlarda muhim ma'lumotlar to'ldirilmagan!"
        )
        lbl_score_sub = QLabel(status_text)
        lbl_score_sub.setStyleSheet("font-size: 11px; color: #334155;" if is_light else "font-size: 11px; color: #cbd5e1;")
        score_desc_box.addWidget(score_title)
        score_desc_box.addWidget(lbl_score_sub)
        b_layout.addLayout(score_desc_box, 1)

        layout.addWidget(banner)

        # 3. Metrikalar paneli (Progress barlar)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        metrics_widget = QWidget()
        metrics_layout = QVBoxLayout(metrics_widget)
        metrics_layout.setSpacing(10)
        metrics_layout.setContentsMargins(0, 4, 0, 4)

        def add_metric_row(label_text, missing_count, icon="⚠️"):
            filled_count = len(self.data) - missing_count
            pct = int(round((filled_count / self.total) * 100))
            
            box = QFrame()
            box_bg = "#ffffff" if is_light else "#1e293b"
            box_border = "#e2e8f0" if is_light else "#334155"
            box.setStyleSheet(f"background-color: {box_bg}; border: 1px solid {box_border}; border-radius: 8px; padding: 8px;")
            
            r_layout = QVBoxLayout(box)
            r_layout.setSpacing(4)

            top_row = QHBoxLayout()
            lbl_title = QLabel(f"{icon} {label_text}")
            lbl_title.setStyleSheet("font-weight: 700; font-size: 12px; color: #0f172a;" if is_light else "font-weight: 700; font-size: 12px; color: #f8fafc;")
            
            lbl_cnt = QLabel(f"To'ldirilgan: {filled_count}/{len(self.data)} ({pct}%) | <b>Kamchilik: {missing_count} ta</b>")
            lbl_cnt.setStyleSheet("font-size: 11px; color: #64748b;" if is_light else "font-size: 11px; color: #94a3b8;")
            top_row.addWidget(lbl_title)
            top_row.addStretch()
            top_row.addWidget(lbl_cnt)
            r_layout.addLayout(top_row)

            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(pct)
            pbar.setTextVisible(False)
            pbar.setFixedHeight(8)
            pbar_color = "#10b981" if pct >= 90 else ("#f59e0b" if pct >= 70 else "#ef4444")
            pbar.setStyleSheet(f"QProgressBar {{ background-color: {'#e2e8f0' if is_light else '#0f172a'}; border-radius: 4px; }} QProgressBar::chunk {{ background-color: {pbar_color}; border-radius: 4px; }}")
            r_layout.addWidget(pbar)

            metrics_layout.addWidget(box)

        add_metric_row("INN (9 xonali identifikatsiya raqami)", len(self.missing_inn), "🆔")
        add_metric_row("Mas'ul / Rahbar Telefoni", len(self.missing_phone), "📞")
        add_metric_row("Buxgalter Telefoni", len(self.missing_bux), "💼")
        add_metric_row("Rahbar F.I.SH (Ism-familiya)", len(self.missing_fio), "👤")
        add_metric_row("Jami kamchilikka ega tashkilotlar", len(self.all_defective), "🚨")

        scroll.setWidget(metrics_widget)
        layout.addWidget(scroll, 1)

        # 4. Tugmalar paneli
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_filter = QPushButton("⚠️ Jadvalda Kamchiliklarni Ko'rish")
        self.btn_filter.setProperty("class", "btn_warning")
        self.btn_filter.setCursor(Qt.PointingHandCursor)
        self.btn_filter.clicked.connect(self.apply_filter_and_close)
        btn_layout.addWidget(self.btn_filter)

        self.btn_export = QPushButton("📊 Kamchiliklarni Excelga Saqlash")
        self.btn_export.setProperty("class", "btn_success")
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.clicked.connect(self.export_defects_to_excel)
        btn_layout.addWidget(self.btn_export)

        btn_layout.addStretch()

        self.btn_close = QPushButton("Yopish")
        self.btn_close.setProperty("class", "btn_secondary")
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)

    def apply_filter_and_close(self):
        """Kamchilikli tashkilotlarni asosiy jadvalda ko'rsatish va dialogni yopish."""
        if callable(self.on_filter_defects):
            self.on_filter_defects()
        self.accept()

    def export_defects_to_excel(self):
        """Barcha kamchilikli tashkilotlarni sabablari bilan Excel faylga saqlash."""
        if not self.all_defective:
            QMessageBox.information(self, "Ma'lumot", "Bazada hech qanday kamchilik topilmadi! Hammasi to'liq. 🎉")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Kamchiliklar audit hisobotini saqlash", "baza_kamchiliklar_auditi.xlsx", "Excel Files (*.xlsx)"
        )
        if not path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Kamchiliklar Auditi"

            headers = [
                "№", "Toifasi", "Tashkilot Nomi", "Rahbar F.I.SH",
                "Rahbar Telefoni", "Buxgalter Telefoni", "INN",
                "Aniqlangan Kamchiliklar"
            ]
            ws.append(headers)

            for idx, it in enumerate(self.all_defective, 1):
                defects = []
                if not str(it.get("inn", "")).strip():
                    defects.append("INN yo'q")
                if not str(it.get("t", "")).strip():
                    defects.append("Rahbar teli yo'q")
                if not str(it.get("bux_tel", "")).strip():
                    defects.append("Buxgalter teli yo'q")
                if not str(it.get("f", "")).strip():
                    defects.append("F.I.SH yo'q")

                row = [
                    idx,
                    str(it.get("s", "")),
                    str(it.get("m", "")),
                    str(it.get("f", "")),
                    str(it.get("t", "")),
                    str(it.get("bux_tel", "")),
                    str(it.get("inn", "")),
                    ", ".join(defects)
                ]
                ws.append(row)

            wb.save(path)
            if self.app and hasattr(self.app, "show_toast"):
                self.app.show_toast(f"Kamchiliklar hisoboti saqlandi: {os.path.basename(path)}! ✅", "success")
            QMessageBox.information(
                self, "Muvaffaqiyatli",
                f"Kamchiliklar audit hisoboti muvaffaqiyatli saqlandi!\nJami: {len(self.all_defective)} ta tashkilot.\n\nFayl: {path}"
            )
        except Exception as e:
            logger.error(f"[AUDIT EXCEL XATO] {e}")
            QMessageBox.critical(self, "Xatolik", f"Excel faylni saqlashda xatolik yuz berdi:\n{e}")


def open_audit_report_dialog(app: Any, on_filter_defects=None) -> None:
    dlg = AuditReportDialog(parent=app, app=app, on_filter_defects=on_filter_defects)
    dlg.exec_()
