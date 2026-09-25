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
from PyQt5.QtGui import QKeySequence, QColor
from ui_qt.views.cabinet_dialog import open_cabinet_dialog
from ui_qt.views.contract_add_dialog import ContractAddDialog
from ui_qt.views.qr_dialog import open_qr_dialog
from ui_qt.components.widgets import ClickableCard
from ui_qt.components.smart_completer import attach_smart_completer
from services.search_service import normalize_text, smart_match_tokens
from ui_qt.styles import hex_to_rgba
from core.logger import logger


class NumericTableWidgetItem(QTableWidgetItem):
    """Sonlar, INN va litsenziya ko'rsatkichlarini to'g'ri raqamli tartiblash (sorting) uchun QTableWidgetItem."""

    def __init__(self, text: str, sort_value: Any = None):
        super().__init__(text)
        self.sort_value = sort_value if sort_value is not None else text

    def __lt__(self, other):
        if isinstance(other, NumericTableWidgetItem):
            try:
                return float(self.sort_value) < float(other.sort_value)
            except (ValueError, TypeError):
                return str(self.sort_value).lower() < str(other.sort_value).lower()
        return super().__lt__(other)


class ContractsView(QWidget):
    """Shartnoma va Ulanishlar Monitoringi Sahifasi."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_theme: str = getattr(app, "current_theme", "dark")
        self.current_category: str = "Barchasi"
        self.contracts_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []
        self.BASE_COLUMNS = ["№", "Tashkilot Nomi", "INN", "Toifasi", "Apparat SHT", "Ulangan", "Rahbar Tel", "Buxgalter Tel"]
        self.custom_columns: List[Dict[str, Any]] = self._load_custom_columns()

        # 250ms Debounce taymeri
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data)

        self.setup_ui()
        self.load_data()

    def _load_custom_columns(self) -> List[Dict[str, Any]]:
        if self.app and hasattr(self.app, "data_manager"):
            return self.app.data_manager.settings.get("contracts_custom_columns", [])
        return []

    def setup_table_columns(self):
        """Jadval ustunlari va sarlavhalarini baza + maxsus ustunlar bilan sozlash."""
        headers = list(self.BASE_COLUMNS)
        for c in self.custom_columns:
            headers.append(str(c.get("name", "Ustun")))

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)

        for idx in range(8, len(headers)):
            header.setSectionResizeMode(idx, QHeaderView.Interactive)
            w = self.custom_columns[idx - 8].get("width", 150)
            self.table.setColumnWidth(idx, w)

        header.setSortIndicatorShown(True)
        self.table.setSortingEnabled(True)
        try:
            header.sectionClicked.disconnect(self._on_section_sorted)
        except Exception:
            pass
        header.sectionClicked.connect(self._on_section_sorted)

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        try:
            self.table.customContextMenuRequested.disconnect(self.show_context_menu)
            self.table.doubleClicked.disconnect(self.on_table_double_clicked)
        except Exception:
            pass
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.doubleClicked.connect(self.on_table_double_clicked)
        self.table.verticalHeader().setVisible(False)
        self.table.installEventFilter(self)

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

        self.btn_columns = QPushButton("⚙ Ustunlar")
        self.btn_columns.setProperty("class", "btn_secondary")
        self.btn_columns.setCursor(Qt.PointingHandCursor)
        self.btn_columns.clicked.connect(self.open_column_manager)
        head_layout.addWidget(self.btn_columns)

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

        # Aqlli Auto-complete (Takliflar) tizimini ulash
        self.completer = attach_smart_completer(
            self.edit_search,
            items=[],
            theme=self.current_theme,
            on_selected=lambda _: self.filter_data()
        )

        self.btn_clear = QPushButton("✖")
        self.btn_clear.setFixedSize(26, 26)
        self.btn_clear.clicked.connect(lambda: self.edit_search.clear())
        toolbar.addWidget(self.btn_clear)

        main_layout.addLayout(toolbar)

        # Kategoriya Pills (Skroll paneli bilan)
        self.cat_scroll = QScrollArea()
        self.cat_scroll.setWidgetResizable(True)
        self.cat_scroll.setFixedHeight(34)
        self.cat_scroll.setFrameShape(QFrame.NoFrame)
        self.cat_scroll.setStyleSheet("background: transparent;")

        self.cat_container = QWidget()
        self.cat_layout = QHBoxLayout(self.cat_container)
        self.cat_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_layout.setSpacing(6)

        self.pill_buttons: Dict[str, QPushButton] = {}
        self.setup_category_pills()

        self.cat_scroll.setWidget(self.cat_container)
        main_layout.addWidget(self.cat_scroll)

        # 4. ASOSIY JADVAL (QTableWidget - Tartiblangan, dinamik ustunlar bilan)
        self.table = QTableWidget()
        self.setup_table_columns()

        # Klaviaturadan qidiruvga o'tish (Ctrl+F) va Tashkilot qo'shish (Ctrl+N)
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self.focus_search)

        self.shortcut_add = QShortcut(QKeySequence("Ctrl+N"), self)
        self.shortcut_add.activated.connect(self.open_add_dialog)

        main_layout.addWidget(self.table, 1)

        # 5. FOOTER
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Jami: 0 ta tashkilot")
        self.lbl_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #94a3b8;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()
        self.lbl_hint = QLabel("💡 Ustun sarlavhasini bosib saralang | Ctrl+C bilan nusxalang | O'ng tugma amallari")
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

        if hasattr(self, "completer"):
            self.completer.set_theme(self.current_theme)

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

    def _on_section_sorted(self, logical_index: int):
        """Ustun bosib saralangandan so'ng № ustunini 1, 2, 3... qilib qayta raqamlash."""
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        try:
            for r in range(self.table.rowCount()):
                no_item = self.table.item(r, 0)
                if no_item:
                    no_item.setText(str(r + 1))
        finally:
            self.table.setSortingEnabled(True)
            self.table.blockSignals(False)

    def copy_selected_cells(self):
        """Tanlangan kataklarni Excel kabi Tab va Yangi qator bilan clipboardga nusxalash."""
        selected_indexes = self.table.selectedIndexes()
        if not selected_indexes:
            return

        rows = sorted(list(set(idx.row() for idx in selected_indexes)))
        cols = sorted(list(set(idx.column() for idx in selected_indexes)))

        text_rows = []
        for r in rows:
            row_vals = []
            for c in cols:
                item = self.table.item(r, c)
                row_vals.append(item.text() if item else "")
            text_rows.append("\t".join(row_vals))

        copied_text = "\n".join(text_rows)
        pyperclip.copy(copied_text)
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"📋 {len(selected_indexes)} ta katak nusxalandi!", "success")

    def eventFilter(self, source, event):
        """Jadvalda klaviatura hodisalari: Enter (tahrir), Ctrl+C (nusxalash)."""
        if source == self.table and event.type() == QEvent.KeyPress:
            if event.matches(QKeySequence.Copy) or (event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_C):
                self.copy_selected_cells()
                return True
            elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.on_table_double_clicked()
                return True
        return super().eventFilter(source, event)

    def setup_category_pills(self):
        """Kategoriya tugmalarini va qo'shish tugmalarini dinamik barpo etish."""
        # Eski elementlarni tozalash
        while self.cat_layout.count():
            item = self.cat_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.pill_buttons = {}

        # Asosiy toifalar ro'yxati
        base_cats = ["Barchasi", "Mahalla", "Maktab", "Bog'cha", "Ta'lim", "Tibbiyot"]
        extra_cats = []
        if self.app and hasattr(self.app, "data_manager") and hasattr(self.app.data_manager, "categories"):
            for c in self.app.data_manager.categories:
                c_clean = str(c).strip()
                if not c_clean:
                    continue
                if not any(b.lower() in c_clean.lower() for b in base_cats) and c_clean.lower() != "boshqa":
                    if c_clean not in extra_cats:
                        extra_cats.append(c_clean)

        categories = base_cats + extra_cats + ["Boshqa"]

        for cat in categories:
            btn = QPushButton(cat)
            btn.setProperty("class", "pill_btn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, c=cat: self.on_category_clicked(c))
            self.cat_layout.addWidget(btn)
            self.pill_buttons[cat] = btn

        # ── 1. "➕ Tashkilot qo'shish" tugmasi (Aynan toifalar qatorida) ──
        self.btn_pill_add = QPushButton("➕ Tashkilot qo'shish")
        self.btn_pill_add.setProperty("class", "pill_action_btn")
        self.btn_pill_add.setCursor(Qt.PointingHandCursor)
        self.btn_pill_add.setToolTip("Yangi tashkilot / shartnoma qo'shish (Ctrl+N)")
        self.btn_pill_add.clicked.connect(lambda: self.open_add_dialog())
        self.cat_layout.addWidget(self.btn_pill_add)

        # ── 2. "+ Toifa" qo'shish tugmasi ──
        self.btn_pill_add_cat = QPushButton("+ Toifa")
        self.btn_pill_add_cat.setProperty("class", "pill_add_cat_btn")
        self.btn_pill_add_cat.setCursor(Qt.PointingHandCursor)
        self.btn_pill_add_cat.setToolTip("Yangi tashkilot toifasini kiritish")
        self.btn_pill_add_cat.clicked.connect(self.open_add_category_dialog)
        self.cat_layout.addWidget(self.btn_pill_add_cat)

        self.cat_layout.addStretch()
        self.update_pill_selection(self.current_category)

    def open_add_category_dialog(self):
        """Yangi toifa qo'shish dialogi."""
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(
            self, "Yangi Toifa Qo'shish",
            "Yangi tashkilot toifasi nomini kiriting:\n(Masalan: Sport, Madaniyat, Bank)"
        )
        if ok and text.strip():
            new_cat = text.strip()
            if hasattr(self.app, "data_manager"):
                if self.app.data_manager.add_category(new_cat):
                    self.setup_category_pills()
                    if hasattr(self.app, "refresh_all_views"):
                        self.app.refresh_all_views()
                    self.on_category_clicked(new_cat)
                    if hasattr(self.app, "show_toast"):
                        self.app.show_toast(f"'{new_cat}' toifasi muvaffaqiyatli qo'shildi! ✅", "success")
                else:
                    QMessageBox.information(self, "Ma'lumot", f"'{new_cat}' toifasi allaqachon mavjud.")

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

            if bux or aparat is not None or ulangan is not None:
                if inn:
                    if inn in seen_inns:
                        continue
                    seen_inns.add(inn)
                contracts.append(it)

        # Standart holatda tashkilot nomi bo'yicha saralash
        self.contracts_data = sorted(contracts, key=lambda x: str(x.get("m", "")).lower())
        self.update_kpis()

        # Auto-complete takliflar lug'atini yangilash
        if hasattr(self, "completer"):
            dict_items = []
            for it in self.contracts_data:
                m = str(it.get("m", "")).strip()
                inn = str(it.get("inn", "")).strip()
                bux = str(it.get("bux_tel", "")).strip()
                f = str(it.get("f", "")).strip()
                if m:
                    dict_items.append(m)
                if inn:
                    dict_items.append(f"{inn} — {m}" if m else inn)
                if bux:
                    dict_items.append(f"📞 {bux} ({m})")
                if f:
                    dict_items.append(f"{f} ({m})")
            self.completer.update_items(dict_items)

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
        query_raw = self.edit_search.text().strip()
        query_norm = normalize_text(query_raw)
        digits_query = "".join(filter(str.isdigit, query_raw))
        cat = self.current_category

        self.filtered_data = []
        for it in self.contracts_data:
            s_val = str(it.get("s", ""))
            m_norm = normalize_text(it.get("m", ""))
            inn_val = str(it.get("inn", "")).strip()
            bux_digits = "".join(filter(str.isdigit, str(it.get("bux_tel", ""))))
            raxbar_digits = "".join(filter(str.isdigit, str(it.get("t", ""))))
            f_norm = normalize_text(it.get("f", ""))

            # Toifa filtri
            if cat != "Barchasi":
                if cat == "Mahalla" and "mahalla" not in s_val.lower() and "mfy" not in m_norm:
                    continue
                elif cat == "Maktab" and "maktab" not in s_val.lower() and "maktab" not in m_norm:
                    continue
                elif cat == "Bog'cha" and "bog'cha" not in s_val.lower() and "mtt" not in m_norm:
                    continue
                elif cat not in ("Mahalla", "Maktab", "Bog'cha") and cat.lower() not in s_val.lower():
                    continue

            # Qidiruv filtri (Aqlli ko'p tokenli va lotin-kirill moslashuvchan)
            if query_norm:
                matched = (
                    smart_match_tokens(query_norm, m_norm) or
                    smart_match_tokens(query_norm, f_norm) or
                    (digits_query and digits_query in inn_val) or
                    (digits_query and digits_query in bux_digits) or
                    (digits_query and digits_query in raxbar_digits)
                )
                if not matched:
                    continue

            self.filtered_data.append(it)

        self.render_table_rows()

    def _get_item_by_row(self, row: int) -> Optional[Dict[str, Any]]:
        """Saralash (sorting) hisobga olingan holda jadval qatoridagi elementni aniqlash."""
        if row < 0 or row >= self.table.rowCount():
            return None
        inn_item = self.table.item(row, 2)
        target_inn = inn_item.text().strip() if inn_item else ""
        if target_inn:
            for it in self.filtered_data:
                if str(it.get("inn", "")).strip() == target_inn:
                    return it
        if 0 <= row < len(self.filtered_data):
            return self.filtered_data[row]
        return None

    def on_table_double_clicked(self):
        """Jadvalda 2 marta bosilganda tahrirlash oynasini ochish."""
        row = self.table.currentRow()
        col = self.table.currentColumn()
        item = self._get_item_by_row(row)
        if not item:
            return

        # Agar maxsus ustun bo'lsa (col >= 8), to'g'ridan-to'g'ri tezkor kiritish dialogi
        if col >= 8 and (col - 8) < len(self.custom_columns):
            c_info = self.custom_columns[col - 8]
            col_name = c_info.get("name", "Ustun")
            col_key = c_info.get("key", "")
            current_val = str(item.get(col_key) or "")
            from PyQt5.QtWidgets import QInputDialog
            new_val, ok = QInputDialog.getText(
                self, f"Tahrirlash: {col_name}",
                f"'{item.get('m')}' uchun {col_name}:",
                text=current_val
            )
            if ok:
                item[col_key] = new_val.strip()
                if self.app and hasattr(self.app, "data_manager"):
                    self.app.data_manager.update_organization(item, user="ADMIN")
                self.render_table_rows()
                if hasattr(self.app, "show_toast"):
                    self.app.show_toast(f"'{col_name}' saqlandi! ✅", "success")
            return

        from ui_qt.views.org_edit_dialog import OrgEditDialog
        dlg = OrgEditDialog(parent=self, app=self.app, item=item)
        if dlg.exec_() == OrgEditDialog.Accepted:
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            self.load_data()

    def open_column_manager(self):
        """Shartnomalar jadvaliga ustun qo'shish va boshqarish dialogi."""
        from ui_qt.components.column_manager_dialog import ColumnManagerDialog
        cur_cols = self._load_custom_columns()
        dlg = ColumnManagerDialog(view_type="contracts", current_columns=cur_cols, parent=self, app=self.app)
        if dlg.exec_() == ColumnManagerDialog.Accepted:
            new_cols = dlg.get_columns()
            self.custom_columns = new_cols
            if self.app and hasattr(self.app, "data_manager"):
                self.app.data_manager.settings["contracts_custom_columns"] = new_cols
                self.app.data_manager.save_settings()
            self.setup_table_columns()
            self.render_table_rows()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("Shartnoma jadvali ustunlari muvaffaqiyatli yangilandi! ⚙", "success")

    def render_table_rows(self):
        """Jadval qatorlarini professional, tartibli va rangli nishonlar bilan chizish."""
        self.table.setUpdatesEnabled(False)
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)
        is_light = (self.current_theme == "light")

        try:
            self.table.setRowCount(len(self.filtered_data))
            for r_idx, it in enumerate(self.filtered_data):
                # 0. №
                item_no = NumericTableWidgetItem(str(r_idx + 1), sort_value=r_idx + 1)
                item_no.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 0, item_no)

                # 1. Tashkilot Nomi
                name_str = str(it.get("m", "-")).strip() or "-"
                item_name = QTableWidgetItem(name_str)
                self.table.setItem(r_idx, 1, item_name)

                # 2. INN
                inn_str = str(it.get("inn", "-")).strip() or "-"
                inn_digits = "".join(filter(str.isdigit, inn_str))
                sort_inn = int(inn_digits) if inn_digits.isdigit() else 0
                item_inn = NumericTableWidgetItem(inn_str, sort_value=sort_inn)
                item_inn.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 2, item_inn)

                # 3. Toifasi
                item_cat = QTableWidgetItem(str(it.get("s", "-")))
                item_cat.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 3, item_cat)

                # 4. Apparat SHT
                aparat_val = it.get("aparat_soni")
                item_aparat = NumericTableWidgetItem(
                    f"{aparat_val} ta" if aparat_val is not None else "—",
                    sort_value=aparat_val if aparat_val is not None else -1
                )
                item_aparat.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 4, item_aparat)

                # 5. Ulangan
                ulangan_val = it.get("ulangan_soni")
                item_ulangan = NumericTableWidgetItem(
                    f"{ulangan_val} ta" if ulangan_val is not None else "—",
                    sort_value=ulangan_val if ulangan_val is not None else -1
                )
                item_ulangan.setTextAlignment(Qt.AlignCenter)
                if ulangan_val is not None and ulangan_val > 0:
                    item_ulangan.setForeground(QColor("#10b981" if not is_light else "#059669"))
                self.table.setItem(r_idx, 5, item_ulangan)

                # 6. Rahbar Tel
                raxbar_str = str(it.get("t", "-")).strip() or "-"
                item_raxbar = QTableWidgetItem(raxbar_str)
                item_raxbar.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r_idx, 6, item_raxbar)

                # 7. Buxgalter Tel
                bux_str = str(it.get("bux_tel", "-")).strip() or "-"
                item_bux = QTableWidgetItem(bux_str)
                item_bux.setTextAlignment(Qt.AlignCenter)
                if bux_str != "-":
                    item_bux.setForeground(QColor("#38bdf8" if not is_light else "#0284c7"))
                self.table.setItem(r_idx, 7, item_bux)

                # 8+. Maxsus qo'shilgan ustunlar
                for c_idx, c_info in enumerate(self.custom_columns):
                    col_key = c_info.get("key", "")
                    val = it.get(col_key)
                    val_str = str(val).strip() if val is not None else ""
                    display_txt = val_str if val_str else "—"

                    if col_key in ("aparat_soni", "ulangan_soni"):
                        s_val = int(val) if val not in (None, "") else -1
                        item_c = NumericTableWidgetItem(f"{val} ta" if val is not None else "—", sort_value=s_val)
                    elif val_str.isdigit():
                        item_c = NumericTableWidgetItem(val_str, sort_value=int(val_str))
                    else:
                        item_c = QTableWidgetItem(display_txt)

                    item_c.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(r_idx, 8 + c_idx, item_c)

            self.lbl_count.setText(f"Ko'rsatilmoqda: {len(self.filtered_data)} ta tashkilot")
        finally:
            self.table.setSortingEnabled(True)
            self.table.blockSignals(False)
            self.table.setUpdatesEnabled(True)

    def open_add_dialog(self, prefill_category: Optional[str] = None):
        """Yangi tashkilot / shartnoma ma'lumotini qo'shish dialogi."""
        init_item = {"_is_new": True}
        cat_to_use = prefill_category or (self.current_category if self.current_category != "Barchasi" else None)
        if cat_to_use:
            init_item["s"] = cat_to_use

        dlg = ContractAddDialog(parent=self, app=self.app, item=init_item)
        if dlg.exec_() == ContractAddDialog.Accepted:
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            self.load_data()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("Yangi tashkilot muvaffaqiyatli qo'shildi! ✅", "success")

    def open_edit_dialog(self):
        """Tanlangan shartnoma ma'lumotini tahrirlash dialogi."""
        row = self.table.currentRow()
        item = self._get_item_by_row(row)
        if not item:
            QMessageBox.information(self, "Ma'lumot", "Tahrirlash uchun jadvaldan tashkilotni tanlang.")
            return
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
        item = self._get_item_by_row(row)
        if not item:
            return

        menu = QMenu(self)

        # Nusxalash amallari
        act_copy_cells = menu.addAction("📋 Tanlangan kataklarni nusxalash (Ctrl+C)")
        act_copy_cells.triggered.connect(self.copy_selected_cells)

        act_copy_row = menu.addAction("📋 Butun qatorni nusxalash")
        act_copy_row.triggered.connect(lambda: self._copy_entire_row(item))

        menu.addSeparator()

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
                "Apparat Soni", "Ulangan Soni",
                "Rahbar Telefoni", "Buxgalter Telefoni"
            ]
            for c in self.custom_columns:
                headers.append(str(c.get("name", "Ustun")))
            ws.append(headers)

            for idx, it in enumerate(self.filtered_data, 1):
                ap = it.get("aparat_soni")
                ul = it.get("ulangan_soni")

                row_vals = [
                    idx,
                    str(it.get("m", "")),
                    str(it.get("inn", "")),
                    str(it.get("s", "")),
                    ap if ap is not None else "",
                    ul if ul is not None else "",
                    str(it.get("t", "")),
                    str(it.get("bux_tel", ""))
                ]
                for c in self.custom_columns:
                    val = it.get(c.get("key", ""))
                    row_vals.append(str(val if val is not None else ""))
                ws.append(row_vals)

            wb.save(path)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(f"📊 {len(self.filtered_data)} ta shartnoma Excelga saqlandi!", "success")
            QMessageBox.information(self, "Muvaffaqiyatli", f"{len(self.filtered_data)} ta tashkilot shartnomalari Excelga saqlandi!")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Excel saqlashda xatolik: {e}")

