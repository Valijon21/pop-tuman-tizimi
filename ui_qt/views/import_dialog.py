"""
ui_qt.views.import_dialog: Excel va CSV fayllar bilan ikki tomonlama aqlli sinxronizatsiya (Smart Diff & Merge).
Mavjud tashkilotlarni INN yoki nom bo'yicha solishtirish, o'zgarishlar diff tahlili va selektiv sinxronlash.
"""
from typing import Optional, Any, List, Dict, Tuple
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFrame, QButtonGroup, QCheckBox, QAbstractItemView
)
from PyQt5.QtCore import Qt
from services.excel_service import import_organizations_from_file
from services.search_service import normalize_text
from ui_qt.styles import get_stylesheet
from core.logger import logger
from core.threading_utils import WorkerThread


class ImportDialog(QDialog):
    """Excel / CSV ommaviy import va aqlli sinxronizatsiya (Smart Diff & Merge) dialogi."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_theme = getattr(app, "current_theme", "dark")
        self.all_analyzed_items: List[Dict[str, Any]] = []
        self.current_filter = "ALL"  # ALL, MODIFIED, NEW, UNCHANGED

        self.setWindowTitle("🔄 Excel / CSV Ikki Tomonlama Sinxronizatsiya (Smart Merge)")
        self.resize(880, 560)
        self.setMinimumSize(700, 440)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # 1. Header
        head = QVBoxLayout()
        head.setSpacing(2)
        title = QLabel("🔄 Excel va CSV Aqlli Sinxronizatsiya (Smart Diff & Merge)")
        title_color = "#059669" if is_light else "#10b981"
        title.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {title_color};")
        sub = QLabel("Fayldagi ma'lumotlarni mavjud baza bilan solishtirish, o'zgarishlarni ko'rish va xavfsiz yangilash")
        sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        head.addWidget(title)
        head.addWidget(sub)
        layout.addLayout(head)

        # 2. Fayl tanlash paneli
        file_box = QHBoxLayout()
        self.lbl_file = QLabel("Fayl tanlanmagan")
        file_bg = "#ffffff" if is_light else "#1e293b"
        file_fg = "#0f172a" if is_light else "#f8fafc"
        file_border = "#cbd5e1" if is_light else "#334155"
        self.lbl_file.setStyleSheet(f"font-size: 12px; color: {file_fg}; background: {file_bg}; border: 1px solid {file_border}; padding: 6px 12px; border-radius: 6px;")
        file_box.addWidget(self.lbl_file, 1)

        self.btn_browse = QPushButton("📁 Faylni Tanlash (.xlsx, .csv)...")
        self.btn_browse.setProperty("class", "btn_secondary")
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.clicked.connect(self.browse_file)
        file_box.addWidget(self.btn_browse)
        layout.addLayout(file_box)

        # 3. Filter Segmented Tabs (Barchasi, O'zgarishlar, Yangilar, Mos kelganlar)
        tab_box = QHBoxLayout()
        tab_box.setSpacing(6)

        self.btn_tab_all = QPushButton("📋 Barchasi (0)")
        self.btn_tab_all.setProperty("class", "pill_btn")
        self.btn_tab_all.setCheckable(True)
        self.btn_tab_all.setChecked(True)
        self.btn_tab_all.clicked.connect(lambda: self.set_filter("ALL"))

        self.btn_tab_modified = QPushButton("🟡 O'zgarishlar / Diff (0)")
        self.btn_tab_modified.setProperty("class", "pill_btn")
        self.btn_tab_modified.setCheckable(True)
        self.btn_tab_modified.clicked.connect(lambda: self.set_filter("MODIFIED"))

        self.btn_tab_new = QPushButton("🟢 Yangi tashkilotlar (0)")
        self.btn_tab_new.setProperty("class", "pill_btn")
        self.btn_tab_new.setCheckable(True)
        self.btn_tab_new.clicked.connect(lambda: self.set_filter("NEW"))

        self.btn_tab_unchanged = QPushButton("⚪ O'zgarishsiz (0)")
        self.btn_tab_unchanged.setProperty("class", "pill_btn")
        self.btn_tab_unchanged.setCheckable(True)
        self.btn_tab_unchanged.clicked.connect(lambda: self.set_filter("UNCHANGED"))

        tab_group = QButtonGroup(self)
        tab_group.addButton(self.btn_tab_all)
        tab_group.addButton(self.btn_tab_modified)
        tab_group.addButton(self.btn_tab_new)
        tab_group.addButton(self.btn_tab_unchanged)

        tab_box.addWidget(self.btn_tab_all)
        tab_box.addWidget(self.btn_tab_modified)
        tab_box.addWidget(self.btn_tab_new)
        tab_box.addWidget(self.btn_tab_unchanged)
        tab_box.addStretch()

        # Tezkor tanlash tugmalari
        self.btn_select_all = QPushButton("☑ Hammasini belgilash")
        self.btn_select_all.setProperty("class", "btn_secondary")
        self.btn_select_all.setFixedHeight(28)
        self.btn_select_all.clicked.connect(lambda: self.toggle_all_selection(True))
        tab_box.addWidget(self.btn_select_all)

        self.btn_deselect_all = QPushButton("☐ Tozalash")
        self.btn_deselect_all.setProperty("class", "btn_secondary")
        self.btn_deselect_all.setFixedHeight(28)
        self.btn_deselect_all.clicked.connect(lambda: self.toggle_all_selection(False))
        tab_box.addWidget(self.btn_deselect_all)

        layout.addLayout(tab_box)

        # 4. Oldindan ko'rish va Diff Jadvali
        self.table_preview = QTableWidget()
        self.table_preview.setColumnCount(7)
        self.table_preview.setHorizontalHeaderLabels([
            "Tanlash", "Holati", "Tashkilot Nomi", "INN", "Toifasi", "Rahbar F.I.SH", "O'zgarishlar Tahlili (Diff)"
        ])
        self.table_preview.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table_preview.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.table_preview.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_preview.setAlternatingRowColors(True)
        self.table_preview.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_preview.setSelectionMode(QTableWidget.SingleSelection)
        self.table_preview.verticalHeader().setVisible(False)
        layout.addWidget(self.table_preview, 1)

        # 5. Footer & Amallar
        footer = QHBoxLayout()
        self.lbl_count = QLabel("Topilgan yozuvlar: 0 ta")
        self.lbl_count.setStyleSheet(f"font-size: 12px; color: {'#059669' if is_light else '#10b981'}; font-weight: 700;")
        footer.addWidget(self.lbl_count)

        footer.addStretch()

        self.btn_merge = QPushButton("✅ Tanlanganlarni Sinxronlash (Smart Merge)")
        self.btn_merge.setEnabled(False)
        self.btn_merge.setProperty("class", "btn_success")
        self.btn_merge.setCursor(Qt.PointingHandCursor)
        self.btn_merge.clicked.connect(self.commit_smart_merge)
        footer.addWidget(self.btn_merge)

        self.btn_close = QPushButton("Yopish")
        self.btn_close.setProperty("class", "btn_secondary")
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.clicked.connect(self.reject)
        footer.addWidget(self.btn_close)

        layout.addLayout(footer)

    def set_filter(self, f_type: str):
        self.current_filter = f_type
        self.render_table()

    def toggle_all_selection(self, select: bool):
        for idx in range(self.table_preview.rowCount()):
            chk_item = self.table_preview.item(idx, 0)
            if chk_item and chk_item.flags() & Qt.ItemIsUserCheckable:
                chk_item.setCheckState(Qt.Checked if select else Qt.Unchecked)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excel yoki CSV faylni tanlang", "",
            "Jadvallar (*.xlsx *.xls *.csv);;Barcha fayllar (*.*)"
        )
        if not file_path:
            return

        self.lbl_file.setText(os.path.basename(file_path))
        self.lbl_count.setText("⏳ Fayl o'qilmoqda va baza bilan solishtirilmoqda...")
        self.btn_browse.setEnabled(False)
        self.btn_merge.setEnabled(False)

        def _read_file():
            items, warnings = import_organizations_from_file(file_path)
            return self._analyze_differences(items)

        self._read_worker = WorkerThread(_read_file, parent=self)
        self._read_worker.result_ready.connect(self._on_analysis_done)
        self._read_worker.error_occurred.connect(self._on_file_read_error)
        self._read_worker.start()

    def _analyze_differences(self, imported_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Import qilingan har bir yozuvni mavjud baza bilan solishtirib diff hosil qilish."""
        existing_data = getattr(self.app, "data", []) if self.app else []
        
        # INN va Nom bo'yicha indekslash
        inn_map: Dict[str, Dict[str, Any]] = {}
        name_map: Dict[str, Dict[str, Any]] = {}

        for ex in existing_data:
            inn = str(ex.get("inn", "")).strip()
            if inn:
                inn_map[inn] = ex
            m_norm = normalize_text(ex.get("m", ""))
            if m_norm:
                name_map[m_norm] = ex

        analyzed: List[Dict[str, Any]] = []

        for it in imported_items:
            inn = str(it.get("inn", "")).strip()
            m_norm = normalize_text(it.get("m", ""))

            # Mavjud yozuvni topish (avval INN, keyin Nomi bo'yicha)
            matched_existing = None
            if inn and inn in inn_map:
                matched_existing = inn_map[inn]
            elif m_norm and m_norm in name_map:
                matched_existing = name_map[m_norm]

            entry = {
                "imported": it,
                "existing": matched_existing,
                "status": "NEW",  # NEW, MODIFIED, UNCHANGED
                "diffs": [],
                "checked": True
            }

            if matched_existing:
                # O'zgarishlarni maydonma-maydon solishtirish
                diffs = []
                check_fields = [
                    ("m", "Nomi"),
                    ("s", "Toifasi"),
                    ("f", "Rahbar F.I.SH"),
                    ("t", "Rahbar Telefoni"),
                    ("bux_tel", "Buxgalter Telefoni"),
                    ("inn", "INN"),
                    ("lavozim", "Lavozimi")
                ]

                for key, label in check_fields:
                    val_new = str(it.get(key, "") or "").strip()
                    val_old = str(matched_existing.get(key, "") or "").strip()
                    if val_new and val_old and val_new != val_old:
                        diffs.append(f"{label}: \"{val_old}\" ➔ \"{val_new}\"")
                    elif val_new and not val_old:
                        diffs.append(f"{label}: [Mavjud emas] ➔ \"{val_new}\"")

                if diffs:
                    entry["status"] = "MODIFIED"
                    entry["diffs"] = diffs
                    entry["checked"] = True  # O'zgarishlar standart holatda tasdiqlash uchun belgilangan
                else:
                    entry["status"] = "UNCHANGED"
                    entry["checked"] = False  # Bir xil bo'lsa standart belgilanmaydi
            else:
                entry["status"] = "NEW"
                entry["checked"] = True

            analyzed.append(entry)

        return analyzed

    def _on_analysis_done(self, analyzed_items: List[Dict[str, Any]]):
        self.btn_browse.setEnabled(True)
        self.all_analyzed_items = analyzed_items
        
        # Hisob-kitoblar
        cnt_all = len(analyzed_items)
        cnt_mod = sum(1 for x in analyzed_items if x["status"] == "MODIFIED")
        cnt_new = sum(1 for x in analyzed_items if x["status"] == "NEW")
        cnt_unc = sum(1 for x in analyzed_items if x["status"] == "UNCHANGED")

        self.btn_tab_all.setText(f"📋 Barchasi ({cnt_all})")
        self.btn_tab_modified.setText(f"🟡 O'zgarishlar / Diff ({cnt_mod})")
        self.btn_tab_new.setText(f"🟢 Yangi ({cnt_new})")
        self.btn_tab_unchanged.setText(f"⚪ O'zgarishsiz ({cnt_unc})")

        self.btn_merge.setEnabled(cnt_all > 0)
        self.lbl_count.setText(f"Tahlil qilindi: {cnt_all} ta (O'zgargan: {cnt_mod}, Yangi: {cnt_new}, O'zgarishsiz: {cnt_unc})")

        # Agar o'zgarishlar bo'lsa, birinchi bo'lib o'zgarishlar sahifasini ko'rsatish
        if cnt_mod > 0:
            self.btn_tab_modified.setChecked(True)
            self.current_filter = "MODIFIED"
        else:
            self.btn_tab_all.setChecked(True)
            self.current_filter = "ALL"

        self.render_table()

    def _on_file_read_error(self, err_msg: str):
        self.btn_browse.setEnabled(True)
        self.btn_merge.setEnabled(False)
        self.lbl_count.setText("❌ Faylni o'qishda xatolik yuz berdi")
        QMessageBox.critical(self, "Xatolik", f"Faylni o'qish yoki tahlil qilishda xatolik:\n{err_msg}")

    def render_table(self):
        """Jadvalni joriy filtrga asosan qayta chizish."""
        self.table_preview.setUpdatesEnabled(False)
        try:
            # Filtrni qo'llash
            if self.current_filter == "ALL":
                items_to_show = self.all_analyzed_items
            else:
                items_to_show = [x for x in self.all_analyzed_items if x["status"] == self.current_filter]

            self.table_preview.setRowCount(len(items_to_show))

            for r_idx, entry in enumerate(items_to_show):
                st = entry["status"]
                it = entry["imported"]

                # 0. Checkbox
                chk_item = QTableWidgetItem()
                chk_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                chk_item.setCheckState(Qt.Checked if entry.get("checked", True) else Qt.Unchecked)
                self.table_preview.setItem(r_idx, 0, chk_item)

                # 1. Holati (Rangli belgi)
                if st == "MODIFIED":
                    st_item = QTableWidgetItem("🟡 O'zgarish (Diff)")
                    st_item.setForeground(Qt.darkYellow)
                elif st == "NEW":
                    st_item = QTableWidgetItem("🟢 Yangi")
                    st_item.setForeground(Qt.darkGreen)
                else:
                    st_item = QTableWidgetItem("⚪ O'zgarishsiz")
                    st_item.setForeground(Qt.gray)
                self.table_preview.setItem(r_idx, 1, st_item)

                # 2-5. Asosiy ustunlar
                self.table_preview.setItem(r_idx, 2, QTableWidgetItem(str(it.get("m", "-"))))
                self.table_preview.setItem(r_idx, 3, QTableWidgetItem(str(it.get("inn", "-"))))
                self.table_preview.setItem(r_idx, 4, QTableWidgetItem(str(it.get("s", "-"))))
                self.table_preview.setItem(r_idx, 5, QTableWidgetItem(str(it.get("f", "-"))))

                # 6. Diff matni
                if st == "MODIFIED":
                    diff_txt = " | ".join(entry.get("diffs", []))
                elif st == "NEW":
                    diff_txt = "Yangi tashkilot sifatida to'liq bazaga kiritiladi"
                else:
                    diff_txt = "Mavjud ma'lumotlar bilan 100% mos keladi"

                self.table_preview.setItem(r_idx, 6, QTableWidgetItem(diff_txt))

        finally:
            self.table_preview.setUpdatesEnabled(True)

    def commit_smart_merge(self):
        """Tanlangan o'zgarishlarni bazaga xavfsiz sinxronlash (Smart Merge)."""
        if not self.all_analyzed_items:
            return

        # Qaysi qatorlar belgilanganini tekshirish
        selected_entries = []
        for r_idx in range(self.table_preview.rowCount()):
            chk_item = self.table_preview.item(r_idx, 0)
            if chk_item and chk_item.checkState() == Qt.Checked:
                # O'sha qator qaysi entry ga tegishli ekanligini topish
                if self.current_filter == "ALL":
                    entry = self.all_analyzed_items[r_idx]
                else:
                    filtered_sub = [x for x in self.all_analyzed_items if x["status"] == self.current_filter]
                    entry = filtered_sub[r_idx]
                selected_entries.append(entry)

        if not selected_entries:
            QMessageBox.warning(self, "Ogohlantirish", "Sinxronlash uchun birorta ham tashkilot belgilanmadi!")
            return

        mod_count = sum(1 for x in selected_entries if x["status"] == "MODIFIED")
        new_count = sum(1 for x in selected_entries if x["status"] == "NEW")

        reply = QMessageBox.question(
            self, "Sinxronizatsiyani tasdiqlash",
            f"Tanlangan o'zgarishlarni tasdiqlaysizmi?\n\n"
            f"🟡 Yangilanadigan tashkilotlar: {mod_count} ta\n"
            f"🟢 Yangi qo'shiladigan tashkilotlar: {new_count} ta\n\n"
            f"(Amaldan oldin avtomatik zaxira nusxa yaratiladi)",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        if not self.app or not hasattr(self.app, "data_manager"):
            return

        # 1. Avtomatik zaxiralash
        try:
            self.app.data_manager.backup_data()
        except Exception as e:
            logger.warning(f"[MERGE] Zaxira olishda ogohlantirish: {e}")

        # 2. O'zgarishlarni qo'llash
        updated_records = 0
        added_records = 0

        for entry in selected_entries:
            st = entry["status"]
            it = entry["imported"]
            ex = entry.get("existing")

            if st == "MODIFIED" and ex:
                # Mavjud yozuvni yangilash
                old_f = ex.get("f", "")
                new_f = it.get("f", "")
                old_t = ex.get("t", "")
                new_t = it.get("t", "")

                ex.update(it)

                # Agar rahbar yoki telefon o'zgargan bo'lsa, kadrlar rotatsiyasi tarixiga yozish
                if (old_f and new_f and old_f != new_f) or (old_t and new_t and old_t != new_t):
                    if hasattr(self.app.data_manager, "sqlite"):
                        try:
                            self.app.data_manager.sqlite.add_staff_history(
                                org_id=ex.get("id", ""),
                                mahalla=ex.get("m", ""),
                                role=ex.get("lavozim") or ex.get("s", "Mas'ul"),
                                full_name=new_f or old_f,
                                phone=new_t or old_t,
                                inn=ex.get("inn", ""),
                                old_fio=old_f,
                                new_fio=new_f,
                                old_phone=old_t,
                                new_phone=new_t,
                                changed_by="EXCEL SMART MERGE",
                                reason="Excel orqali ommaviy sinxronlandi"
                            )
                        except Exception as e:
                            logger.error(f"[MERGE KADR LOG] {e}")

                updated_records += 1

            elif st == "NEW":
                # Yangi yozuv qo'shish
                self.app.data_manager.data.append(it)
                added_records += 1

        # 3. Bazani saqlash (SQLite + Atomic JSON)
        self.app.data_manager.save_data()
        if hasattr(self.app, "refresh_all_views"):
            self.app.refresh_all_views()

        msg = f"Sinxronizatsiya muvaffaqiyatli bajarildi! ✅\n\nYangilangan tashkilotlar: {updated_records} ta\nYangi kiritilganlar: {added_records} ta"
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"Sinxronlandi: {updated_records} yangilandi, {added_records} qo'shildi! ✅", "success")

        QMessageBox.information(self, "Muvaffaqiyatli", msg)
        self.accept()


def open_batch_import_dialog(app: Any) -> None:
    dlg = ImportDialog(parent=app, app=app)
    dlg.exec_()
