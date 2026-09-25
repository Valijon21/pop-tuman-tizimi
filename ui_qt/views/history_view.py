"""
ui_qt.views.history_view: Kadrlar almashinuvi va rotatsiyasi tarixi dialogi (PyQt5).
Senior darajadagi Vizual Vaqt Chizig'i (Visual Timeline) va to'liq audit jadvali.
"""
from typing import Optional, Any, List, Dict
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QComboBox,
    QLineEdit, QMessageBox, QScrollArea, QWidget, QFrame,
    QStackedWidget, QButtonGroup
)
from PyQt5.QtCore import Qt
from ui_qt.styles import get_stylesheet
from ui_qt.components.smart_completer import attach_smart_completer
from core.logger import logger


class HistoryView(QDialog):
    """Kadrlar tarixi va rotatsiyasi dialog oynasi (Visual Timeline + Table)."""

    def __init__(self, parent=None, app=None, org_id: Optional[str] = None, mahalla: Optional[str] = None):
        super().__init__(parent)
        self.app = app
        self.org_id = org_id
        self.mahalla = mahalla
        self.current_theme = getattr(app, "current_theme", "dark")
        self.all_records: List[Dict[str, Any]] = []
        self.filtered_records: List[Dict[str, Any]] = []

        self.setWindowTitle("📜 Kadrlar Almashinuvi va Rotatsiyasi Tarixi (Timeline & Audit)")
        self.resize(850, 560)
        self.setMinimumSize(680, 420)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # 1. Header & Rejim Tanlash
        head = QHBoxLayout()
        
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        title = QLabel("📜 Kadrlar Almashinuvi Tarixi (Audit & Timeline)")
        title_color = "#7e22ce" if is_light else "#c084fc"
        title.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {title_color};")
        
        sub_text = f"«{self.mahalla}» bo'yicha mas'ul xodimlar almashinuvi" if self.mahalla else "Pop tumanidagi tashkilot va mahallalarda xodimlar o'zgarishi qaydnomasi"
        sub = QLabel(sub_text)
        sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        head.addLayout(title_box, 1)

        # Rejim tugmalari (Segmented switch)
        mode_box = QHBoxLayout()
        mode_box.setSpacing(4)
        
        self.btn_mode_timeline = QPushButton("🕒 Vaqt Chizig'i")
        self.btn_mode_timeline.setCheckable(True)
        self.btn_mode_timeline.setChecked(True)
        self.btn_mode_timeline.setProperty("class", "pill_btn")
        self.btn_mode_timeline.setCursor(Qt.PointingHandCursor)
        self.btn_mode_timeline.clicked.connect(lambda: self.switch_view(0))

        self.btn_mode_table = QPushButton("📑 Jadval")
        self.btn_mode_table.setCheckable(True)
        self.btn_mode_table.setProperty("class", "pill_btn")
        self.btn_mode_table.setCursor(Qt.PointingHandCursor)
        self.btn_mode_table.clicked.connect(lambda: self.switch_view(1))

        mode_group = QButtonGroup(self)
        mode_group.addButton(self.btn_mode_timeline)
        mode_group.addButton(self.btn_mode_table)

        mode_box.addWidget(self.btn_mode_timeline)
        mode_box.addWidget(self.btn_mode_table)
        head.addLayout(mode_box)

        layout.addLayout(head)

        # 2. Qidiruv va Filtr Paneli
        filter_box = QHBoxLayout()
        filter_box.setSpacing(8)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Qidiruv (Mahalla, tashkilot, lavozim yoki xodim ismi)...")
        if self.mahalla:
            self.txt_search.setText(self.mahalla)
        self.txt_search.textChanged.connect(self.filter_records)
        filter_box.addWidget(self.txt_search, 1)

        # Smart Completer
        self.completer = attach_smart_completer(
            self.txt_search,
            items=[],
            theme=self.current_theme,
            on_selected=lambda _: self.filter_records()
        )

        self.btn_refresh = QPushButton("🔄 Yangilash")
        self.btn_refresh.setProperty("class", "btn_primary")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_history)
        filter_box.addWidget(self.btn_refresh)

        layout.addLayout(filter_box)

        # 3. Stacked Widget (0: Timeline, 1: Table)
        self.stack = QStackedWidget()

        # 3A. TIMELINE VIEW
        self.timeline_scroll = QScrollArea()
        self.timeline_scroll.setWidgetResizable(True)
        self.timeline_scroll.setFrameShape(QFrame.NoFrame)
        self.timeline_scroll.setStyleSheet("background: transparent;")

        self.timeline_container = QWidget()
        self.timeline_layout = QVBoxLayout(self.timeline_container)
        self.timeline_layout.setSpacing(12)
        self.timeline_layout.setContentsMargins(8, 6, 8, 6)
        self.timeline_scroll.setWidget(self.timeline_container)
        self.stack.addWidget(self.timeline_scroll)

        # 3B. TABLE VIEW
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
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.stack.addWidget(self.table)

        layout.addWidget(self.stack, 1)

        # 4. Footer
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Jami yozuvlar: 0 ta")
        self.lbl_count.setStyleSheet(f"font-size: 12px; color: {'#475569' if is_light else '#94a3b8'}; font-weight: 700;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()

        self.btn_close = QPushButton("Yopish")
        self.btn_close.setProperty("class", "btn_secondary")
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.clicked.connect(self.accept)
        footer.addWidget(self.btn_close)

        layout.addLayout(footer)

    def switch_view(self, index: int):
        self.stack.setCurrentIndex(index)
        self.btn_mode_timeline.setChecked(index == 0)
        self.btn_mode_table.setChecked(index == 1)

    def load_history(self):
        """SQLite dan tarix yozuvlarini yuklash."""
        self.all_records = []
        if self.app and hasattr(self.app, "data_manager") and hasattr(self.app.data_manager, "sqlite"):
            try:
                self.all_records = self.app.data_manager.sqlite.get_staff_history(mahalla=self.mahalla)
            except Exception as e:
                logger.error(f"Tarixni olishda xatolik: {e}")

        if hasattr(self, "completer"):
            suggest_items = set()
            for r in self.all_records:
                m = r.get("mahalla") or r.get("mahalla_nomi")
                old = r.get("old_name") or r.get("old_fio") or r.get("eski_xodim")
                new = r.get("new_name") or r.get("new_fio") or r.get("yangi_xodim") or r.get("full_name")
                role = r.get("role") or r.get("lavozim")
                if m: suggest_items.add(str(m))
                if old: suggest_items.add(str(old))
                if new: suggest_items.add(str(new))
                if role: suggest_items.add(str(role))
            self.completer.update_items(list(suggest_items))

        self.filter_records()

    def filter_records(self):
        query = self.txt_search.text().strip().lower()
        if not query:
            self.filtered_records = list(self.all_records)
        else:
            self.filtered_records = []
            for r in self.all_records:
                m = str(r.get("mahalla") or r.get("mahalla_nomi") or "").lower()
                role = str(r.get("role") or r.get("lavozim") or "").lower()
                old_n = str(r.get("old_name") or r.get("old_fio") or r.get("eski_xodim") or "").lower()
                new_n = str(r.get("new_name") or r.get("new_fio") or r.get("yangi_xodim") or r.get("full_name") or "").lower()
                if query in m or query in role or query in old_n or query in new_n:
                    self.filtered_records.append(r)

        self.render_timeline(self.filtered_records)
        self.render_table(self.filtered_records)
        self.lbl_count.setText(f"Jami yozuvlar: {len(self.filtered_records)} ta")

    def render_timeline(self, records):
        """Vizual vaqt chizig'ini (Timeline cards) generatsiya qilish."""
        # Eski kartalarni tozalash
        while self.timeline_layout.count():
            item = self.timeline_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        is_light = (self.current_theme == "light")

        if not records:
            empty_box = QFrame()
            empty_box.setStyleSheet("background: transparent; padding: 40px;")
            e_lay = QVBoxLayout(empty_box)
            lbl_empty = QLabel("📜 Kadrlar almashinuvi yozuvlari topilmadi")
            lbl_empty.setAlignment(Qt.AlignCenter)
            lbl_empty.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {'#94a3b8' if is_light else '#64748b'};")
            lbl_sub = QLabel("Xodimlar ma'lumotlari tahrirlanganda o'zgarishlar bu yerda xronologik qayd etiladi.")
            lbl_sub.setAlignment(Qt.AlignCenter)
            lbl_sub.setStyleSheet("font-size: 11px; color: #94a3b8;")
            e_lay.addWidget(lbl_empty)
            e_lay.addWidget(lbl_sub)
            self.timeline_layout.addWidget(empty_box)
            return

        for row in records:
            created_at = str(row.get("created_at") if isinstance(row, dict) else row["created_at"])[:19]
            mahalla = str(row.get("mahalla", "-") if isinstance(row, dict) else row["mahalla"])
            role = str(row.get("role", "-") if isinstance(row, dict) else row["role"])
            old_name = str(row.get("old_name", "-") if isinstance(row, dict) else row["old_name"])
            new_name = str(row.get("new_name", "-") if isinstance(row, dict) else row["new_name"])
            old_phone = str(row.get("old_phone", "") if isinstance(row, dict) else row.get("old_phone", ""))
            new_phone = str(row.get("new_phone", "") if isinstance(row, dict) else row.get("new_phone", ""))
            reason = str(row.get("change_reason", "") if isinstance(row, dict) else row["change_reason"])
            changed_by = str(row.get("changed_by", "ADMIN") if isinstance(row, dict) else row.get("changed_by", "ADMIN"))

            card = QFrame()
            card_bg = "#ffffff" if is_light else "#1e293b"
            card_border = "#e2e8f0" if is_light else "#334155"
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {card_bg};
                    border: 1px solid {card_border};
                    border-left: 4px solid #a855f7;
                    border-radius: 8px;
                    padding: 8px 12px;
                }}
            """)

            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(6)

            # 1. Sarlavha qatori: Tashkilot, Lavozim va Sana
            top_line = QHBoxLayout()
            lbl_org = QLabel(f"🏛 {mahalla}")
            lbl_org.setStyleSheet(f"font-size: 13px; font-weight: 800; color: {'#0f172a' if is_light else '#f8fafc'};")
            
            lbl_role = QLabel(f"• {role}")
            lbl_role.setStyleSheet("font-size: 12px; font-weight: 700; color: #a855f7;")

            lbl_date = QLabel(f"🕒 {created_at}")
            lbl_date.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")

            top_line.addWidget(lbl_org)
            top_line.addWidget(lbl_role)
            top_line.addStretch()
            top_line.addWidget(lbl_date)
            c_layout.addLayout(top_line)

            # 2. Xodimlar almashinuvi diff qatori
            diff_box = QHBoxLayout()
            diff_box.setSpacing(12)

            # Oldingi
            old_str = f"{old_name}" + (f" ({old_phone})" if old_phone else "")
            lbl_old = QLabel(f"🔴 <b>Oldingi:</b> {old_str}")
            lbl_old.setStyleSheet("font-size: 12px; color: #ef4444; background: #fee2e2; border-radius: 4px; padding: 3px 8px;" if is_light else "font-size: 12px; color: #fca5a5; background: #450a0a; border-radius: 4px; padding: 3px 8px;")

            # Strelka
            lbl_arrow = QLabel("➔")
            lbl_arrow.setStyleSheet("font-size: 14px; font-weight: 800; color: #94a3b8;")

            # Yangi
            new_str = f"{new_name}" + (f" ({new_phone})" if new_phone else "")
            lbl_new = QLabel(f"🟢 <b>Yangi:</b> {new_str}")
            lbl_new.setStyleSheet("font-size: 12px; color: #15803d; background: #dcfce7; border-radius: 4px; padding: 3px 8px;" if is_light else "font-size: 12px; color: #86efac; background: #052e16; border-radius: 4px; padding: 3px 8px;")

            diff_box.addWidget(lbl_old)
            diff_box.addWidget(lbl_arrow)
            diff_box.addWidget(lbl_new)
            diff_box.addStretch()
            c_layout.addLayout(diff_box)

            # 3. Sabab va Audit tafsiloti
            meta_box = QHBoxLayout()
            meta_str = f"👤 Kiritdi: <b>{changed_by}</b>"
            if reason:
                meta_str += f" &bull; 📝 Izoh: <i>{reason}</i>"
            lbl_meta = QLabel(meta_str)
            lbl_meta.setStyleSheet(f"font-size: 10.5px; color: {'#64748b' if is_light else '#94a3b8'};")
            meta_box.addWidget(lbl_meta)
            c_layout.addLayout(meta_box)

            self.timeline_layout.addWidget(card)

        self.timeline_layout.addStretch()

    def render_table(self, records):
        """Kadrlar tarixi jadvalini to'ldirish."""
        self.table.setUpdatesEnabled(False)
        try:
            self.table.setRowCount(len(records))
            for r_idx, row in enumerate(records):
                created_at = str(row.get("created_at") if isinstance(row, dict) else row["created_at"])[:19]
                mahalla = str(row.get("mahalla", "-") if isinstance(row, dict) else row["mahalla"])
                role = str(row.get("role", "-") if isinstance(row, dict) else row["role"])
                old_name = str(row.get("old_name", "-") if isinstance(row, dict) else row["old_name"])
                new_name = str(row.get("new_name", "-") if isinstance(row, dict) else row["new_name"])
                reason = str(row.get("change_reason", "") if isinstance(row, dict) else row["change_reason"])

                self.table.setItem(r_idx, 0, QTableWidgetItem(created_at))
                self.table.setItem(r_idx, 1, QTableWidgetItem(mahalla))
                self.table.setItem(r_idx, 2, QTableWidgetItem(role))
                self.table.setItem(r_idx, 3, QTableWidgetItem(old_name))
                self.table.setItem(r_idx, 4, QTableWidgetItem(new_name))
                self.table.setItem(r_idx, 5, QTableWidgetItem(reason))
        finally:
            self.table.setUpdatesEnabled(True)


def open_staff_history_dialog(app: Any, org_id: Optional[str] = None, mahalla: Optional[str] = None) -> None:
    dlg = HistoryView(parent=app, app=app, org_id=org_id, mahalla=mahalla)
    dlg.exec_()
