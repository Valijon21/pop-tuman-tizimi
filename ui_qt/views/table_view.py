"""
ui_qt.views.table_view: Asosiy tashkilotlar jadvali (Table View) (PyQt5).
Senior-darajadagi QTableView, QAbstractTableModel, toifalar pill-paneli,
boyitilgan asboblar paneli va to'liq kontekstli menyu.
Dark va Light mavzuga to'liq moslashgan.
"""
from typing import Any, Optional, Dict, List
import pyperclip
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTableView, QHeaderView, QMenu,
    QMessageBox, QFileDialog, QFrame, QScrollArea, QShortcut
)
from PyQt5.QtCore import Qt, QModelIndex, QTimer, QEvent
from PyQt5.QtGui import QKeySequence
from ui_qt.components.table_model import OrganizationTableModel
from ui_qt.views.org_edit_dialog import OrgEditDialog
from ui_qt.views.cabinet_dialog import open_cabinet_dialog, copy_cabinet_quick
from ui_qt.views.verification_dialog import open_verification_dialog, copy_verification_quick
from services.search_service import SearchService
from services.excel_service import export_organizations_to_excel
from ui_qt.views.qr_dialog import open_qr_dialog
from core.logger import logger
from core.threading_utils import WorkerThread

class TableView(QWidget):
    """PyQt5 Tashkilotlar Jadvali Ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_category = "Barchasi"
        self.filtered_data: List[Dict[str, Any]] = []
        self.current_theme: str = getattr(app, "current_theme", "dark")

        # Qidiruv uchun 250ms Debounce taymeri
        self.search_timer = QTimer(self)
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_data)

        self.setup_ui()
        self.init_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(8)

        # 0. HEADER (Sarlavha va Subtitr)
        is_light = (self.current_theme == "light")
        head_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        self.lbl_title = QLabel("🏢 Tashkilotlar Ro'yxati va Boshqaruvi")
        self.lbl_title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0284c7;" if is_light else "font-size: 15px; font-weight: 800; color: #38bdf8;")
        self.lbl_subtitle = QLabel("Pop tumani barcha davlat va nodavlat tashkilotlari, rahbarlar, INN va aloqalar reyestri")
        self.lbl_subtitle.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        title_box.addWidget(self.lbl_title)
        title_box.addWidget(self.lbl_subtitle)
        head_layout.addLayout(title_box)
        head_layout.addStretch()
        main_layout.addLayout(head_layout)

        # 1. ASBOBLAR PANELI (TOOLBAR)
        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        # Qidiruv maydoni
        self.combo_search_type = QComboBox()
        self.combo_search_type.addItems(["Nomi", "F.I.SH", "INN", "Izoh"])
        self.combo_search_type.setFixedWidth(85)
        self.combo_search_type.currentIndexChanged.connect(self.on_search_changed)
        toolbar.addWidget(self.combo_search_type)

        self.edit_search = QLineEdit()
        self.edit_search.setPlaceholderText("🔍 Qidiruv (Ctrl+F)...")
        self.edit_search.textChanged.connect(self.on_search_changed)
        self.edit_search.returnPressed.connect(self.filter_data)
        self.edit_search.setMinimumWidth(140)
        toolbar.addWidget(self.edit_search, 1)

        self.btn_clear = QPushButton("✖")
        self.btn_clear.setFixedSize(26, 26)
        self.btn_clear.setObjectName("btn_clear_search")
        self.btn_clear.clicked.connect(lambda: self.edit_search.clear())
        toolbar.addWidget(self.btn_clear)

        # Amallar tugmalari (Ixcham, tartibli va professional Senior uslubi)
        def add_tool_btn(txt, cmd, css_class="btn_secondary", min_w=65):
            btn = QPushButton(txt)
            btn.setProperty("class", css_class)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumWidth(min_w)
            btn.clicked.connect(cmd)
            toolbar.addWidget(btn)
            return btn

        self.btn_add = add_tool_btn("➕ Qo'shish", self.open_add_dialog, "btn_primary", 76)
        self.btn_edit = add_tool_btn("✏ Tahrir", self.open_edit_dialog, "btn_warning", 66)
        self.btn_cabinet = add_tool_btn("🔑 Kabinet", self.open_cabinet, "btn_secondary", 70)
        self.btn_verif = add_tool_btn("🛡 Verifikatsiya", self.open_verification, "btn_info", 86)
        self.btn_qr = add_tool_btn("📱 QR Kod", self.open_qr, "btn_purple", 74)
        self.btn_excel = add_tool_btn("📊 Excel", self.export_excel, "btn_success", 66)

        # Qo'shimcha amallar menyu tugmasi
        self.btn_more = QPushButton("⚡ Boshqa ▾")
        self.btn_more.setObjectName("btn_more_actions")
        self.btn_more.setProperty("class", "btn_secondary")
        self.btn_more.setCursor(Qt.PointingHandCursor)
        more_menu = QMenu(self)
        act_yettilik = more_menu.addAction("🏘 Mahalla 'Yettiligi' (360° Pasport)")
        act_yettilik.triggered.connect(self.open_yettilik)
        act_broadcast = more_menu.addAction("📢 Ommaviy Xabarnoma (SMS/Telegram)")
        act_broadcast.triggered.connect(self.open_broadcast)
        act_history = more_menu.addAction("📜 Kadrlar Almashinuvi Tarixi")
        act_history.triggered.connect(lambda: self.app.open_history() if hasattr(self.app, "open_history") else None)
        act_import = more_menu.addAction("📥 Excel / CSV Ommaviy Import")
        act_import.triggered.connect(lambda: self.app.open_import() if hasattr(self.app, "open_import") else None)
        more_menu.addSeparator()
        act_trash = more_menu.addAction("🗑 Chiqindi Qutisi")
        act_trash.triggered.connect(lambda: self.app.show_trash() if hasattr(self.app, "show_trash") else None)

        self.btn_more.setMenu(more_menu)
        toolbar.addWidget(self.btn_more)

        main_layout.addLayout(toolbar)

        # 2. KATEGORIYA PILL-PANELI (Gorizontal skroll bilan)
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
        categories = ["Barchasi"] + (self.app.data_manager.categories if self.app else [])
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

        # 3. ASOSIY QTABLEVIEW
        self.table_view = QTableView()
        self.table_model = OrganizationTableModel()
        self.table_view.setModel(self.table_model)

        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().setVisible(False)

        # Ustunlar kengligi
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.Stretch)

        # Hodisalar
        self.table_view.doubleClicked.connect(self.on_table_double_clicked)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)
        self.table_view.installEventFilter(self)

        # Klaviaturadan qidiruvga o'tish (Ctrl+F)
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self.focus_search)

        main_layout.addWidget(self.table_view, 1)

        # 4. FOOTER STATUS
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Jami: 0 ta")
        self.lbl_count.setObjectName("table_footer_count")
        footer.addWidget(self.lbl_count)

        footer.addStretch()
        self.lbl_hint = QLabel("💡 2 marta bosish - Tahrirlash | O'ng tugma - Kabinet / Verifikatsiya menyusi")
        self.lbl_hint.setObjectName("table_footer_hint")
        footer.addWidget(self.lbl_hint)

        main_layout.addLayout(footer)

    def set_theme(self, theme: str):
        """Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish."""
        self.current_theme = theme
        is_light = (theme == "light")

        if hasattr(self, "lbl_title"):
            self.lbl_title.setStyleSheet(f"font-size: 15px; font-weight: 800; color: {'#0284c7' if is_light else '#38bdf8'};")
        if hasattr(self, "lbl_subtitle"):
            self.lbl_subtitle.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")

        # Clear button
        if is_light:
            self.btn_clear.setStyleSheet("background: #e2e8f0; color: #475569; font-weight: bold; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0px;")
            self.lbl_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #475569;")
            self.lbl_hint.setStyleSheet("font-size: 11px; color: #64748b;")
        else:
            self.btn_clear.setStyleSheet("background: #334155; color: #cbd5e1; font-weight: bold; border: 1px solid #475569; border-radius: 6px; padding: 0px;")
            self.lbl_count.setStyleSheet("font-size: 12px; font-weight: 700; color: #94a3b8;")
            self.lbl_hint.setStyleSheet("font-size: 11px; color: #64748b;")

        # Category pills
        self.update_pill_selection(self.current_category)

    def init_data(self):
        self.update_pill_selection("Barchasi")
        self.filter_data()

    def update_pill_selection(self, selected_cat: str):
        self.current_category = selected_cat
        for cat, btn in self.pill_buttons.items():
            btn.setChecked(cat == selected_cat)

    def on_category_clicked(self, cat: str):
        self.update_pill_selection(cat)
        self.filter_data()

    def focus_search(self):
        """Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash."""
        self.edit_search.setFocus()
        self.edit_search.selectAll()

    def on_search_changed(self):
        """250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi."""
        if hasattr(self, "search_timer"):
            self.search_timer.start(250)
        else:
            self.filter_data()

    def eventFilter(self, source, event):
        """Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)."""
        if source == self.table_view and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.open_edit_dialog()
                return True
            elif event.key() == Qt.Key_Delete:
                item = self.get_selected_item()
                if item:
                    self.delete_item(item)
                return True
        return super().eventFilter(source, event)

    def filter_data(self):
        """Ma'lumotlarni SearchService orqali qidirish va modelga uzatish."""
        if not self.app or not hasattr(self.app, "data"):
            return

        query = self.edit_search.text().strip()
        f_type = self.combo_search_type.currentText()
        cat = self.current_category

        self.filtered_data = SearchService.search(
            self.app.data,
            query=query,
            category=cat,
            field_type=f_type
        )

        self.table_model.set_data(self.filtered_data)
        self.lbl_count.setText(f"Jami ko'rsatilmoqda: {len(self.filtered_data)} ta tashkilot")

    def get_selected_item(self) -> Optional[Dict[str, Any]]:
        indexes = self.table_view.selectionModel().selectedRows()
        if not indexes:
            return None
        row = indexes[0].row()
        return self.table_model.get_item_by_row(row)

    def on_table_double_clicked(self, index: QModelIndex):
        self.open_edit_dialog()

    def open_add_dialog(self):
        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self):
                return
        dlg = OrgEditDialog(parent=self, app=self.app)
        if dlg.exec_() == OrgEditDialog.Accepted:
            self.filter_data()
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()

    def open_edit_dialog(self):
        item = self.get_selected_item()
        if not item:
            QMessageBox.information(self, "Ma'lumot", "Tahrirlash uchun jadvaldan tashkilotni tanlang.")
            return

        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self):
                return

        dlg = OrgEditDialog(parent=self, app=self.app, item=item)
        if dlg.exec_() == OrgEditDialog.Accepted:
            self.filter_data()
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()

    def open_cabinet(self):
        item = self.get_selected_item()
        open_cabinet_dialog(self.app, item)

    def open_verification(self):
        item = self.get_selected_item()
        open_verification_dialog(self.app, item)

    def open_qr(self, item: Optional[Dict[str, Any]] = None):
        if not item:
            item = self.get_selected_item()
        if not item:
            QMessageBox.information(self, "Ma'lumot", "QR-kod yaratish uchun jadvaldan tashkilotni tanlang.")
            return
        open_qr_dialog(self.app, item=item)

    def open_yettilik(self):
        item = self.get_selected_item()
        mahalla_name = item.get("m") if item else None
        if hasattr(self.app, "open_yettilik"):
            self.app.open_yettilik(mahalla_name)

    def open_broadcast(self):
        if hasattr(self.app, "open_broadcast"):
            self.app.open_broadcast()

    def export_excel(self):
        if not self.filtered_data:
            QMessageBox.warning(self, "Ogohlantirish", "Eksport qilish uchun jadvalda ma'lumot yo'q.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Excel faylini saqlash", "tashkilotlar.xlsx", "Excel Files (*.xlsx)"
        )
        if not path:
            return

        if hasattr(self.app, "show_toast"):
            self.app.show_toast("📊 Excel fayl shakllantirilmoqda...", "info")

        def _do_export():
            return export_organizations_to_excel(self.filtered_data, path, category_name=self.current_category)

        self._export_worker = WorkerThread(_do_export, parent=self)
        self._export_worker.result_ready.connect(lambda cnt: self._on_export_done(cnt, path))
        self._export_worker.error_occurred.connect(self._on_export_err)
        self._export_worker.start()

    def _on_export_done(self, cnt: int, path: str):
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"📊 {cnt} ta tashkilot Excelga saqlandi!", "success")
        QMessageBox.information(self, "Muvaffaqiyatli", f"{cnt} ta tashkilot muvaffaqiyatli Excelga saqlandi!\n\nFayl: {path}")

    def _on_export_err(self, err: str):
        logger.error(f"[EXCEL EKSPORT] Xatolik: {err}")
        QMessageBox.critical(self, "Xatolik", f"Excel saqlashda xatolik yuz berdi:\n{err}")

    def show_context_menu(self, pos):
        """O'ng tugma bosilganda kontekst menyu."""
        index = self.table_view.indexAt(pos)
        if not index.isValid():
            return

        item = self.table_model.get_item_by_row(index.row())
        if not item:
            return

        menu = QMenu(self)

        # 1. Asosiy shablonlar
        act_cab = menu.addAction("🔑 Kabinetga dostup (Dialog)")
        act_cab.triggered.connect(lambda: open_cabinet_dialog(self.app, item))

        act_cab_quick = menu.addAction("⚡ Tezkor Kabinetga dostup nusxalash")
        act_cab_quick.triggered.connect(lambda: copy_cabinet_quick(self.app, item))

        menu.addSeparator()

        act_verif = menu.addAction("🛡 Verifikatsiya so'rovi (Dialog)")
        act_verif.triggered.connect(lambda: open_verification_dialog(self.app, item))

        act_verif_quick = menu.addAction("⚡ Tezkor Verifikatsiya nusxalash")
        act_verif_quick.triggered.connect(lambda: copy_verification_quick(self.app, item))

        menu.addSeparator()

        act_yettilik = menu.addAction("🏘 Mahalla 'Yettiligi' (360° Pasport)")
        act_yettilik.triggered.connect(lambda: self.app.open_yettilik(item.get("m")))

        act_history = menu.addAction("📜 Kadrlar almashinuvi tarixi")
        act_history.triggered.connect(lambda: self.app.open_history(mahalla=item.get("m")))

        act_broadcast = menu.addAction("📢 Ommaviy Xabarnoma")
        act_broadcast.triggered.connect(self.app.open_broadcast)

        act_qr = menu.addAction("📱 QR Kod (Telefon & Kontakt)")
        act_qr.triggered.connect(lambda: self.open_qr(item))

        menu.addSeparator()

        act_edit = menu.addAction("✏ Tahrirlash")
        act_edit.triggered.connect(self.open_edit_dialog)

        # Nusxalash amallari
        act_copy_phone = menu.addAction("📞 Telefonni nusxalash")
        act_copy_phone.triggered.connect(lambda: pyperclip.copy(str(item.get("t", ""))))

        bux_tel = str(item.get("bux_tel", "")).strip()
        if bux_tel:
            act_copy_bux = menu.addAction(f"💼 Buxgalter tel nusxalash ({bux_tel})")
            act_copy_bux.triggered.connect(lambda: self._copy_and_toast(bux_tel, "Buxgalter telefoni nusxalandi! 💼"))

        act_copy_inn = menu.addAction("🆔 INN nusxalash")
        act_copy_inn.triggered.connect(lambda: pyperclip.copy(str(item.get("inn", ""))))

        act_copy_row = menu.addAction("📋 Butun qatorni nusxalash")
        act_copy_row.triggered.connect(lambda: self.copy_entire_row(item))

        menu.addSeparator()

        act_delete = menu.addAction("🗑 Chiqindiga tashlash")
        act_delete.triggered.connect(lambda: self.delete_item(item))

        menu.exec_(self.table_view.viewport().mapToGlobal(pos))

    def _copy_and_toast(self, text: str, msg: str):
        if text:
            pyperclip.copy(text)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(msg, "success")

    def copy_entire_row(self, item: Dict[str, Any]):
        row_str = f"{item.get('s', '')}\t{item.get('m', '')}\t{item.get('f', '')}\t{item.get('t', '')}\t{item.get('inn', '')}\t{item.get('izoh', '')}"
        pyperclip.copy(row_str)
        if hasattr(self.app, "show_toast"):
            self.app.show_toast("Qator xotiraga nusxalandi! 📋", "success")

    def delete_item(self, item: Dict[str, Any]):
        if self.app and hasattr(self.app, "check_permission"):
            if not self.app.check_permission("edit", parent=self):
                return
        reply = QMessageBox.question(
            self, "Tasdiqlash",
            f"'{item.get('m')}' tashkilotini chiqindi qutisiga tashlamoqchimisiz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.app.data_manager.move_to_trash(item)
            self.filter_data()
            if hasattr(self.app, "show_toast"):
                self.app.show_toast("Tashkilot chiqindiga tashlandi.", "warning")
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()

def render_table(parent: Any, app: Any):
    view = TableView(parent=parent, app=app)
    return view
