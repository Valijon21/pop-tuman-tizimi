"""
ui_qt.views.contracts_view: Shartnoma va Ulanishlar Monitoringi Ekrani (PyQt5).
Pop tumanidagi 232 ta tashkilotning shartnoma ma'lumotlari, apparat shtati,
tizimga ulangan xodimlar litsenziyalari, Rahbar va Buxgalter kontaktlari.
Senior darajadagi High-DPI, Fluent dizayn, KPI kartochkalari va to'liq Dark/Light mavzu.
"""
from typing import Any, Optional, Dict, List
import pyperclip
import openpyxl
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QMenu, QMessageBox, QFileDialog, QFrame, QScrollArea, QShortcut,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QKeySequence
from ui_qt.views.cabinet_dialog import open_cabinet_dialog
from ui_qt.views.contract_add_dialog import ContractAddDialog
from ui_qt.views.qr_dialog import open_qr_dialog
from ui_qt.components.widgets import ClickableCard
from ui_qt.styles import hex_to_rgba
from core.logger import logger

class ContractsView(QWidget):
    """Shartnoma va Ulanishlar Monitoringi Sahifasi."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_theme: str = getattr(app, "current_theme", "dark")
        self.current_category: str = "Barchasi"
        self.contracts_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []

        # 250ms Debounce taymeri
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(10)

        # 1. HEADER (Sarlavha va Eksport)
        head_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        self.lbl_title = QLabel("📑 Shartnoma & Ulanishlar Monitoringi")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8;")
        self.lbl_subtitle = QLabel("Tashkilotlarning shartnoma holati, apparat shtati, ulangan litsenziyalar va buxgalter kontaktlari")
        self.lbl_subtitle.setStyleSheet("font-size: 11px; color: #94a3b8;")

        title_box.addWidget(self.lbl_title)
        title_box.addWidget(self.lbl_subtitle)
        head_layout.addLayout(title_box)
        head_layout.addStretch()

        self.btn_add = QPushButton("➕ Qo'shish")
        self.btn_add.setProperty("class", "btn_primary")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.clicked.connect(self.open_add_dialog)
        head_layout.addWidget(self.btn_add)

        self.btn_export = QPushButton("📊 Excelga Eksport")
        self.btn_export.setProperty("class", "btn_success")
        self.btn_export.setCursor(Qt.PointingHandCursor)
        self.btn_export.clicked.connect(self.export_to_excel)
        head_layout.addWidget(self.btn_export)

        main_layout.addLayout(head_layout)

        # 2. KPI KARTALARI PANELI (4 ta karta)
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(10)

        self.card_total = self._create_kpi_card("Jami Shartnomalar", "🏢", "0 ta", "Tuzilgan", ("#38bdf8", "#0284c7"))
        self.card_aparat = self._create_kpi_card("Apparat Shtati", "👥", "0 ta", "Shtat birligi", ("#34d399", "#059669"))
        self.card_ulangan = self._create_kpi_card("Ulangan Xodimlar", "🔗", "0 ta", "Litsenziyalar", ("#a78bfa", "#7c3aed"))
        self.card_bux = self._create_kpi_card("Buxgalter Aloqalari", "📞", "0 ta", "Aloqada", ("#fbbf24", "#d97706"))

        kpi_layout.addWidget(self.card_total)
        kpi_layout.addWidget(self.card_aparat)
        kpi_layout.addWidget(self.card_ulangan)
        kpi_layout.addWidget(self.card_bux)

        main_layout.addLayout(kpi_layout)

        # 3. QIDIRUV VA TOIFA FILTRI (TOOLBAR)
        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        self.edit_search = QLineEdit()
        self.edit_search.setPlaceholderText("🔍 Qidiruv (Nomi, INN, Buxgalter yoki Rahbar telefoni, Ctrl+F)...")
        self.edit_search.textChanged.connect(self.on_search_changed)
        self.edit_search.returnPressed.connect(self.filter_data)
        toolbar.addWidget(self.edit_search, 1)

        self.btn_clear = QPushButton("✖")
        self.btn_clear.setFixedSize(26, 26)
        self.btn_clear.clicked.connect(lambda: self.edit_search.clear())
        toolbar.addWidget(self.btn_clear)

        main_layout.addLayout(toolbar)

        # Kategoriya Pills (Skroll paneli bilan)
        cat_scroll = QScrollArea()
        cat_scroll.setWidgetResizable(True)
        cat_scroll.setFixedHeight(34)
        cat_scroll.setFrameShape(QFrame.NoFrame)
        cat_scroll.setStyleSheet("background: transparent;")

        cat_container = QWidget()
        self.cat_layout = QHBoxLayout(cat_container)
        self.cat_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_layout.setSpacing(6)

        self.pill_buttons: Dict[str, QPushButton] = {}
        categories = ["Barchasi", "Mahalla", "Maktab", "Bog'cha", "Ta'lim", "Tibbiyot", "Boshqa"]
        for cat in categories:
            btn = QPushButton(cat)
            btn.setProperty("class", "pill_btn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, c=cat: self.on_category_clicked(c))
            self.cat_layout.addWidget(btn)
            self.pill_buttons[cat] = btn

        self.cat_layout.addStretch()
        cat_scroll.setWidget(cat_container)
        main_layout.addWidget(cat_scroll)

        # 4. ASOSIY JADVAL (QTableWidget)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "№", "Tashkilot Nomi", "INN", "Toifasi",
            "Apparat", "Ulangan", "Rahbar Tel", "Buxgalter Tel"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.doubleClicked.connect(self.on_table_double_clicked)
        self.table.verticalHeader().setVisible(False)
        self.table.installEventFilter(self)

        # Klaviaturadan qidiruvga o'tish (Ctrl+F)
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self.focus_search)

        main_layout.addWidget(self.table, 1)

        # 5. FOOTER
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Jami: 0 ta tashkilot")
        self.lbl_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #94a3b8;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()
        self.lbl_hint = QLabel("💡 O'ng tugma orqali Buxgalter yoki Rahbar raqamini bir zumda nusxalashingiz mumkin")
        self.lbl_hint.setStyleSheet("font-size: 11px; color: #64748b;")
        footer.addWidget(self.lbl_hint)

        main_layout.addLayout(footer)

        self.update_styles()

    def _create_kpi_card(self, title: str, icon: str, value: str, sub: str, color_spec: Any) -> ClickableCard:
        """Senior-darajadagi muvozanatli 2x2 KPI statistika kartochkasi."""
        is_light = (self.current_theme == "light")
        if isinstance(color_spec, (tuple, list)):
            color = color_spec[1] if is_light else color_spec[0]
        else:
            color = color_spec

        card = ClickableCard(hover_color=color, theme=self.current_theme)
        card.setMinimumHeight(86)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        card.setObjectName("contract_kpi_card")
        card._kpi_meta = (title, icon, sub, color_spec)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(6)

        # 1. YUQORI QATOR: Toifa nomi (chapda) + Nozik ikonka nishoni (o'ngda)
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)

        t_col = "#64748b" if is_light else "#94a3b8"
        lbl_t = QLabel(title)
        lbl_t.setObjectName("card_t")
        lbl_t.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {t_col};")
        top.addWidget(lbl_t)

        top.addStretch()

        icon_bg = hex_to_rgba(color, 0.10 if is_light else 0.15)
        icon_border = hex_to_rgba(color, 0.20 if is_light else 0.30)
        icon_lbl = QLabel(icon)
        icon_lbl.setObjectName("card_icon")
        icon_lbl.setFixedSize(30, 30)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 14px; background: {icon_bg}; border: 1px solid {icon_border}; border-radius: 7px;")
        top.addWidget(icon_lbl)
        layout.addLayout(top)

        # 2. QUYI QATOR: Katta ko'rsatkich (chapda) + Izoh nishoni (o'ngda)
        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)

        lbl_v = QLabel(value)
        lbl_v.setObjectName("card_v")
        lbl_v.setStyleSheet(f"font-size: 26px; font-weight: 800; color: {color};")
        bottom.addWidget(lbl_v)

        bottom.addStretch()

        sub_bg = hex_to_rgba(color, 0.08 if is_light else 0.12)
        lbl_s = QLabel(sub)
        lbl_s.setObjectName("card_s")
        lbl_s.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {sub_bg}; border-radius: 4px; padding: 2px 7px;")
        bottom.addWidget(lbl_s, alignment=Qt.AlignBottom)
        layout.addLayout(bottom)

        return card

    def set_theme(self, theme: str):
        """Mavzuni Dark / Light rejimiga moslashtirish."""
        self.current_theme = theme
        self.update_styles()

    def update_styles(self):
        is_light = (self.current_theme == "light")

        # Clear button
        if is_light:
            self.btn_clear.setStyleSheet("background: #e2e8f0; color: #475569; font-weight: bold; border: 1px solid #cbd5e1; border-radius: 6px;")
            self.lbl_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0284c7;")
            self.lbl_subtitle.setStyleSheet("font-size: 11px; color: #64748b;")
            self.lbl_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
            self.lbl_hint.setStyleSheet("font-size: 11px; color: #64748b;")
        else:
            self.btn_clear.setStyleSheet("background: #334155; color: #cbd5e1; font-weight: bold; border: 1px solid #475569; border-radius: 6px;")
            self.lbl_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #38bdf8;")
            self.lbl_subtitle.setStyleSheet("font-size: 11px; color: #94a3b8;")
            self.lbl_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #94a3b8;")
            self.lbl_hint.setStyleSheet("font-size: 11px; color: #64748b;")

        # KPI Kartalari
        for card in (self.card_total, self.card_aparat, self.card_ulangan, self.card_bux):
            if hasattr(card, "set_theme"):
                card.set_theme(self.current_theme)
            if hasattr(card, "_kpi_meta"):
                title, icon, sub, color_spec = card._kpi_meta
                color = color_spec[1] if is_light else color_spec[0]
                t_col = "#64748b" if is_light else "#94a3b8"
                lbl_t = card.findChild(QLabel, "card_t")
                if lbl_t:
                    lbl_t.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {t_col};")
                lbl_v = card.findChild(QLabel, "card_v")
                if lbl_v:
                    lbl_v.setStyleSheet(f"font-size: 26px; font-weight: 800; color: {color};")
                icon_lbl = card.findChild(QLabel, "card_icon")
                if icon_lbl:
                    icon_bg = hex_to_rgba(color, 0.10 if is_light else 0.15)
                    icon_border = hex_to_rgba(color, 0.20 if is_light else 0.30)
                    icon_lbl.setStyleSheet(f"font-size: 14px; background: {icon_bg}; border: 1px solid {icon_border}; border-radius: 7px;")
                lbl_s = card.findChild(QLabel, "card_s")
                if lbl_s:
                    sub_bg = hex_to_rgba(color, 0.08 if is_light else 0.12)
                    lbl_s.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {sub_bg}; border-radius: 4px; padding: 2px 7px;")

        self.update_pill_selection(self.current_category)

    def update_pill_selection(self, selected_cat: str):
        self.current_category = selected_cat
        for cat, btn in self.pill_buttons.items():
            btn.setChecked(cat == selected_cat)

    def focus_search(self):
        """Ctrl+F bosilganda qidiruv maydoniga o'tish."""
        self.edit_search.setFocus()
        self.edit_search.selectAll()

    def on_search_changed(self):
        """250ms Debounce bilan qidiruv."""
        if hasattr(self, "search_timer"):
            self.search_timer.start(250)
        else:
            self.filter_data()

    def eventFilter(self, source, event):
        """Jadvalda klaviatura hodisalari: Enter (tahrir)."""
        if source == self.table and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.on_table_double_clicked()
                return True
        return super().eventFilter(source, event)

    def on_category_clicked(self, cat: str):
        self.update_pill_selection(cat)
        self.filter_data()

    def load_data(self):
        """Bazada mavjud bo'lgan shartnoma ma'lumotlarini yuklash."""
        if not self.app or not hasattr(self.app, "data"):
            return

        # Faqat shartnoma ma'lumoti bo'lgan (aparat_soni, ulangan_soni yoki bux_tel) tashkilotlarni saralash
        contracts = []
        seen_inns = set()

        for it in self.app.data:
            bux = it.get("bux_tel") or ""
            aparat = it.get("aparat_soni")
            ulangan = it.get("ulangan_soni")
            inn = str(it.get("inn", "")).strip()

            if (bux or aparat is not None or ulangan is not None) and inn not in seen_inns:
                seen_inns.add(inn)
                contracts.append(it)

        # Agar INN bo'yicha saralangan bo'lsa
        self.contracts_data = sorted(contracts, key=lambda x: str(x.get("m", "")))
        self.update_kpis()
        self.filter_data()

    def update_kpis(self):
        """KPI kartochkalaridagi umumiy sonlarni hisoblash."""
        total_contracts = len(self.contracts_data)
        total_aparat = sum((it.get("aparat_soni") or 0) for it in self.contracts_data)
        total_ulangan = sum((it.get("ulangan_soni") or 0) for it in self.contracts_data)
        total_bux = sum(1 for it in self.contracts_data if str(it.get("bux_tel", "")).strip())

        self.card_total.findChild(QLabel, "card_v").setText(f"{total_contracts} ta")
        self.card_aparat.findChild(QLabel, "card_v").setText(f"{total_aparat:,} ta".replace(",", " "))
        self.card_ulangan.findChild(QLabel, "card_v").setText(f"{total_ulangan:,} ta".replace(",", " "))
        self.card_bux.findChild(QLabel, "card_v").setText(f"{total_bux} ta")

    def filter_data(self):
        """Qidiruv va toifa bo'yicha ma'lumotlarni filtrlab jadvalga chiqarish."""
        query = self.edit_search.text().strip().lower()
        cat = self.current_category

        self.filtered_data = []
        for it in self.contracts_data:
            s_val = str(it.get("s", ""))
            m_val = str(it.get("m", "")).lower()
            inn_val = str(it.get("inn", "")).lower()
            bux_val = str(it.get("bux_tel", "")).lower()
            raxbar_val = str(it.get("t", "")).lower()
            f_val = str(it.get("f", "")).lower()

            # Toifa filtri
            if cat != "Barchasi":
                if cat == "Mahalla" and "mahalla" not in s_val.lower() and "mfy" not in m_val:
                    continue
                elif cat == "Maktab" and "maktab" not in s_val.lower() and "maktab" not in m_val:
                    continue
                elif cat == "Bog'cha" and "bog'cha" not in s_val.lower() and "mtt" not in m_val:
                    continue
                elif cat not in ("Mahalla", "Maktab", "Bog'cha") and cat.lower() not in s_val.lower():
                    continue

            # Qidiruv filtri
            if query:
                if (query not in m_val and query not in inn_val and 
                    query not in bux_val and query not in raxbar_val and 
                    query not in f_val):
                    continue

            self.filtered_data.append(it)

        self.render_table_rows()

    def on_table_double_clicked(self):
        """Jadvalda 2 marta bosilganda tahrirlash oynasini ochish."""
        row = self.table.currentRow()
        if 0 <= row < len(self.filtered_data):
            item = self.filtered_data[row]
            from ui_qt.views.org_edit_dialog import OrgEditDialog
            dlg = OrgEditDialog(parent=self, app=self.app, item=item)
            if dlg.exec_() == OrgEditDialog.Accepted:
                if hasattr(self.app, "refresh_all_views"):
                    self.app.refresh_all_views()
                self.load_data()

    def render_table_rows(self):
        """Jadval qatorlarini chizish (Yuqori unumdorlik: updatesEnabled(False) va blockSignals(True))."""
        self.table.setUpdatesEnabled(False)
        self.table.blockSignals(True)
        try:
            self.table.setRowCount(len(self.filtered_data))
            for r_idx, it in enumerate(self.filtered_data):
                # 0. №
                item_no = QTableWidgetItem(str(r_idx + 1))
                item_no.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 0, item_no)

                # 1. Tashkilot Nomi
                item_name = QTableWidgetItem(str(it.get("m", "-")))
                self.table.setItem(r_idx, 1, item_name)

                # 2. INN
                item_inn = QTableWidgetItem(str(it.get("inn", "-")))
                item_inn.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 2, item_inn)

                # 3. Toifasi
                item_cat = QTableWidgetItem(str(it.get("s", "-")))
                item_cat.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 3, item_cat)

                # 4. Apparat Soni
                aparat_val = it.get("aparat_soni")
                item_aparat = QTableWidgetItem(f"{aparat_val} ta" if aparat_val is not None else "-")
                item_aparat.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 4, item_aparat)

                # 5. Ulangan Soni
                ulangan_val = it.get("ulangan_soni")
                item_ulangan = QTableWidgetItem(f"{ulangan_val} ta" if ulangan_val is not None else "-")
                item_ulangan.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 5, item_ulangan)

                # 6. Rahbar Tel
                item_raxbar = QTableWidgetItem(str(it.get("t", "-")))
                item_raxbar.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 6, item_raxbar)

                # 7. Buxgalter Tel
                item_bux = QTableWidgetItem(str(it.get("bux_tel", "-")))
                item_bux.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 7, item_bux)

            self.lbl_count.setText(f"Ko'rsatilmoqda: {len(self.filtered_data)} ta tashkilot")
        finally:
            self.table.blockSignals(False)
            self.table.setUpdatesEnabled(True)

    def open_add_dialog(self):
        """Yangi shartnoma ma'lumotini qo'shish dialogi."""
        dlg = ContractAddDialog(parent=self, app=self.app)
        if dlg.exec_() == ContractAddDialog.Accepted:
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            self.load_data()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("Yangi shartnoma ma'lumoti muvaffaqiyatli qo'shildi! ✅", "success")

    def open_edit_dialog(self):
        """Tanlangan shartnoma ma'lumotini tahrirlash dialogi."""
        row = self.table.currentRow()
        if row < 0 or row >= len(self.filtered_data):
            QMessageBox.information(self, "Ma'lumot", "Tahrirlash uchun jadvaldan tashkilotni tanlang.")
            return
        item = self.filtered_data[row]
        dlg = ContractAddDialog(parent=self, app=self.app, item=item)
        if dlg.exec_() == ContractAddDialog.Accepted:
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            self.load_data()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("Shartnoma ma'lumoti yangilandi! ✅", "success")

    def show_context_menu(self, pos):
        """O'ng tugma kontekst menyusi."""
        row = self.table.currentRow()
        if row < 0 or row >= len(self.filtered_data):
            return

        item = self.filtered_data[row]
        menu = QMenu(self)

        # Tahrirlash va qo'shish amallari
        act_edit = menu.addAction("✏ Tahrirlash")
        act_edit.triggered.connect(self.open_edit_dialog)

        act_add = menu.addAction("➕ Yangi shartnoma qo'shish")
        act_add.triggered.connect(self.open_add_dialog)

        menu.addSeparator()

        bux_tel = str(item.get("bux_tel", "")).strip()
        raxbar_tel = str(item.get("t", "")).strip()
        inn = str(item.get("inn", "")).strip()

        act_bux = menu.addAction(f"📞 Buxgalter telefonini nusxalash ({bux_tel or 'mavjud emas'})")
        act_bux.setEnabled(bool(bux_tel))
        act_bux.triggered.connect(lambda: self._copy_and_toast(bux_tel, "Buxgalter telefoni nusxalandi!"))

        act_raxbar = menu.addAction(f"📞 Rahbar telefonini nusxalash ({raxbar_tel or 'mavjud emas'})")
        act_raxbar.setEnabled(bool(raxbar_tel))
        act_raxbar.triggered.connect(lambda: self._copy_and_toast(raxbar_tel, "Rahbar telefoni nusxalandi!"))

        act_inn = menu.addAction(f"🆔 INN nusxalash ({inn})")
        act_inn.setEnabled(bool(inn))
        act_inn.triggered.connect(lambda: self._copy_and_toast(inn, "INN nusxalandi!"))

        menu.addSeparator()

        act_qr_raxbar = menu.addAction("📱 Rahbar QR Kodi (Kontakt)")
        act_qr_raxbar.setEnabled(bool(raxbar_tel))
        act_qr_raxbar.triggered.connect(lambda: open_qr_dialog(
            self.app,
            item=item,
            phone=raxbar_tel,
            org_name=str(item.get("m", "")),
            person_name=str(item.get("f", "")),
            role="Rahbar",
            inn=inn
        ))

        act_qr_bux = menu.addAction("📱 Buxgalter QR Kodi (Kontakt)")
        act_qr_bux.setEnabled(bool(bux_tel))
        act_qr_bux.triggered.connect(lambda: open_qr_dialog(
            self.app,
            item=item,
            phone=bux_tel,
            org_name=str(item.get("m", "")),
            person_name="Buxgalter",
            role="Buxgalter",
            inn=inn
        ))

        menu.addSeparator()

        act_cabinet = menu.addAction("🔑 Kabinetga dostup")
        act_cabinet.triggered.connect(lambda: open_cabinet_dialog(self.app, item))

        act_copy_row = menu.addAction("📋 Butun qatorni nusxalash")
        act_copy_row.triggered.connect(lambda: self._copy_entire_row(item))

        menu.exec_(self.table.viewport().mapToGlobal(pos))

    def _copy_and_toast(self, text: str, msg: str):
        if text:
            pyperclip.copy(text)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(msg, "success")

    def _copy_entire_row(self, item: Dict[str, Any]):
        row_str = f"{item.get('m', '')}\t{item.get('inn', '')}\t{item.get('s', '')}\tApparat: {item.get('aparat_soni', '')}\tUlangan: {item.get('ulangan_soni', '')}\tRahbar: {item.get('t', '')}\tBuxgalter: {item.get('bux_tel', '')}"
        pyperclip.copy(row_str)
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Qator to'liq nusxalandi! 📋", "success")

    def export_to_excel(self):
        """Shartnoma ma'lumotlarini Excelga eksport qilish."""
        if not self.filtered_data:
            QMessageBox.warning(self, "Ogohlantirish", "Eksport qilish uchun jadvalda ma'lumot yo'q.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Shartnomalar hisobotini saqlash", "shartnomalar_va_ulanishlar.xlsx", "Excel Files (*.xlsx)"
        )
        if not path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Shartnomalar"

            headers = [
                "№", "Tashkilot Nomi", "INN", "Toifasi",
                "Apparat Soni", "Ulangan Soni (Shartnomada)",
                "Rahbar Telefoni", "Buxgalter Telefoni"
            ]
            ws.append(headers)

            for idx, it in enumerate(self.filtered_data, 1):
                ws.append([
                    idx,
                    str(it.get("m", "")),
                    str(it.get("inn", "")),
                    str(it.get("s", "")),
                    it.get("aparat_soni") or "",
                    it.get("ulangan_soni") or "",
                    str(it.get("t", "")),
                    str(it.get("bux_tel", ""))
                ])

            wb.save(path)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(f"📊 {len(self.filtered_data)} ta shartnoma Excelga saqlandi!", "success")
            QMessageBox.information(self, "Muvaffaqiyatli", f"{len(self.filtered_data)} ta tashkilot shartnomalari Excelga saqlandi!")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Excel saqlashda xatolik: {e}")
