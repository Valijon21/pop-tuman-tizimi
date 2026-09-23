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
    QMessageBox, QFileDialog, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QModelIndex
from ui_qt.components.table_model import OrganizationTableModel
from ui_qt.views.org_edit_dialog import OrgEditDialog
from ui_qt.views.cabinet_dialog import open_cabinet_dialog, copy_cabinet_quick
from ui_qt.views.verification_dialog import open_verification_dialog, copy_verification_quick
from services.search_service import SearchService
from services.excel_service import export_organizations_to_excel
from services.qr_service import generate_phone_qr_image
from core.logger import logger

class TableView(QWidget):
    """PyQt5 Tashkilotlar Jadvali Ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_category = "Barchasi"
        self.filtered_data: List[Dict[str, Any]] = []
        self.current_theme: str = getattr(app, "current_theme", "dark")

        self.setup_ui()
        self.init_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(8)

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
        self.edit_search.setPlaceholderText("🔍 Qidiruv...")
        self.edit_search.textChanged.connect(self.on_search_changed)
        self.edit_search.setMinimumWidth(140)
        toolbar.addWidget(self.edit_search, 1)

        self.btn_clear = QPushButton("✖")
        self.btn_clear.setFixedSize(26, 26)
        self.btn_clear.setObjectName("btn_clear_search")
        self.btn_clear.clicked.connect(lambda: self.edit_search.clear())
        toolbar.addWidget(self.btn_clear)

        # Amallar tugmalari (Ixcham va tartibli)
        def add_tool_btn(txt, cmd, bg_color, min_w=70):
            btn = QPushButton(txt)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: white;
                    font-weight: 700;
                    padding: 5px 9px;
                    border-radius: 6px;
                    min-width: {min_w}px;
                    font-size: 11.5px;
                }}
            """)
            btn.clicked.connect(cmd)
            toolbar.addWidget(btn)
            return btn

        add_tool_btn("➕ Qo'shish", self.open_add_dialog, "#16a34a", 72)
        add_tool_btn("✏ Tahrir", self.open_edit_dialog, "#f59e0b", 62)
        add_tool_btn("🔑 Kabinet", self.open_cabinet, "#d97706", 68)
        add_tool_btn("🛡 Verifikatsiya", self.open_verification, "#0284c7", 82)
        add_tool_btn("📊 Excel", self.export_excel, "#059669", 60)

        # Qo'shimcha amallar menyu tugmasi
        self.btn_more = QPushButton("⚡ Boshqa ▾")
        self.btn_more.setObjectName("btn_more_actions")
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

        # Clear button
        if is_light:
            self.btn_clear.setStyleSheet("background: #e2e8f0; color: #475569; font-weight: bold; border-radius: 6px; padding: 0px;")
        else:
            self.btn_clear.setStyleSheet("background: #334155; color: #94a3b8; font-weight: bold; border-radius: 6px; padding: 0px;")

        # Boshqa tugmasi
        if is_light:
            self.btn_more.setStyleSheet("""
                QPushButton { background-color: #e2e8f0; color: #0f172a; font-weight: 700; padding: 5px 9px; border-radius: 6px; min-width: 70px; font-size: 11.5px; }
                QPushButton:hover { background-color: #cbd5e1; }
            """)
        else:
            self.btn_more.setStyleSheet("""
                QPushButton { background-color: #334155; color: #f8fafc; font-weight: 700; padding: 5px 9px; border-radius: 6px; min-width: 70px; font-size: 11.5px; }
                QPushButton:hover { background-color: #475569; }
            """)

        # Footer yozuvlari
        if is_light:
            self.lbl_count.setStyleSheet("font-size: 13px; font-weight: 700; color: #475569;")
            self.lbl_hint.setStyleSheet("font-size: 11px; color: #94a3b8;")
        else:
            self.lbl_count.setStyleSheet("font-size: 13px; font-weight: 700; color: #94a3b8;")
            self.lbl_hint.setStyleSheet("font-size: 11px; color: #64748b;")

        # Category pills
        self.update_pill_selection(self.current_category)

    def init_data(self):
        self.update_pill_selection("Barchasi")
        self.filter_data()

    def update_pill_selection(self, selected_cat: str):
        self.current_category = selected_cat
        is_light = (self.current_theme == "light")
        for cat, btn in self.pill_buttons.items():
            btn.setChecked(cat == selected_cat)
            if cat == selected_cat:
                btn.setStyleSheet("background-color: #2563eb; color: white; font-weight: 700; border-radius: 14px; padding: 6px 16px;")
            else:
                if is_light:
                    btn.setStyleSheet("background-color: #f1f5f9; color: #475569; font-weight: 600; border: 1px solid #e2e8f0; border-radius: 14px; padding: 6px 16px;")
                else:
                    btn.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-weight: 600; border: 1px solid #334155; border-radius: 14px; padding: 6px 16px;")

    def on_category_clicked(self, cat: str):
        self.update_pill_selection(cat)
        self.filter_data()

    def on_search_changed(self):
        self.filter_data()

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

        try:
            cnt = export_organizations_to_excel(self.filtered_data, path, category_name=self.current_category)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(f"📊 {cnt} ta tashkilot Excelga saqlandi!", "success")
            QMessageBox.information(self, "Muvaffaqiyatli", f"{cnt} ta tashkilot muvaffaqiyatli Excelga saqlandi!")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Excel saqlashda xatolik: {e}")

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
