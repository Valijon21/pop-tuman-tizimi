"""
ui_qt.views.mahalla_passport_view: Mahalla 'Yettiligi' 360° Pasport oynasi (PyQt5).
7 ta mas'ul xodimning (Rais, Hokim yordamchisi, Yoshlar yetakchisi, Xotin-qizlar,
Profilaktika, Soliq inspektori, Ijtimoiy xodim) to'liq pasport kartasi va tezkor amallari.
"""
from typing import Optional, Dict, Any, List
import pyperclip
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QComboBox, QPushButton, QScrollArea, QWidget, QFrame,
    QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt
from services.verification_service import build_verification_text
from services.cabinet_service import build_cabinet_access_text
from ui_qt.views.qr_dialog import open_qr_dialog
from ui_qt.styles import get_stylesheet, hex_to_rgba
from core.logger import logger

ROLES_CONFIG = [
    ("Rais", "Mahalla Raisi", "👑", "#3b82f6"),
    ("Hokim yordamchisi", "Hokim Yordamchisi", "💼", "#10b981"),
    ("Yoshlar yetakchisi", "Yoshlar Yetakchisi", "🚀", "#8b5cf6"),
    ("Xotin-qizlar faoli", "Xotin-qizlar Faoli", "🌸", "#ec4899"),
    ("Profilaktika inspektori", "Profilaktika Inspektori", "👮", "#f59e0b"),
    ("Soliq inspektori", "Soliq Inspektori", "📊", "#06b6d4"),
    ("Ijtimoiy xodim", "Ijtimoiy Xodim (Inson)", "🤝", "#14b8a6"),
]

