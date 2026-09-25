"""
ui_qt.views.apps_view: Yordamchi va Kommunal Dasturlar (Utilities & Tools) Sahifasi (PyQt5).
UzCrypto (E-IMZO) va AnyDesk dasturlarini professional boshqarish, ishga tushirish, buferga nusxalash (Ctrl+V) va monitoring qilish.
"""
import os
import sys
import platform
import subprocess
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QUrl, QMimeData

from core.config import UZCRYPTO_PATH, ANYDESK_PATH, BASE_DIR
from core.logger import logger


def copy_file_to_windows_clipboard(file_path: str) -> bool:
    """
    Faylni Windows tizim buferiga (Clipboard) to'g'ridan-to'g'ri nusxalash (CF_HDROP).
    Foydalanuvchi istalgan papka, Ish stoli (Desktop) yoki fleshkaga borib
    Ctrl + V (yoki sichqonchaning o'ng tugmasi -> 'Vstavit / Paste') bosganda
    haqiqiy EXE faylining o'zi nusxalanib joylashadi.
    """
    if not os.path.exists(file_path):
        return False

    abs_path = os.path.abspath(file_path).replace("/", "\\")

    # 1. Qt Clipboard (QMimeData orqali cross-platform va Qt ichki dasturlari uchun)
    try:
        mime = QMimeData()
        mime.setUrls([QUrl.fromLocalFile(abs_path)])
        mime.setText(abs_path)
        QApplication.clipboard().setMimeData(mime)
    except Exception as e:
        logger.warning(f"[CLIPBOARD] Qt setMimeData xatolik: {e}")

    # 2. Windows Native CF_HDROP (Windows Explorer da Ctrl+V to'liq ishlashi uchun)
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
        kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
        kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalUnlock.restype = wintypes.BOOL
        kernel32.GlobalFree.argtypes = [wintypes.HGLOBAL]
        kernel32.GlobalFree.restype = wintypes.HGLOBAL

        user32.OpenClipboard.argtypes = [wintypes.HWND]
        user32.OpenClipboard.restype = wintypes.BOOL
        user32.EmptyClipboard.argtypes = []
        user32.EmptyClipboard.restype = wintypes.BOOL
        user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
        user32.SetClipboardData.restype = wintypes.HANDLE
        user32.CloseClipboard.argtypes = []
        user32.CloseClipboard.restype = wintypes.BOOL

        file_bytes = (abs_path + "\0\0").encode("utf-16le")
        offset = 20
        total_size = offset + len(file_bytes)

        GMEM_MOVEABLE = 0x0002
        GMEM_ZEROINIT = 0x0040
        GHND = GMEM_MOVEABLE | GMEM_ZEROINIT

        h_global = kernel32.GlobalAlloc(GHND, total_size)
        if h_global:
            p_global = kernel32.GlobalLock(h_global)
            if p_global:
                header = bytearray(20)
                header[0:4] = (20).to_bytes(4, "little")  # pFiles offset
                header[16:20] = (1).to_bytes(4, "little")  # fWide = TRUE (Unicode)
                ctypes.memmove(p_global, bytes(header), 20)
                ctypes.memmove(p_global + 20, file_bytes, len(file_bytes))
                kernel32.GlobalUnlock(h_global)

                if user32.OpenClipboard(0):
                    user32.EmptyClipboard()
                    CF_HDROP = 15
                    user32.SetClipboardData(CF_HDROP, h_global)
                    user32.CloseClipboard()
                    logger.info(f"[CLIPBOARD] Fayl Windows buferiga nusxalandi: {abs_path}")
                    return True
                else:
                    kernel32.GlobalFree(h_global)
    except Exception as e:
        logger.warning(f"[CLIPBOARD] Win32 CF_HDROP xatolik: {e}")

    return True


