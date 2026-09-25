"""
ui_qt.views.qr_dialog: Telefon raqami va tashkilot ma'lumotlari uchun zamonaviy PyQt5 QR-kod oynasi.
High-DPI qo'llab-quvvatlash, xotirada tezkor generatsiya, vCard raqamli kontakt va PNG eksport.
"""
from typing import Optional, Dict, Any
from io import BytesIO
import pyperclip
from PIL import Image

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QMessageBox, QFileDialog, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

from services.qr_service import (
    clean_phone_number,
    generate_phone_qr_image,
    generate_vcard_qr_image,
    generate_mecard_qr_image
)
from ui_qt.styles import get_stylesheet
from core.logger import logger


def pil_to_qpixmap(pil_img: Image.Image) -> QPixmap:
    """PIL Image ob'ektini PyQt5 QPixmap tasviriga xotirada tezkor aylantirish."""
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    qimg = QImage()
    qimg.loadFromData(buffer.getvalue())
    return QPixmap.fromImage(qimg)


class QRDialog(QDialog):
    """Telefon raqami va tashkilot kontakti uchun professional QR-Kod Dialogi."""

    def __init__(
        self,
        parent=None,
        app=None,
        phone: str = "",
        org_name: str = "",
        person_name: str = "",
        role: str = "",
        inn: str = "",
        item: Optional[Dict[str, Any]] = None
    ):
        super().__init__(parent)
        self.app = app
        self.current_theme = getattr(app, "current_theme", "dark")
        self.setWindowTitle("📱 QR Kod — Mobil Kontakt & Qo'ng'iroq")
        self.resize(400, 540)
        self.setMinimumSize(360, 500)
        self.setStyleSheet(get_stylesheet(self.current_theme))

        # Ma'lumotlarni to'ldirish
        if item:
            self.org_name = org_name or str(item.get("m", "")).strip()
            self.person_name = person_name or str(item.get("f", "")).strip()
            self.role = role or str(item.get("s", "") or item.get("lavozim", "")).strip()
            self.phone = phone or str(item.get("t", "")).strip()
            self.inn = inn or str(item.get("inn", "")).strip()
        else:
            self.org_name = org_name.strip()
            self.person_name = person_name.strip()
            self.role = role.strip()
            self.phone = phone.strip()
            self.inn = inn.strip()

        self.clean_tel = clean_phone_number(self.phone)
        self.current_mode = "tel"  # 'tel', 'mecard' yoki 'vcard'
        self.current_pil_img: Optional[Image.Image] = None

        self.setup_ui()
        self.update_qr()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        bg_card = "#ffffff" if is_light else "#1e293b"
        border_col = "#e2e8f0" if is_light else "#334155"
        text_title = "#0f172a" if is_light else "#f8fafc"
        text_muted = "#64748b" if is_light else "#94a3b8"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(10)

        # 1. Sarlavha
        head_box = QVBoxLayout()
        head_box.setSpacing(2)
        title_lbl = QLabel("📱 Mobil QR Kod")
        title_lbl.setStyleSheet(f"font-size: 15px; font-weight: 800; color: {text_title};")
        sub_lbl = QLabel("Telefoningiz kamerasi orqali skaner qiling")
        sub_lbl.setStyleSheet(f"font-size: 11px; color: {text_muted};")
        head_box.addWidget(title_lbl, alignment=Qt.AlignCenter)
        head_box.addWidget(sub_lbl, alignment=Qt.AlignCenter)
        layout.addLayout(head_box)

        # 2. Rejim tanlash (Radio tugmalar)
        mode_box = QHBoxLayout()
        mode_box.setSpacing(8)
        mode_box.setAlignment(Qt.AlignCenter)

        self.btn_grp = QButtonGroup(self)
        self.rad_tel = QRadioButton("📞 Qo'ng'iroq")
        self.rad_mecard = QRadioButton("📱 MeCard")
        self.rad_vcard = QRadioButton("📇 vCard")
        self.rad_tel.setChecked(True)

        self.btn_grp.addButton(self.rad_tel)
        self.btn_grp.addButton(self.rad_mecard)
        self.btn_grp.addButton(self.rad_vcard)
        self.rad_tel.toggled.connect(self._on_mode_toggled)
        self.rad_mecard.toggled.connect(self._on_mode_toggled)
        self.rad_vcard.toggled.connect(self._on_mode_toggled)

        rad_style = f"""
            QRadioButton {{
                font-size: 11px;
                font-weight: 700;
                color: {'#1e293b' if is_light else '#e2e8f0'};
            }}
        """
        self.rad_tel.setStyleSheet(rad_style)
        self.rad_mecard.setStyleSheet(rad_style)
        self.rad_vcard.setStyleSheet(rad_style)

        mode_box.addWidget(self.rad_tel)
        mode_box.addWidget(self.rad_mecard)
        mode_box.addWidget(self.rad_vcard)
        layout.addLayout(mode_box)

        # 3. QR Tasvir Konteyneri
        self.qr_frame = QFrame()
        self.qr_frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {border_col};
                border-radius: 12px;
                padding: 10px;
            }}
        """)
        qr_layout = QVBoxLayout(self.qr_frame)
        qr_layout.setContentsMargins(8, 8, 8, 8)
        qr_layout.setSpacing(4)

        self.lbl_qr_image = QLabel()
        self.lbl_qr_image.setAlignment(Qt.AlignCenter)
        self.lbl_qr_image.setFixedSize(220, 220)
        qr_layout.addWidget(self.lbl_qr_image, alignment=Qt.AlignCenter)

        self.lbl_tip = QLabel("✅ Toza xalqaro format — 835 raqami qo'shilmaydi")
        self.lbl_tip.setStyleSheet("font-size: 10px; color: #059669; font-weight: 700;")
        self.lbl_tip.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(self.lbl_tip)

        layout.addWidget(self.qr_frame, alignment=Qt.AlignCenter)

        # 4. Ma'lumotlar kartochkasi
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_card};
                border: 1px solid {border_col};
                border-radius: 8px;
                padding: 6px 10px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 6, 8, 6)
        info_layout.setSpacing(3)

        if self.org_name:
            lbl_org = QLabel(f"🏢 {self.org_name}")
            lbl_org.setStyleSheet(f"font-size: 11.5px; font-weight: 700; color: {text_title};")
            lbl_org.setWordWrap(True)
            info_layout.addWidget(lbl_org)

        if self.person_name:
            lbl_person = QLabel(f"👤 {self.person_name} ({self.role or 'Mas’ul'})")
            lbl_person.setStyleSheet(f"font-size: 11px; color: {text_muted};")
            lbl_person.setWordWrap(True)
            info_layout.addWidget(lbl_person)

        self.lbl_phone = QLabel(f"📞 {self.clean_tel or 'Telefon kiritilmagan'}")
        self.lbl_phone.setStyleSheet("font-size: 13px; font-weight: 800; color: #10b981;")
        info_layout.addWidget(self.lbl_phone)

        if self.inn:
            lbl_inn = QLabel(f"🆔 INN: {self.inn}")
            lbl_inn.setStyleSheet(f"font-size: 10px; color: {text_muted};")
            info_layout.addWidget(lbl_inn)

        layout.addWidget(info_frame)

        # 5. Harakatlar tugmalari
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        btn_copy = QPushButton("📋 Nusxalash")
        btn_copy.setProperty("class", "btn_primary")
        btn_copy.setCursor(Qt.PointingHandCursor)
        btn_copy.clicked.connect(self.copy_phone)
        btn_layout.addWidget(btn_copy)

        btn_save = QPushButton("💾 Saqlash (.png)")
        btn_save.setProperty("class", "btn_success")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_qr_image)
        btn_layout.addWidget(btn_save)

        btn_close = QPushButton("Yopish")
        btn_close.setProperty("class", "btn_secondary")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

    def _on_mode_toggled(self, checked: bool):
        if self.rad_tel.isChecked():
            self.current_mode = "tel"
            self.lbl_tip.setText("✅ Toza xalqaro format (+998...) — 835 vanity xatosi bo'lmaydi")
        elif hasattr(self, "rad_mecard") and self.rad_mecard.isChecked():
            self.current_mode = "mecard"
            self.lbl_tip.setText("📱 MeCard — barcha mobil kameralar uchun universal kontakt")
        else:
            self.current_mode = "vcard"
            self.lbl_tip.setText("📇 vCard 3.0 — RFC 2426 xalqaro standartidagi kontakt")
        self.update_qr()

    def update_qr(self):
        """QR kod tasvirini joriy rejim bo'yicha qayta chizish."""
        if not self.clean_tel and not self.org_name:
            self.lbl_qr_image.setText("QR kod uchun ma'lumot yetarli emas")
            return

        try:
            if self.current_mode == "vcard":
                self.current_pil_img = generate_vcard_qr_image(
                    name=self.person_name,
                    phone=self.clean_tel or self.phone,
                    org=self.org_name,
                    title=self.role,
                    inn=self.inn,
                    size=220
                )
            elif self.current_mode == "mecard":
                self.current_pil_img = generate_mecard_qr_image(
                    name=self.person_name,
                    phone=self.clean_tel or self.phone,
                    org=self.org_name,
                    title=self.role,
                    inn=self.inn,
                    size=220
                )
            else:
                target_phone = self.clean_tel or self.phone
                self.current_pil_img = generate_phone_qr_image(target_phone, size=220, as_uri=False)

            pix = pil_to_qpixmap(self.current_pil_img)
            self.lbl_qr_image.setPixmap(pix)
        except Exception as e:
            logger.error(f"[QR] Generatsiya xatosi: {e}")
            self.lbl_qr_image.setText("QR kod yaratishda xatolik")

    def copy_phone(self):
        val = self.clean_tel or self.phone
        if val:
            pyperclip.copy(val)
            if hasattr(self.app, "show_toast"):
                self.app.show_toast(f"Telefon raqami ({val}) nusxalandi! 📋", "success")
            else:
                QMessageBox.information(self, "Nusxalandi", f"Telefon raqami ({val}) xotiraga nusxalandi!")

    def save_qr_image(self):
        """QR-kod rasmini PNG fayl qilib saqlash."""
        if not self.current_pil_img:
            return

        def_name = f"QR_{self.org_name or self.clean_tel or 'telefon'}_{self.current_mode}.png"
        clean_filename = "".join(c for c in def_name if c.isalnum() or c in (" ", ".", "_", "-")).strip()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "QR Kod Tasvirini Saqlash",
            clean_filename,
            "PNG Tasvirlar (*.png);;Barcha fayllar (*.*)"
        )
        if file_path:
            try:
                # O'lchamini kattaroq (500x500) qilib saqlash
                if self.current_mode == "vcard":
                    export_img = generate_vcard_qr_image(
                        name=self.person_name,
                        phone=self.clean_tel or self.phone,
                        org=self.org_name,
                        title=self.role,
                        inn=self.inn,
                        size=500
                    )
                elif self.current_mode == "mecard":
                    export_img = generate_mecard_qr_image(
                        name=self.person_name,
                        phone=self.clean_tel or self.phone,
                        org=self.org_name,
                        title=self.role,
                        inn=self.inn,
                        size=500
                    )
                else:
                    export_img = generate_phone_qr_image(self.clean_tel or self.phone, size=500, as_uri=False)

                export_img.save(file_path, format="PNG")
                if hasattr(self.app, "show_toast"):
                    self.app.show_toast("QR-kod tasviri saqlandi! 💾", "success")
                QMessageBox.information(self, "Saqlandi", f"QR-kod tasviri muvaffaqiyatli saqlandi:\n{file_path}")
            except Exception as e:
                logger.error(f"[QR SAQLASH] Xatolik: {e}")
                QMessageBox.critical(self, "Xatolik", f"Tasvirni saqlashda xatolik yuz berdi:\n{e}")


def open_qr_dialog(
    app: Any,
    item: Optional[Dict[str, Any]] = None,
    phone: str = "",
    org_name: str = "",
    person_name: str = "",
    role: str = "",
    inn: str = ""
) -> None:
    """Ilova oynasida QR dialogini xavfsiz ochish."""
    dlg = QRDialog(
        parent=app,
        app=app,
        phone=phone,
        org_name=org_name,
        person_name=person_name,
        role=role,
        inn=inn,
        item=item
    )
    dlg.exec_()
