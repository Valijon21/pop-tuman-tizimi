"""
ui_qt.views.password_dialog: Tahrirlash va Sozlamalar uchun zamonaviy xavfsizlik dialogi (PyQt5).
PBKDF2-HMAC-SHA256, ko'z tugmasi (show/hide), sessiyani eslab qolish va brute-force himoyasi bilan.
"""
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFrame, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont

from core.security import verify_action_password, is_rate_limited
from ui_qt.styles import get_stylesheet
from core.logger import logger


class PasswordPromptDialog(QDialog):
    """Amallarni (tahrirlash yoki sozlamalar) himoyalash uchun zamonaviy modal dialog."""

    def __init__(self, parent=None, app=None, action: str = "edit"):
        super().__init__(parent)
        self.app = app
        self.action = action  # "edit" yoki "settings"
        self.current_theme = getattr(app, "current_theme", "dark")
        self.font_size = getattr(app, "font_size", 12)
        self.is_password_visible = False

        self.setWindowTitle("🔒 Xavfsizlik Himoyasi")
        self.setFixedSize(380, 240)
        self.setModal(True)
        self.setStyleSheet(get_stylesheet(self.current_theme, self.font_size))

        self.setup_ui()

    def setup_ui(self):
        is_light = (self.current_theme == "light")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(12)

        # 1. Sarlavha va Ikona
        head = QHBoxLayout()
        head.setSpacing(10)

        icon_lbl = QLabel("🔐" if self.action == "settings" else "✏️")
        icon_lbl.setStyleSheet("font-size: 24px;")
        head.addWidget(icon_lbl)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        
        if self.action == "settings":
            title_text = "Sozlamalarga Kirish"
            sub_text = "Tizim sozlamalari himoyalangan. Parolni kiriting:"
        else:
            title_text = "Tahrirlash Rejimi"
            sub_text = "Tashkilotlarni o'zgartirish uchun parolni kiriting:"

        lbl_title = QLabel(title_text)
        lbl_title.setStyleSheet(f"font-size: 14px; font-weight: 800; color: {'#0284c7' if is_light else '#38bdf8'};")
        title_box.addWidget(lbl_title)

        lbl_sub = QLabel(sub_text)
        lbl_sub.setWordWrap(True)
        lbl_sub.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'};")
        title_box.addWidget(lbl_sub)

        head.addLayout(title_box)
        layout.addLayout(head)

        # 2. Parol kiritish maydoni + Ko'z tugmasi
        input_container = QFrame()
        input_container.setStyleSheet(
            f"background: {'#f1f5f9' if is_light else '#1e293b'}; "
            f"border: 1px solid {'#cbd5e1' if is_light else '#334155'}; "
            f"border-radius: 6px; padding: 2px 4px;"
        )
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(6, 2, 6, 2)
        input_layout.setSpacing(6)

        self.edit_pwd = QLineEdit()
        self.edit_pwd.setEchoMode(QLineEdit.Password)
        self.edit_pwd.setPlaceholderText("Parolni kiriting...")
        self.edit_pwd.setStyleSheet("border: none; background: transparent; font-size: 12px;")
        self.edit_pwd.returnPressed.connect(self.submit_password)
        input_layout.addWidget(self.edit_pwd, 1)

        self.btn_eye = QPushButton("👁")
        self.btn_eye.setCursor(Qt.PointingHandCursor)
        self.btn_eye.setToolTip("Parolni ko'rsatish/yashirish")
        self.btn_eye.setStyleSheet("border: none; background: transparent; font-size: 14px; padding: 2px;")
        self.btn_eye.clicked.connect(self.toggle_password_visibility)
        input_layout.addWidget(self.btn_eye)

        layout.addWidget(input_container)

        # Xatolik matni (yashirin)
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #ef4444; font-size: 11px; font-weight: 600;")
        self.lbl_error.setVisible(False)
        layout.addWidget(self.lbl_error)

        # 3. Sessiyani eslab qolish opsiyasi
        self.chk_remember = QCheckBox("Ushbu sessiyada eslab qolish")
        self.chk_remember.setChecked(True)
        self.chk_remember.setCursor(Qt.PointingHandCursor)
        self.chk_remember.setStyleSheet(f"font-size: 11px; color: {'#475569' if is_light else '#cbd5e1'};")
        layout.addWidget(self.chk_remember)

        # 4. Tugmalar
        btns = QHBoxLayout()
        btns.setSpacing(8)

        self.btn_cancel = QPushButton("Bekor Qilish")
        self.btn_cancel.setProperty("class", "btn_secondary")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        btns.addWidget(self.btn_cancel)

        self.btn_submit = QPushButton("Tasdiqlash ↵")
        self.btn_submit.setProperty("class", "btn_primary")
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        self.btn_submit.clicked.connect(self.submit_password)
        btns.addWidget(self.btn_submit)

        layout.addLayout(btns)

        # Dastlab fokusni parol maydoniga berish
        QTimer.singleShot(50, self.edit_pwd.setFocus)

    def toggle_password_visibility(self):
        """Parolni ko'rsatish yoki yashirish."""
        self.is_password_visible = not self.is_password_visible
        if self.is_password_visible:
            self.edit_pwd.setEchoMode(QLineEdit.Normal)
            self.btn_eye.setText("🙈")
        else:
            self.edit_pwd.setEchoMode(QLineEdit.Password)
            self.btn_eye.setText("👁")

    def submit_password(self):
        """Parolni tekshirish va tasdiqlash."""
        entered = self.edit_pwd.text().strip()
        if not entered:
            self.lbl_error.setText("⚠️ Iltimos, parolni kiriting.")
            self.lbl_error.setVisible(True)
            return

        passwords_dict = {}
        if self.app and hasattr(self.app, "data_manager"):
            passwords_dict = self.app.data_manager.settings.get("passwords", {})

        ident = f"action_{self.action}"
        ok, msg = verify_action_password(self.action, entered, passwords_dict, identifier=ident)

        if ok:
            # Agar eslab qolish tanlangan bo'lsa, app sessiyasiga yozib qo'yish
            if self.app and self.chk_remember.isChecked():
                if not hasattr(self.app, "_session_authenticated"):
                    self.app._session_authenticated = {}
                self.app._session_authenticated[self.action] = True
            logger.info(f"[SECURITY] '{self.action}' uchun parol muvaffaqiyatli tasdiqlandi.")
            self.accept()
        else:
            self.lbl_error.setText(f"❌ {msg}")
            self.lbl_error.setVisible(True)
            self.edit_pwd.selectAll()
            self.edit_pwd.setFocus()


def request_password(parent: Any, app: Any, action: str = "edit") -> bool:
    """
    Amal ('edit' yoki 'settings') uchun parolni so'rash.
    Agar joriy sessiyada avval muvaffaqiyatli kiritilgan bo'lsa, qayta so'ramaydi.
    """
    if app and hasattr(app, "_session_authenticated"):
        if app._session_authenticated.get(action):
            return True

    # Offscreen yoki test rejimida modal bloklanmasligi uchun
    import os
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen" or os.environ.get("TESTING") == "1":
        return True

    dialog = PasswordPromptDialog(parent=parent, app=app, action=action)
    return (dialog.exec_() == QDialog.Accepted)