class AppsView(QWidget):
    """Yordamchi va Kommunal Dasturlar ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_theme = getattr(app, "current_theme", "dark")
        self.setup_ui()
        self.refresh_status()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(12)

        # 1. HEADER (Sarlavha qismi)
        head_layout = QVBoxLayout()
        head_layout.setSpacing(3)

        self.title_lbl = QLabel("💻 Yordamchi va Kommunal Dasturlar (Utilities & Tools)")
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8;")
        self.sub_lbl = QLabel(
            "Pop tumani korxona va tashkilotlari bilan ishlash, E-IMZO raqamli imzo drayverlari va tezkor masofaviy texnik yordam vositalari"
        )
        self.sub_lbl.setStyleSheet("font-size: 11.5px; color: #94a3b8;")

        head_layout.addWidget(self.title_lbl)
        head_layout.addWidget(self.sub_lbl)
        main_layout.addLayout(head_layout)

        # 2. SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        self.c_layout = QVBoxLayout(container)
        self.c_layout.setSpacing(14)
        self.c_layout.setContentsMargins(0, 0, 4, 10)

        # 3. TIZIM STATUSI BANNERI
        self.sys_banner = QFrame()
        self.sys_banner.setProperty("class", "info_card")
        self.sys_banner.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 8px;
                padding: 10px 14px;
            }
        """)
        b_layout = QHBoxLayout(self.sys_banner)
        b_layout.setContentsMargins(10, 8, 10, 8)
        b_layout.setSpacing(16)

        # OS info
        os_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
        self.lbl_os_info = QLabel(f"🖥 <b>Operatsion tizim:</b> {os_info} | <b>Arxitektura:</b> 64-bit / 32-bit mos | <b>GUI:</b> PyQt5 PRO")
        self.lbl_os_info.setStyleSheet("color: #cbd5e1; font-size: 11.5px;")
        b_layout.addWidget(self.lbl_os_info)

        b_layout.addStretch()

        btn_refresh = QPushButton("🔄 Holatni Yangilash")
        btn_refresh.setProperty("class", "btn_secondary")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.clicked.connect(self.refresh_status)
        b_layout.addWidget(btn_refresh)

        self.c_layout.addWidget(self.sys_banner)

        # 4. KARTALAR GRIDI (UzCrypto & AnyDesk)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)

        # --- KARTA 1: UZCRYPTO (E-IMZO) ---
        self.card_uzcrypto = self._create_uzcrypto_card()
        cards_layout.addWidget(self.card_uzcrypto, 1)

        # --- KARTA 2: ANYDESK ---
        self.card_anydesk = self._create_anydesk_card()
        cards_layout.addWidget(self.card_anydesk, 1)

        self.c_layout.addLayout(cards_layout)

        # 5. QO'LLANMA VA YO'RIQNOMA KARTASI (FAQ / Quick Guide)
        self.card_guide = self._create_guide_card()
        self.c_layout.addWidget(self.card_guide)

        self.c_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _create_uzcrypto_card(self) -> QFrame:
        """UzCrypto (E-IMZO) dasturi uchun karta vidjeti."""
        card = QFrame()
        card.setProperty("class", "clickable_card")
        card.setStyleSheet("""
            QFrame {
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid rgba(56, 189, 248, 0.28);
                border-radius: 10px;
            }
            QFrame:hover {
                border: 1px solid rgba(56, 189, 248, 0.6);
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Header: Icon & Badge
        h_row = QHBoxLayout()
        icon_lbl = QLabel("🔐")
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent; padding: 2px;")
        h_row.addWidget(icon_lbl)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        c_title = QLabel("UzCrypto (E-IMZO)")
        c_title.setStyleSheet("font-size: 14.5px; font-weight: 800; color: #38bdf8;")
        c_sub = QLabel("Raqamli Imzo va ERI Kriptografik Moduli")
        c_sub.setStyleSheet("font-size: 11px; color: #94a3b8; font-weight: 600;")
        title_box.addWidget(c_title)
        title_box.addWidget(c_sub)
        h_row.addLayout(title_box)

        h_row.addStretch()

        self.lbl_uzcrypto_badge = QLabel("v2.2.3.41-x32")
        self.lbl_uzcrypto_badge.setStyleSheet("""
            background: rgba(14, 165, 233, 0.15);
            border: 1px solid rgba(14, 165, 233, 0.4);
            color: #38bdf8;
            font-size: 10.5px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 12px;
        """)
        h_row.addWidget(self.lbl_uzcrypto_badge)
        layout.addLayout(h_row)

        # Description
        desc = QLabel(
            "O'zbekiston Respublikasi Davlat Soliq Qo'mitasi (soliq.uz), Didox (didox.uz), Yagona Portali (my.gov.uz) "
            "hamda davlat xizmatlarida tashkilotning elektron raqamli imzo (ERI) kalitlari bilan ishlash va hujjatlarni "
            "tasdiqlash uchun zarur bo'lgan rasmiy kriptografik modul va drayver."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #cbd5e1; font-size: 11.5px; line-height: 1.4;")
        layout.addWidget(desc)

        # File specs
        spec_box = QFrame()
        spec_box.setStyleSheet("background: rgba(30, 41, 59, 0.5); border-radius: 6px; padding: 6px 10px;")
        sb_layout = QVBoxLayout(spec_box)
        sb_layout.setContentsMargins(6, 6, 6, 6)
        sb_layout.setSpacing(4)

        self.lbl_uzcrypto_status = QLabel("Holat: Aniqlanmoqda...")
        self.lbl_uzcrypto_status.setStyleSheet("font-size: 11px; font-weight: 700; color: #10b981;")
        self.lbl_uzcrypto_file = QLabel("Fayl: uzcrypto-2.2.3.41-x32-setup.exe")
        self.lbl_uzcrypto_file.setStyleSheet("font-size: 10.5px; color: #94a3b8;")
        self.lbl_uzcrypto_size = QLabel("Hajmi: 14.5 MB (14,556,569 bayt)")
        self.lbl_uzcrypto_size.setStyleSheet("font-size: 10.5px; color: #94a3b8;")
        self.lbl_uzcrypto_portals = QLabel("Portallar: soliq.uz, didox.uz, my.gov.uz, e-imzo.uz")
        self.lbl_uzcrypto_portals.setStyleSheet("font-size: 10.5px; color: #38bdf8;")

        sb_layout.addWidget(self.lbl_uzcrypto_status)
        sb_layout.addWidget(self.lbl_uzcrypto_file)
        sb_layout.addWidget(self.lbl_uzcrypto_size)
        sb_layout.addWidget(self.lbl_uzcrypto_portals)
        layout.addWidget(spec_box)

        # Action Buttons (O'rnatish, Kopiya, Papkani ochish)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_run_uzcrypto = QPushButton("▶ O'rnatishni boshlash (Setup)")
        self.btn_run_uzcrypto.setProperty("class", "btn_success")
        self.btn_run_uzcrypto.setCursor(Qt.PointingHandCursor)
        self.btn_run_uzcrypto.setStyleSheet("font-weight: 700; padding: 7px 12px;")
        self.btn_run_uzcrypto.clicked.connect(self.launch_uzcrypto)
        btn_layout.addWidget(self.btn_run_uzcrypto, 2)

        self.btn_copy_uzcrypto = QPushButton("📋 Nusxa olish (Kopiya)")
        self.btn_copy_uzcrypto.setProperty("class", "btn_primary")
        self.btn_copy_uzcrypto.setCursor(Qt.PointingHandCursor)
        self.btn_copy_uzcrypto.setToolTip("UzCrypto faylini buferga nusxalash (Istalgan papkada Ctrl+V bosib joylash uchun)")
        self.btn_copy_uzcrypto.setStyleSheet("font-weight: 600; padding: 7px 10px;")
        self.btn_copy_uzcrypto.clicked.connect(self.copy_uzcrypto_file)
        btn_layout.addWidget(self.btn_copy_uzcrypto, 2)

        self.btn_folder_uzcrypto = QPushButton("📁 Papkani ochish")
        self.btn_folder_uzcrypto.setProperty("class", "btn_secondary")
        self.btn_folder_uzcrypto.setCursor(Qt.PointingHandCursor)
        self.btn_folder_uzcrypto.setStyleSheet("font-weight: 600; padding: 7px 10px;")
        self.btn_folder_uzcrypto.clicked.connect(self.open_uzcrypto_folder)
        btn_layout.addWidget(self.btn_folder_uzcrypto, 1)

        layout.addLayout(btn_layout)
        return card

    def _create_anydesk_card(self) -> QFrame:
        """AnyDesk (Masofaviy Texnik Yordam) dasturi uchun karta vidjeti."""
        card = QFrame()
        card.setProperty("class", "clickable_card")
        card.setStyleSheet("""
            QFrame {
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid rgba(244, 63, 94, 0.28);
                border-radius: 10px;
            }
            QFrame:hover {
                border: 1px solid rgba(244, 63, 94, 0.6);
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Header: Icon & Badge
        h_row = QHBoxLayout()
        icon_lbl = QLabel("⚡")
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent; padding: 2px;")
        h_row.addWidget(icon_lbl)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        c_title = QLabel("AnyDesk (Masofaviy Yordam)")
        c_title.setStyleSheet("font-size: 14.5px; font-weight: 800; color: #f43f5e;")
        c_sub = QLabel("Tezkor Masofaviy Boshqaruv va Texnik Qo'llab-quvvatlash")
        c_sub.setStyleSheet("font-size: 11px; color: #94a3b8; font-weight: 600;")
        title_box.addWidget(c_title)
        title_box.addWidget(c_sub)
        h_row.addLayout(title_box)

        h_row.addStretch()

        self.lbl_anydesk_badge = QLabel("Portativ Versiya")
        self.lbl_anydesk_badge.setStyleSheet("""
            background: rgba(244, 63, 94, 0.15);
            border: 1px solid rgba(244, 63, 94, 0.4);
            color: #fb7185;
            font-size: 10.5px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 12px;
        """)
        h_row.addWidget(self.lbl_anydesk_badge)
        layout.addLayout(h_row)

        # Description
        desc = QLabel(
            "Tizim administratorlari va texnik yordam mutaxassislari bilan tezkor bog'lanish, dastur sozlamalari, "
            "baza sinxronizatsiyasi yoki yuzaga kelgan nosozliklarni real vaqt rejimida masofadan xavfsiz bartaraf etish "
            "dasturi. O'rnatish talab etilmaydi, portativ va darhol ishga tushadi."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #cbd5e1; font-size: 11.5px; line-height: 1.4;")
        layout.addWidget(desc)

        # File specs
        spec_box = QFrame()
        spec_box.setStyleSheet("background: rgba(30, 41, 59, 0.5); border-radius: 6px; padding: 6px 10px;")
        sb_layout = QVBoxLayout(spec_box)
        sb_layout.setContentsMargins(6, 6, 6, 6)
        sb_layout.setSpacing(4)

        self.lbl_anydesk_status = QLabel("Holat: Aniqlanmoqda...")
        self.lbl_anydesk_status.setStyleSheet("font-size: 11px; font-weight: 700; color: #10b981;")
        self.lbl_anydesk_file = QLabel("Fayl: AnyDesk.exe")
        self.lbl_anydesk_file.setStyleSheet("font-size: 10.5px; color: #94a3b8;")
        self.lbl_anydesk_size = QLabel("Hajmi: 3.67 MB (3,670,480 bayt)")
        self.lbl_anydesk_size.setStyleSheet("font-size: 10.5px; color: #94a3b8;")
        self.lbl_anydesk_feature = QLabel("Xususiyat: Shifrlangan TLS 1.2 aloqa, Tezkor 9-xonali ID")
        self.lbl_anydesk_feature.setStyleSheet("font-size: 10.5px; color: #fb7185;")

        sb_layout.addWidget(self.lbl_anydesk_status)
        sb_layout.addWidget(self.lbl_anydesk_file)
        sb_layout.addWidget(self.lbl_anydesk_size)
        sb_layout.addWidget(self.lbl_anydesk_feature)
        layout.addWidget(spec_box)

        # Action Buttons (Ishga tushirish, Kopiya, Papkani ochish)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_run_anydesk = QPushButton("🚀 AnyDesk ni ishga tushirish (Run)")
        self.btn_run_anydesk.setProperty("class", "btn_primary")
        self.btn_run_anydesk.setCursor(Qt.PointingHandCursor)
        self.btn_run_anydesk.setStyleSheet("font-weight: 700; padding: 7px 12px;")
        self.btn_run_anydesk.clicked.connect(self.launch_anydesk)
        btn_layout.addWidget(self.btn_run_anydesk, 2)

        self.btn_copy_anydesk = QPushButton("📋 Nusxa olish (Kopiya)")
        self.btn_copy_anydesk.setProperty("class", "btn_secondary")
        self.btn_copy_anydesk.setCursor(Qt.PointingHandCursor)
        self.btn_copy_anydesk.setToolTip("AnyDesk faylini buferga nusxalash (Istalgan papkada Ctrl+V bosib joylash uchun)")
        self.btn_copy_anydesk.setStyleSheet("font-weight: 600; padding: 7px 10px;")
        self.btn_copy_anydesk.clicked.connect(self.copy_anydesk_file)
        btn_layout.addWidget(self.btn_copy_anydesk, 2)

        self.btn_folder_anydesk = QPushButton("📁 Papkani ochish")
        self.btn_folder_anydesk.setProperty("class", "btn_secondary")
        self.btn_folder_anydesk.setCursor(Qt.PointingHandCursor)
        self.btn_folder_anydesk.setStyleSheet("font-weight: 600; padding: 7px 10px;")
        self.btn_folder_anydesk.clicked.connect(self.open_anydesk_folder)
        btn_layout.addWidget(self.btn_folder_anydesk, 1)

        layout.addLayout(btn_layout)
        return card

    def _create_guide_card(self) -> QFrame:
        """Yo'riqnoma va tezkor eslatmalar kartasi."""
        card = QFrame()
        card.setProperty("class", "info_card")
        card.setStyleSheet("""
            QFrame {
                background: rgba(30, 41, 59, 0.4);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 12px 14px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        g_title = QLabel("💡 Qo'llanma va Muhim Foydali Eslatmalar")
        g_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #f59e0b;")
        layout.addWidget(g_title)

        tips = [
            "<b>1. E-IMZO / UzCrypto o'rnatish:</b> Setup tugmasini bosganingizdan so'ng chiqqan oynada 'Далее' tugmalarini ketma-ket bosing. O'rnatish tugagach tizim patnisida (tray) E-IMZO doimiy faol bo'lib turadi.",
            "<b>2. Fayldan nusxa olish (Ctrl+V):</b> '📋 Nusxa olish (Kopiya)' tugmasini bosganingizda dastur to'g'ridan-to'g'ri Windows buferiga olinadi. Istalgan papkaga, Ish stoli (Desktop) yoki Telegramga o'tib Ctrl+V (yoki Paste) tugmasini bosing.",
            "<b>3. AnyDesk orqali ulanish:</b> AnyDesk oynasi ochilganda 'Ushbu ish stoli (This Desk)' ostidagi 9 xonali identifikator raqamini dasturchiga taqdim eting va ulanish so'rovi kelganda 'Ruxsat berish (Accept)' tugmasini bosing.",
            "<b>4. Xavfsizlik kafolati:</b> Barcha dasturlar rasmiy sertifikatlangan bo'lib, tashkilot ma'lumotlar bazasi va shaxsiy ma'lumotlarning butunligiga to'liq kafolat beriladi."
        ]

        for tip in tips:
            lbl = QLabel(tip)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 11px; color: #cbd5e1; line-height: 1.35;")
            layout.addWidget(lbl)

        return card

    def refresh_status(self):
        """Fayllarning mavjudligi va hajmini tekshirish."""
        # 1. UzCrypto
        if os.path.exists(UZCRYPTO_PATH):
            size_bytes = os.path.getsize(UZCRYPTO_PATH)
            mb = size_bytes / (1024 * 1024)
            self.lbl_uzcrypto_status.setText("🟢 O'rnatishga tayyor (Mavjud)")
            self.lbl_uzcrypto_status.setStyleSheet("font-size: 11px; font-weight: 700; color: #10b981;")
            self.lbl_uzcrypto_size.setText(f"Hajmi: {mb:.2f} MB ({size_bytes:,} bayt)")
            self.btn_run_uzcrypto.setEnabled(True)
            self.btn_copy_uzcrypto.setEnabled(True)
            self.btn_folder_uzcrypto.setEnabled(True)
        else:
            self.lbl_uzcrypto_status.setText("🔴 Fayl topilmadi!")
            self.lbl_uzcrypto_status.setStyleSheet("font-size: 11px; font-weight: 700; color: #ef4444;")
            self.btn_run_uzcrypto.setEnabled(False)
            self.btn_copy_uzcrypto.setEnabled(False)

        # 2. AnyDesk
        if os.path.exists(ANYDESK_PATH):
            size_bytes = os.path.getsize(ANYDESK_PATH)
            mb = size_bytes / (1024 * 1024)
            self.lbl_anydesk_status.setText("🟢 Ishga tushirishga tayyor (Mavjud)")
            self.lbl_anydesk_status.setStyleSheet("font-size: 11px; font-weight: 700; color: #10b981;")
            self.lbl_anydesk_size.setText(f"Hajmi: {mb:.2f} MB ({size_bytes:,} bayt)")
            self.btn_run_anydesk.setEnabled(True)
            self.btn_copy_anydesk.setEnabled(True)
            self.btn_folder_anydesk.setEnabled(True)
        else:
            self.lbl_anydesk_status.setText("🔴 Fayl topilmadi!")
            self.lbl_anydesk_status.setStyleSheet("font-size: 11px; font-weight: 700; color: #ef4444;")
            self.btn_run_anydesk.setEnabled(False)
            self.btn_copy_anydesk.setEnabled(False)

    def launch_uzcrypto(self):
        """UzCrypto o'rnatish dasturini ishga tushirish."""
        if not os.path.exists(UZCRYPTO_PATH):
            QMessageBox.warning(
                self,
                "Fayl Topilmadi",
                f"UzCrypto o'rnatish fayli quyidagi manzilda topilmadi:\n{UZCRYPTO_PATH}\n\nFaylni loyiha papkasiga joylashtiring."
            )
            return

        try:
            logger.info(f"[APPS] UzCrypto o'rnatish boshlanmoqda: {UZCRYPTO_PATH}")
            if hasattr(os, "startfile"):
                os.startfile(UZCRYPTO_PATH)
            else:
                subprocess.Popen([UZCRYPTO_PATH], shell=False)

            if self.app and hasattr(self.app, "show_toast"):
                self.app.show_toast("UzCrypto o'rnatuvchi dastur ishga tushirildi! 🔐", "success")
        except Exception as e:
            logger.error(f"[APPS] UzCrypto ishga tushirishda xatolik: {e}")
            QMessageBox.critical(
                self,
                "Ishga tushirishda xatolik",
                f"UzCrypto dasturini ishga tushirib bo'lmadi:\n{str(e)}"
            )

    def copy_uzcrypto_file(self):
        """UzCrypto faylini Windows buferiga nusxalash (Ctrl+V paste uchun)."""
        if not os.path.exists(UZCRYPTO_PATH):
            QMessageBox.warning(
                self,
                "Fayl Topilmadi",
                f"UzCrypto o'rnatish fayli quyidagi manzilda topilmadi:\n{UZCRYPTO_PATH}"
            )
            return

        ok = copy_file_to_windows_clipboard(UZCRYPTO_PATH)
        if ok:
            orig_text = "📋 Nusxa olish (Kopiya)"
            self.btn_copy_uzcrypto.setText("✅ Nusxalandi! (Ctrl+V)")
            self.btn_copy_uzcrypto.setStyleSheet("background-color: #059669; color: #ffffff; font-weight: 700; padding: 7px 10px;")
            QTimer.singleShot(2500, lambda: self._restore_copy_btn(self.btn_copy_uzcrypto, orig_text))

            if self.app and hasattr(self.app, "show_toast"):
                self.app.show_toast("UzCrypto buferga nusxalandi! Istalgan papkaga o'tib Ctrl+V bosing 📋", "success")

    def open_uzcrypto_folder(self):
        """UzCrypto fayli joylashgan papkani Windows Explorer da ko'rsatish."""
        self._reveal_in_explorer(UZCRYPTO_PATH)

    def launch_anydesk(self):
        """AnyDesk masofaviy yordam dasturini ishga tushirish."""
        if not os.path.exists(ANYDESK_PATH):
            QMessageBox.warning(
                self,
                "Fayl Topilmadi",
                f"AnyDesk dasturi quyidagi manzilda topilmadi:\n{ANYDESK_PATH}\n\nFaylni loyiha papkasiga joylashtiring."
            )
            return

        try:
            logger.info(f"[APPS] AnyDesk ishga tushirilmoqda: {ANYDESK_PATH}")
            if hasattr(os, "startfile"):
                os.startfile(ANYDESK_PATH)
            else:
                subprocess.Popen([ANYDESK_PATH], shell=False)

            if self.app and hasattr(self.app, "show_toast"):
                self.app.show_toast("AnyDesk ishga tushirildi! ID raqamingizni taqdim eting ⚡", "info")
        except Exception as e:
            logger.error(f"[APPS] AnyDesk ishga tushirishda xatolik: {e}")
            QMessageBox.critical(
                self,
                "Ishga tushirishda xatolik",
                f"AnyDesk dasturini ishga tushirib bo'lmadi:\n{str(e)}"
            )

    def copy_anydesk_file(self):
        """AnyDesk faylini Windows buferiga nusxalash (Ctrl+V paste uchun)."""
        if not os.path.exists(ANYDESK_PATH):
            QMessageBox.warning(
                self,
                "Fayl Topilmadi",
                f"AnyDesk dasturi quyidagi manzilda topilmadi:\n{ANYDESK_PATH}"
            )
            return

        ok = copy_file_to_windows_clipboard(ANYDESK_PATH)
        if ok:
            orig_text = "📋 Nusxa olish (Kopiya)"
            self.btn_copy_anydesk.setText("✅ Nusxalandi! (Ctrl+V)")
            self.btn_copy_anydesk.setStyleSheet("background-color: #059669; color: #ffffff; font-weight: 700; padding: 7px 10px;")
            QTimer.singleShot(2500, lambda: self._restore_copy_btn(self.btn_copy_anydesk, orig_text))

            if self.app and hasattr(self.app, "show_toast"):
                self.app.show_toast("AnyDesk buferga nusxalandi! Istalgan papkaga o'tib Ctrl+V bosing 📋", "success")

    def _restore_copy_btn(self, btn: QPushButton, text: str):
        btn.setText(text)
        btn.setStyleSheet("")

    def open_anydesk_folder(self):
        """AnyDesk fayli joylashgan papkani Windows Explorer da ko'rsatish."""
        self._reveal_in_explorer(ANYDESK_PATH)

    def _reveal_in_explorer(self, target_path: str):
        """Faylni Windows Explorer da tanlab ko'rsatish."""
        norm_path = os.path.normpath(target_path)
        try:
            if os.path.exists(norm_path):
                subprocess.Popen(f'explorer /select,"{norm_path}"')
            else:
                parent_dir = os.path.dirname(norm_path)
                if os.path.exists(parent_dir):
                    os.startfile(parent_dir)
                else:
                    QMessageBox.warning(self, "Papka topilmadi", f"Yo'l topilmadi:\n{norm_path}")
        except Exception as e:
            logger.error(f"[EXPLORER] Papkani ochishda xatolik: {e}")
            try:
                os.startfile(os.path.dirname(norm_path))
            except Exception:
                pass

    def set_theme(self, theme: str):
        """Mavzu o'zgarganda (light / dark) kartalarni yangilash."""
        self.current_theme = theme
        is_light = (theme == "light")
        if is_light:
            self.title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #0284c7;")
            self.sub_lbl.setStyleSheet("font-size: 11.5px; color: #475569;")
            self.sys_banner.setStyleSheet("""
                QFrame {
                    background: #f1f5f9;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 10px 14px;
                }
            """)
            self.lbl_os_info.setStyleSheet("color: #1e293b; font-size: 11.5px;")
            self.card_uzcrypto.setStyleSheet("""
                QFrame {
                    background: #ffffff;
                    border: 1px solid #93c5fd;
                    border-radius: 10px;
                }
                QFrame:hover {
                    border: 1px solid #3b82f6;
                    background: #f8fafc;
                }
            """)
            self.card_anydesk.setStyleSheet("""
                QFrame {
                    background: #ffffff;
                    border: 1px solid #fca5a5;
                    border-radius: 10px;
                }
                QFrame:hover {
                    border: 1px solid #ef4444;
                    background: #f8fafc;
                }
            """)
            self.card_guide.setStyleSheet("""
                QFrame {
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 12px 14px;
                }
            """)
        else:
            self.title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8;")
            self.sub_lbl.setStyleSheet("font-size: 11.5px; color: #94a3b8;")
            self.sys_banner.setStyleSheet("""
                QFrame {
                    background: rgba(30, 41, 59, 0.6);
                    border: 1px solid rgba(56, 189, 248, 0.25);
                    border-radius: 8px;
                    padding: 10px 14px;
                }
            """)
            self.lbl_os_info.setStyleSheet("color: #cbd5e1; font-size: 11.5px;")
            self.card_uzcrypto.setStyleSheet("""
                QFrame {
                    background: rgba(15, 23, 42, 0.7);
                    border: 1px solid rgba(56, 189, 248, 0.28);
                    border-radius: 10px;
                }
                QFrame:hover {
                    border: 1px solid rgba(56, 189, 248, 0.6);
                }
            """)
            self.card_anydesk.setStyleSheet("""
                QFrame {
                    background: rgba(15, 23, 42, 0.7);
                    border: 1px solid rgba(244, 63, 94, 0.28);
                    border-radius: 10px;
                }
                QFrame:hover {
                    border: 1px solid rgba(244, 63, 94, 0.6);
                }
            """)
            self.card_guide.setStyleSheet("""
                QFrame {
                    background: rgba(30, 41, 59, 0.4);
                    border: 1px solid rgba(148, 163, 184, 0.2);
                    border-radius: 8px;
                    padding: 12px 14px;
                }
            """)