class MahallaPassportView(QDialog):
    """Mahalla Yettiligi 360 Pasport Oynasi."""

    def __init__(self, parent=None, app=None, selected_mahalla: Optional[str] = None):
        super().__init__(parent)
        self.app = app
        self.selected_mahalla = selected_mahalla
        self.current_theme = getattr(app, "current_theme", "dark")
        self.setWindowTitle("🏘 Mahalla 'Yettiligi' 360° Pasport Tizimi")
        self.resize(850, 540)
        self.setMinimumSize(700, 420)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        self.setup_ui()
        self.populate_mahallalar()
        if self.selected_mahalla:
            idx = self.combo_mahalla.findText(self.selected_mahalla)
            if idx >= 0:
                self.combo_mahalla.setCurrentIndex(idx)
            else:
                self.load_passport(self.selected_mahalla)
        else:
            if self.combo_mahalla.count() > 0:
                self.load_passport(self.combo_mahalla.currentText())

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(8)

        # Header Paneli
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        title = QLabel("🏘 Mahalla 'Yettiligi' 360° Raqamli Pasporti")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0284c7;" if is_light else "font-size: 15px; font-weight: 800; color: #38bdf8;")
        subtitle = QLabel("Pop tumani barcha mahallalarining 7 ta asosiy mas'ul xodimlari ma'lumotlar bazasi")
        subtitle.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)

        header.addStretch()

        # Mahalla tanlash
        select_box = QHBoxLayout()
        lbl = QLabel("Mahalla:")
        lbl.setStyleSheet(f"font-size: 11.5px; font-weight: 700; color: {'#0f172a' if is_light else '#f1f5f9'};")
        select_box.addWidget(lbl)

        self.combo_mahalla = QComboBox()
        self.combo_mahalla.setEditable(True)
        self.combo_mahalla.setMinimumWidth(200)
        self.combo_mahalla.setStyleSheet("""
            QComboBox { font-size: 12px; font-weight: 600; padding: 4px 8px; }
        """)
        self.combo_mahalla.currentTextChanged.connect(self.on_mahalla_changed)
        select_box.addWidget(self.combo_mahalla)
        header.addLayout(select_box)

        main_layout.addLayout(header)

        # Ajratuvchi chiziq
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {'#e2e8f0' if is_light else '#334155'}; margin: 4px 0px;")
        main_layout.addWidget(line)

        # Skroll maydoni kartalar uchun
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.cards_container = QWidget()
        self.cards_grid = QGridLayout(self.cards_container)
        self.cards_grid.setSpacing(16)
        self.cards_grid.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(self.cards_container)

        main_layout.addWidget(scroll, 1)

        # Pastki amallar
        footer = QHBoxLayout()
        self.lbl_stats = QLabel("Yuklanmoqda...")
        self.lbl_stats.setStyleSheet(f"font-size: 12px; color: {'#475569' if is_light else '#94a3b8'}; font-weight: 600;")
        footer.addWidget(self.lbl_stats)

        footer.addStretch()
        self.btn_close = QPushButton("Yopish")
        self.btn_close.clicked.connect(self.accept)
        footer.addWidget(self.btn_close)

        main_layout.addLayout(footer)

    def populate_mahallalar(self):
        """Tizimdagi barcha mahallalarni to'plash."""
        if not self.app or not hasattr(self.app, "data"):
            return
        mahallalar = set()
        for item in self.app.data:
            s_val = str(item.get("s", "")).strip()
            m_val = str(item.get("m", "")).strip()
            if "Mahalla" in s_val or "MFY" in s_val or "MFY" in m_val:
                mahallalar.add(m_val)

        sorted_m = sorted(list(mahallalar))
        self.combo_mahalla.blockSignals(True)
        self.combo_mahalla.clear()
        self.combo_mahalla.addItems(sorted_m)
        self.combo_mahalla.blockSignals(False)

    def on_mahalla_changed(self, text: str):
        if text.strip():
            self.load_passport(text.strip())

    def load_passport(self, mahalla_name: str):
        """Tanlangan mahalla uchun 7 ta kartani to'ldirish."""
        self.cards_container.setUpdatesEnabled(False)
        try:
            # Avvalgi kartalarni tozalash
            while self.cards_grid.count():
                item = self.cards_grid.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # Ma'lumotlarni qidirish
            all_items = [i for i in self.app.data if str(i.get("m", "")).strip().lower() == mahalla_name.lower()]
            main_item = all_items[0] if all_items else {"m": mahalla_name, "s": "Mahalla (MFY)"}

            filled_count = 0

            for idx, (role_key, role_title, icon, color) in enumerate(ROLES_CONFIG):
                # Rollarga mos xodimni aniqlash
                role_item = None
                rk = role_key.lower()
                for it in all_items:
                    s_val = str(it.get("s", "")).lower()
                    izoh = str(it.get("izoh", "")).lower()
                    lavozim = str(it.get("lavozim", "")).lower()
                    if (rk in s_val or rk in izoh or rk in lavozim or
                        (rk == "rais" and ("mahalla" in s_val or "rais" in izoh)) or
                        ("xotin" in rk and "xotin" in s_val) or
                        ("profilaktika" in rk and ("profilaktika" in s_val or "inspektor" in s_val)) or
                        ("soliq" in rk and "soliq" in s_val) or
                        ("ijtimoiy" in rk and "ijtimoiy" in s_val)):
                        role_item = it
                        break

                if not role_item:
                    if idx == 0:
                        role_item = main_item
                    else:
                        role_item = {
                            "m": mahalla_name,
                            "s": role_title,
                            "lavozim": role_title,
                            "inn": main_item.get("inn", ""),
                            "f": "",
                            "t": "",
                            "jshr": "",
                            "seriya": "",
                            "izoh": f"{mahalla_name} - {role_title}",
                            "_is_new": True
                        }

                fio = role_item.get("f", "") if role_item else ""
                phone = role_item.get("t", "") if role_item else ""
                inn = role_item.get("inn", "") if role_item else main_item.get("inn", "")
                jshr = role_item.get("jshr", "") if role_item else ""
                seriya = role_item.get("seriya", "") if role_item else ""

                if fio:
                    filled_count += 1

                card = self.create_role_card(
                    mahalla=mahalla_name,
                    role_key=role_key,
                    role_title=role_title,
                    icon=icon,
                    color=color,
                    fio=fio,
                    phone=phone,
                    inn=inn,
                    jshr=jshr,
                    seriya=seriya,
                    item=role_item
                )

                row = idx // 2
                col = idx % 2
                self.cards_grid.addWidget(card, row, col)

            self.lbl_stats.setText(f"Mahalla: {mahalla_name} | Yettilik to'liqligi: {filled_count}/7 ta xodim")
        finally:
            self.cards_container.setUpdatesEnabled(True)

    def create_role_card(self, mahalla, role_key, role_title, icon, color, fio, phone, inn, jshr, seriya, item):
        is_light = (self.current_theme == "light")
        card_bg = "#ffffff" if is_light else "#1e293b"
        card_border = "#e2e8f0" if is_light else "#334155"

        card = QFrame()
        card.setObjectName("mahalla_role_card")
        card.setStyleSheet(f"""
            QFrame#mahalla_role_card {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 8px;
            }}
            QFrame#mahalla_role_card:hover {{
                border: 1px solid {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Yuqori qism: Ikonka + Lavozim nomi
        top = QHBoxLayout()
        icon_bg = hex_to_rgba(color, 0.12 if is_light else 0.18)
        icon_border = hex_to_rgba(color, 0.25 if is_light else 0.35)
        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(30, 30)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 15px; background: {icon_bg}; border: 1px solid {icon_border}; border-radius: 6px;")
        top.addWidget(icon_lbl)

        role_lbl = QLabel(role_title)
        role_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {color};")
        top.addWidget(role_lbl)
        top.addStretch()

        status_txt = "✅ To'liq" if fio else "⚠️ Bo'sh"
        status_color = "#10b981" if fio else "#ef4444"
        status_bg = "#f1f5f9" if is_light else "#0f172a"
        status_lbl = QLabel(status_txt)
        status_lbl.setStyleSheet(f"font-size: 10px; font-weight: 700; color: {status_color}; background: {status_bg}; border-radius: 4px; padding: 1px 6px;")
        top.addWidget(status_lbl)
        layout.addLayout(top)

        # F.I.SH
        fio_color = "#0f172a" if is_light else "#ffffff"
        fio_muted = "#64748b" if is_light else "#94a3b8"
        fio_lbl = QLabel(f"👤 {fio if fio else 'Biriktirilmagan'}")
        fio_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {fio_color};" if fio else f"font-size: 11px; color: {fio_muted}; font-style: italic;")
        layout.addWidget(fio_lbl)

        # Ma'lumotlar qatori
        info_layout = QHBoxLayout()
        phone_txt = f"📞 {phone}" if phone else "📞 -"
        inn_txt = f"🆔 INN: {inn}" if inn else "🆔 -"
        meta_color = "#475569" if is_light else "#94a3b8"
        p_lbl = QLabel(phone_txt)
        p_lbl.setStyleSheet(f"font-size: 11px; color: {meta_color};")
        i_lbl = QLabel(inn_txt)
        i_lbl.setStyleSheet(f"font-size: 11px; color: {meta_color};")
        info_layout.addWidget(p_lbl)
        info_layout.addWidget(i_lbl)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        # JSHSHIR va Seriya
        pass_layout = QHBoxLayout()
        jshr_txt = f"🔢 JSHR: {jshr}" if jshr else "🔢 JSHR: -"
        ser_txt = f"📄 Seriya: {seriya}" if seriya else "📄 Seriya: -"
        sub_color = "#64748b" if is_light else "#94a3b8"
        j_lbl = QLabel(jshr_txt)
        j_lbl.setStyleSheet(f"font-size: 10px; color: {sub_color};")
        s_lbl = QLabel(ser_txt)
        s_lbl.setStyleSheet(f"font-size: 10px; color: {sub_color};")
        pass_layout.addWidget(j_lbl)
        pass_layout.addWidget(s_lbl)
        pass_layout.addStretch()
        layout.addLayout(pass_layout)

        # Tugmalar paneli
        btns = QHBoxLayout()
        btns.setSpacing(6)

        btn_verif = QPushButton("🛡 Verifikatsiya")
        btn_verif.setProperty("class", "btn_info")
        btn_verif.setCursor(Qt.PointingHandCursor)
        btn_verif.setStyleSheet("font-size: 11px; padding: 4px 8px; border-radius: 5px;")
        btn_verif.clicked.connect(lambda: self.copy_role_verif(mahalla, role_title, fio, inn, jshr, seriya))

        btn_cab = QPushButton("🔑 Kabinet")
        btn_cab.setProperty("class", "btn_warning")
        btn_cab.setCursor(Qt.PointingHandCursor)
        btn_cab.setStyleSheet("font-size: 11px; padding: 4px 8px; border-radius: 5px;")
        btn_cab.clicked.connect(lambda: self.copy_role_cabinet(mahalla, fio, inn))

        btn_qr = QPushButton("📱 QR")
        btn_qr.setProperty("class", "btn_purple")
        btn_qr.setCursor(Qt.PointingHandCursor)
        btn_qr.setStyleSheet("font-size: 11px; padding: 4px 8px; border-radius: 5px;")
        btn_qr.setToolTip(f"{role_title} ({fio or 'Masʼul'}) uchun mobil QR kod")
        btn_qr.clicked.connect(lambda _, m=mahalla, r=role_title, f=fio, p=phone, i=inn, it=item: open_qr_dialog(
            self.app,
            phone=p,
            org_name=f"{m} MFY",
            person_name=f,
            role=r,
            inn=i,
            item=it
        ))

        btn_edit = QPushButton("✏ Tahrir")
        btn_edit.setProperty("class", "btn_secondary")
        btn_edit.setCursor(Qt.PointingHandCursor)
        btn_edit.setStyleSheet("font-size: 11px; padding: 4px 8px; border-radius: 5px;")
        btn_edit.clicked.connect(lambda: self.edit_role_person(item, role_title))

        btns.addWidget(btn_verif)
        btns.addWidget(btn_cab)
        btns.addWidget(btn_qr)
        btns.addWidget(btn_edit)
        btns.addStretch()
        layout.addLayout(btns)

        return card

    def copy_role_verif(self, mahalla, role_title, fio, inn, jshr, seriya):
        text = (
            f"Tashkilot nomi: {mahalla}\n"
            f"INN:   {inn or '-'}\n"
            f"F.I.O:  {fio or '-'}\n"
            f"JSHR : {jshr or '-'}\n"
            f"Seriya : {seriya or '-'}\n"
            f"Lavozimi: {role_title}\n"
            f"verfikatsiya bervoring."
        )
        pyperclip.copy(text)
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"🛡 {role_title} verifikatsiya matni nusxalandi!", "success")
        else:
            QMessageBox.information(self, "OK", f"{role_title} verifikatsiya matni nusxalandi!")

    def copy_role_cabinet(self, mahalla, fio, inn):
        text = (
            f"Tashkilot nomi: {mahalla}\n"
            f"INN:   {inn or '-'}\n"
            f"F.I.O:  {fio or '-'}\n"
            f"cabinetga dostup"
        )
        pyperclip.copy(text)
        if hasattr(self.app, "show_toast"):
            self.app.show_toast(f"🔑 {mahalla} kabinet matni nusxalandi!", "success")
        else:
            QMessageBox.information(self, "OK", "Kabinetga dostup matni nusxalandi!")

    def edit_role_person(self, item, role_title):
        from ui_qt.views.org_edit_dialog import OrgEditDialog
        dlg = OrgEditDialog(parent=self, app=self.app, item=item)
        if dlg.exec_() == QDialog.Accepted:
            if hasattr(self.app, "refresh_all_views"):
                self.app.refresh_all_views()
            self.load_passport(self.combo_mahalla.currentText())

def open_mahalla_passport(app: Any, mahalla: Optional[str] = None) -> None:
    dlg = MahallaPassportView(parent=app, app=app, selected_mahalla=mahalla)
    dlg.exec_()
