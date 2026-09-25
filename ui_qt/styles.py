"""
ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterprise Edition).
Kichik va o'rta ekranlarga (1366x768, 1080p, 2K/4K, 125%/150% High-DPI) mukammal moslashuvchan,
ixcham, professional, ko'zni charchatmaydigan Fluent UI dizayni.
To'liq Dark va Light rejimlari, dinamik shrift masshtabi, mukammal ranglar balansi.
"""
from typing import Dict, Any


def hex_to_rgba(hex_code: str, alpha: float = 0.12) -> str:
    """Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazadi."""
    h = str(hex_code).strip().lstrip("#")
    if len(h) >= 6:
        try:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha:.2f})"
        except ValueError:
            pass
    return hex_code


def get_stylesheet(theme: str = "dark", font_size: int = 12) -> str:
    """
    Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha
    to'liq va mukammal PyQt5 QSS stilini generatsiya qiladi.
    """
    is_light = (str(theme).lower() == "light")
    fs = max(10, min(20, int(font_size)))  # Xavfsiz chegaralarda (10px - 20px)

    # Shrift o'lchamlari ierarxiyasi (butun son piksellarda)
    fs_micro = max(9, fs - 3)     # 9-10px (Kichik belgilar, yordamchi)
    fs_sub = max(10, fs - 2)      # 10-11px (Subtitrlar, hintlar)
    fs_sidebar = max(10, fs - 1)  # 11px standart (asosiysi 12px bo'lganda sidebar menyulari uchun nafis)
    fs_caption = max(11, fs - 1)  # 11-12px (Headerlar, toifa pillari)
    fs_base = fs                  # 12-13px (Asosiy matn, inputlar, jadval)
    fs_title_sm = fs + 1          # 13-14px (Kichik sarlavhalar)
    fs_title_md = fs + 3          # 15-16px (Oyna / dialog sarlavhalari)
    fs_kpi = fs + 8               # 20-22px (Katta raqamli ko'rsatkichlar)

    if is_light:
        # ==========================================
        # KUNDUZGI (LIGHT) MAVZU RANG TOKENS
        # ==========================================
        c_bg_main = "#f8fafc"           # Slate 50
        c_sidebar_bg = "#ffffff"        # Oq
        c_sidebar_border = "#e2e8f0"    # Slate 200
        c_sidebar_title = "#0f172a"     # Slate 900
        c_sidebar_sub = "#0284c7"       # Sky 600
        c_sidebar_btn_text = "#475569"  # Slate 600
        c_sidebar_btn_hover = "#f1f5f9" # Slate 100
        c_sidebar_btn_hover_fg = "#0f172a"

        c_card_bg = "#ffffff"
        c_card_border = "#e2e8f0"
        c_card_hover_bg = "#f0f7ff"
        c_card_hover_border = "#93c5fd"

        c_text_main = "#0f172a"         # Slate 900
        c_text_muted = "#475569"        # Slate 600
        c_text_tertiary = "#94a3b8"     # Slate 400
        c_text_disabled = "#94a3b8"

        c_input_bg = "#ffffff"
        c_input_border = "#cbd5e1"      # Slate 300
        c_input_focus_bg = "#ffffff"
        c_input_hover_border = "#94a3b8"
        c_input_disabled_bg = "#f1f5f9"
        c_arrow = "#475569"

        c_btn_base_bg = "#f1f5f9"
        c_btn_base_fg = "#1e293b"
        c_btn_base_border = "#cbd5e1"
        c_btn_base_hover = "#e2e8f0"
        c_btn_base_pressed = "#cbd5e1"

        c_btn_sec_bg = "#ffffff"
        c_btn_sec_fg = "#1e293b"
        c_btn_sec_border = "#cbd5e1"
        c_btn_sec_hover = "#f1f5f9"
        c_btn_sec_hover_border = "#94a3b8"

        c_pill_bg = "#ffffff"
        c_pill_border = "#cbd5e1"
        c_pill_fg = "#475569"
        c_pill_hover_bg = "#f1f5f9"
        c_pill_hover_fg = "#0f172a"
        c_pill_hover_border = "#94a3b8"

        c_table_bg = "#ffffff"
        c_table_alt_bg = "#f8fafc"
        c_table_grid = "#f1f5f9"
        c_table_hover = "#f1f5f9"
        c_table_sel_bg = "#dbeafe"      # Blue 100
        c_table_sel_fg = "#1e40af"      # Blue 800
        c_table_hdr_bg = "#f1f5f9"
        c_table_hdr_fg = "#475569"
        c_table_hdr_border = "#e2e8f0"

        c_scroll_track = "#f8fafc"
        c_scroll_thumb = "#cbd5e1"
        c_scroll_thumb_hover = "#94a3b8"

        c_menu_bg = "#ffffff"
        c_menu_border = "#cbd5e1"
        c_menu_hover = "#eff6ff"
        c_menu_hover_fg = "#2563eb"

        c_status_bg = "#ffffff"
        c_status_border = "#e2e8f0"
        c_status_fg = "#64748b"

        c_tab_inactive_bg = "#f1f5f9"
        c_tab_inactive_fg = "#64748b"
        c_tab_active_bg = "#ffffff"
        c_tab_active_fg = "#2563eb"

        c_tooltip_bg = "#0f172a"
        c_tooltip_fg = "#ffffff"
        c_tooltip_border = "#334155"
    else:
        # ==========================================
        # TUNGI (DARK) MAVZU RANG TOKENS
        # ==========================================
        c_bg_main = "#0f172a"           # Slate 900
        c_sidebar_bg = "#0b1120"        # Slate 950
        c_sidebar_border = "#1e293b"    # Slate 800
        c_sidebar_title = "#ffffff"
        c_sidebar_sub = "#38bdf8"       # Sky 400
        c_sidebar_btn_text = "#94a3b8"  # Slate 400
        c_sidebar_btn_hover = "#1e293b" # Slate 800
        c_sidebar_btn_hover_fg = "#f8fafc"

        c_card_bg = "#1e293b"           # Slate 800
        c_card_border = "#334155"       # Slate 700
        c_card_hover_bg = "#243248"
        c_card_hover_border = "#38bdf8"

        c_text_main = "#f1f5f9"         # Slate 100
        c_text_muted = "#94a3b8"        # Slate 400
        c_text_tertiary = "#64748b"     # Slate 500
        c_text_disabled = "#64748b"

        c_input_bg = "#172337"          # To'q fon
        c_input_border = "#334155"
        c_input_focus_bg = "#0b1120"
        c_input_hover_border = "#475569"
        c_input_disabled_bg = "#0b1120"
        c_arrow = "#94a3b8"

        c_btn_base_bg = "#334155"
        c_btn_base_fg = "#f8fafc"
        c_btn_base_border = "#475569"
        c_btn_base_hover = "#475569"
        c_btn_base_pressed = "#1e293b"

        c_btn_sec_bg = "#1e293b"
        c_btn_sec_fg = "#f1f5f9"
        c_btn_sec_border = "#334155"
        c_btn_sec_hover = "#283850"
        c_btn_sec_hover_border = "#475569"

        c_pill_bg = "#1e293b"
        c_pill_border = "#334155"
        c_pill_fg = "#cbd5e1"
        c_pill_hover_bg = "#334155"
        c_pill_hover_fg = "#ffffff"
        c_pill_hover_border = "#475569"

        c_table_bg = "#1e293b"
        c_table_alt_bg = "#172233"
        c_table_grid = "#243248"
        c_table_hover = "#2d3e58"
        c_table_sel_bg = "#1d4ed8"      # Blue 700
        c_table_sel_fg = "#ffffff"
        c_table_hdr_bg = "#0b1120"
        c_table_hdr_fg = "#94a3b8"
        c_table_hdr_border = "#334155"

        c_scroll_track = "#0f172a"
        c_scroll_thumb = "#334155"
        c_scroll_thumb_hover = "#475569"

        c_menu_bg = "#1e293b"
        c_menu_border = "#334155"
        c_menu_hover = "#2563eb"
        c_menu_hover_fg = "#ffffff"

        c_status_bg = "#0b1120"
        c_status_border = "#1e293b"
        c_status_fg = "#94a3b8"

        c_tab_inactive_bg = "#0f172a"
        c_tab_inactive_fg = "#94a3b8"
        c_tab_active_bg = "#1e293b"
        c_tab_active_fg = "#38bdf8"

        c_tooltip_bg = "#1e293b"
        c_tooltip_fg = "#f8fafc"
        c_tooltip_border = "#475569"

    qss = f"""
/* ==========================================================================
   POP TUMAN TIZIMI - UNIFIED ENTERPRISE QSS
   Mavzu: {'Kunduzgi (Light)' if is_light else 'Tungi (Dark)'} | Shrift: {fs}px
   ========================================================================== */

* {{
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, "Roboto", "Helvetica Neue", sans-serif;
    font-size: {fs_base}px;
    color: {c_text_main};
    outline: none;
}}

QMainWindow, QDialog {{
    background-color: {c_bg_main};
}}

QWidget {{
    background-color: transparent;
}}

/* ========== SIDEBAR (CHAP BOSHQARUV PANELI) ========== */
QFrame#sidebar {{
    background-color: {c_sidebar_bg};
    border-right: 1px solid {c_sidebar_border};
    min-width: 220px;
    max-width: 236px;
}}

QLabel#sidebar_title {{
    font-size: {fs_title_sm}px;
    font-weight: 800;
    color: {c_sidebar_title};
    letter-spacing: 0.8px;
    padding: 1px 0px 0px 0px;
}}

QLabel#sidebar_subtitle {{
    font-size: {fs_micro}px;
    font-weight: 700;
    color: {c_sidebar_sub};
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 0px;
}}

QLabel#sidebar_section {{
    font-size: {fs_micro}px;
    font-weight: 700;
    color: {c_text_tertiary};
    letter-spacing: 0.8px;
    padding: 6px 8px 2px 8px;
    text-transform: uppercase;
}}

/* Sidebar Tugmalari */
QPushButton.sidebar_btn {{
    text-align: left;
    padding: 6px 10px;
    border: none;
    border-radius: 6px;
    background-color: transparent;
    color: {c_sidebar_btn_text};
    font-size: {fs_sidebar}px;
    font-weight: 600;
    margin: 1px 3px;
    min-height: 18px;
}}

QPushButton.sidebar_btn:hover {{
    background-color: {c_sidebar_btn_hover};
    color: {c_sidebar_btn_hover_fg};
}}

QPushButton.sidebar_btn:checked, QPushButton.sidebar_btn.active {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6);
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.sidebar_btn_danger {{
    text-align: left;
    padding: 6px 10px;
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 6px;
    background-color: rgba(239, 68, 68, 0.08);
    color: #ef4444;
    font-size: {fs_sidebar}px;
    font-weight: 700;
    margin: 1px 3px;
    min-height: 18px;
}}

QPushButton.sidebar_btn_danger:hover {{
    background-color: #ef4444;
    color: #ffffff;
}}

QPushButton.sidebar_btn_danger:pressed {{
    background-color: #dc2626;
    color: #ffffff;
}}

/* ========== ASOSIY KONTENT MAYDONI ========== */
QFrame#content_area {{
    background-color: {c_bg_main};
    border: none;
}}

/* ========== KARTALAR (CARDS & SURFACES) ========== */
QFrame.stat_card, QFrame.clickable_card, QFrame#donut_card, QFrame#bar_card,
QFrame#contract_kpi_card, QFrame.info_card {{
    background-color: {c_card_bg};
    border: 1px solid {c_card_border};
    border-radius: 8px;
}}

QFrame#donut_card, QFrame#bar_card, QFrame.info_card {{
    padding: 10px;
}}

QFrame.stat_card:hover, QFrame.clickable_card:hover {{
    border: 1px solid {c_card_hover_border};
    background-color: {c_card_hover_bg};
}}

QLabel.card_title {{
    font-size: {fs_caption}px;
    font-weight: 600;
    color: {c_text_muted};
    text-transform: uppercase;
    letter-spacing: 0.4px;
}}

QLabel.card_value {{
    font-size: {fs_kpi}px;
    font-weight: 800;
    color: {c_text_main};
    margin: 2px 0px;
}}

QLabel.card_subtitle {{
    font-size: {fs_sub}px;
    color: {c_text_tertiary};
}}

/* ========== INPUTLAR, TEXTEDIT VA COMBOBOX ========== */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {c_input_bg};
    border: 1px solid {c_input_border};
    border-radius: 6px;
    padding: 5px 8px;
    color: {c_text_main};
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    font-size: {fs_base}px;
    min-height: 18px;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1.5px solid #3b82f6;
    background-color: {c_input_focus_bg};
}}

QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
    background-color: {c_input_disabled_bg};
    color: {c_text_disabled};
    border-color: {c_card_border};
}}

QComboBox {{
    background-color: {c_input_bg};
    border: 1px solid {c_input_border};
    border-radius: 6px;
    padding: 4px 8px;
    color: {c_text_main};
    min-height: 20px;
    font-size: {fs_base}px;
    font-weight: 500;
}}

QComboBox:hover {{
    border-color: {c_input_hover_border};
}}

QComboBox:focus {{
    border: 1.5px solid #3b82f6;
}}

QComboBox::drop-down {{
    border: none;
    width: 22px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {c_arrow};
    margin-right: 6px;
}}

QComboBox QAbstractItemView {{
    background-color: {c_card_bg};
    border: 1px solid {c_card_border};
    border-radius: 6px;
    color: {c_text_main};
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    padding: 4px;
    outline: none;
}}

/* ========== QSPINBOX VA QDOUBLESPINBOX ========== */
QSpinBox, QDoubleSpinBox {{
    background-color: {c_input_bg};
    border: 1px solid {c_input_border};
    border-radius: 6px;
    padding: 4px 8px;
    color: {c_text_main};
    min-height: 20px;
    font-size: {fs_base}px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1.5px solid #3b82f6;
    background-color: {c_input_focus_bg};
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 18px;
    border: none;
    background: transparent;
    margin-right: 3px;
}}

QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 18px;
    border: none;
    background: transparent;
    margin-right: 3px;
}}

QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-bottom: 4px solid {c_arrow};
    width: 0px;
    height: 0px;
}}

QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-top: 4px solid {c_arrow};
    width: 0px;
    height: 0px;
}}

/* ========== QCHECKBOX VA QRADIOBUTTON ========== */
QCheckBox, QRadioButton {{
    spacing: 7px;
    color: {c_text_main};
    font-size: {fs_base}px;
    font-weight: 500;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid {c_input_border};
    border-radius: 4px;
    background-color: {c_input_bg};
}}

QCheckBox::indicator:hover {{
    border-color: #3b82f6;
}}

QCheckBox::indicator:checked {{
    background-color: #2563eb;
    border-color: #2563eb;
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid {c_input_border};
    border-radius: 8px;
    background-color: {c_input_bg};
}}

QRadioButton::indicator:hover {{
    border-color: #3b82f6;
}}

QRadioButton::indicator:checked {{
    background-color: #2563eb;
    border: 3.5px solid {c_card_bg};
}}

/* ========== TUGMALAR (BUTTONS) TIZIMI ========== */
QPushButton {{
    background-color: {c_btn_base_bg};
    color: {c_btn_base_fg};
    border: 1px solid {c_btn_base_border};
    border-radius: 6px;
    padding: 5px 12px;
    font-size: {fs_base}px;
    font-weight: 600;
    min-height: 18px;
}}

QPushButton:hover {{
    background-color: {c_btn_base_hover};
    border-color: {c_input_hover_border};
}}

QPushButton:pressed {{
    background-color: {c_btn_base_pressed};
}}

QPushButton:disabled {{
    background-color: {c_input_disabled_bg};
    color: {c_text_disabled};
    border-color: transparent;
}}

/* Primary Button (Moviy / Royal Blue) */
QPushButton.btn_primary {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6);
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.btn_primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1d4ed8, stop:1 #2563eb);
}}

QPushButton.btn_primary:pressed {{
    background-color: #1e40af;
}}

/* Secondary Button (Neytral toza tugma) */
QPushButton.btn_secondary {{
    background-color: {c_btn_sec_bg};
    border: 1px solid {c_btn_sec_border};
    color: {c_btn_sec_fg};
    font-weight: 600;
}}

QPushButton.btn_secondary:hover {{
    background-color: {c_btn_sec_hover};
    border-color: {c_btn_sec_hover_border};
}}

QPushButton.btn_secondary:pressed {{
    background-color: {c_btn_base_pressed};
}}

/* Success Button (Yashil / Emerald) */
QPushButton.btn_success {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.btn_success:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #047857, stop:1 #059669);
}}

QPushButton.btn_success:pressed {{
    background-color: #064e3b;
}}

/* Danger Button (Qizil / Crimson) */
QPushButton.btn_danger {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #ef4444);
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.btn_danger:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b91c1c, stop:1 #dc2626);
}}

QPushButton.btn_danger:pressed {{
    background-color: #991b1b;
}}

/* Warning Button (Sariq / To'q sariq) */
QPushButton.btn_warning {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d97706, stop:1 #f59e0b);
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.btn_warning:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b45309, stop:1 #d97706);
}}

QPushButton.btn_warning:pressed {{
    background-color: #78350f;
}}

/* Info Button (Moviy-ko'k / Sky Blue) */
QPushButton.btn_info {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.btn_info:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0369a1, stop:1 #0284c7);
}}

QPushButton.btn_info:pressed {{
    background-color: #075985;
}}

/* Purple Button (Siyohrang / Violet) */
QPushButton.btn_purple {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7c3aed, stop:1 #8b5cf6);
    border: none;
    color: #ffffff;
    font-weight: 700;
}}

QPushButton.btn_purple:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6d28d9, stop:1 #7c3aed);
}}

QPushButton.btn_purple:pressed {{
    background-color: #5b21b6;
}}

/* Filter Pill Button (Toifalar tanlash tugmasi) */
QPushButton.pill_btn {{
    background-color: {c_pill_bg};
    border: 1px solid {c_pill_border};
    border-radius: 13px;
    padding: 4px 12px;
    color: {c_pill_fg};
    font-size: {fs_caption}px;
    font-weight: 600;
    min-height: 16px;
}}

QPushButton.pill_btn:hover {{
    background-color: {c_pill_hover_bg};
    color: {c_pill_hover_fg};
    border-color: {c_pill_hover_border};
}}

QPushButton.pill_btn:checked, QPushButton.pill_btn.active {{
    background-color: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
    font-weight: 700;
}}

/* ========== JADVALLAR (QTableView & QTableWidget) ========== */
QTableView, QTableWidget {{
    background-color: {c_table_bg};
    alternate-background-color: {c_table_alt_bg};
    border: 1px solid {c_card_border};
    border-radius: 8px;
    gridline-color: {c_table_grid};
    color: {c_text_main};
    selection-background-color: {c_table_sel_bg};
    selection-color: {c_table_sel_fg};
    font-size: {fs_base}px;
    outline: none;
}}

QTableView::item, QTableWidget::item {{
    padding: 5px 7px;
    border: none;
}}

QTableView::item:selected, QTableWidget::item:selected {{
    background-color: {c_table_sel_bg};
    color: {c_table_sel_fg};
    font-weight: 600;
}}

QTableView::item:hover, QTableWidget::item:hover {{
    background-color: {c_table_hover};
}}

QHeaderView::section {{
    background-color: {c_table_hdr_bg};
    color: {c_table_hdr_fg};
    padding: 6px 9px;
    border: none;
    border-bottom: 2px solid {c_table_hdr_border};
    font-size: {fs_caption}px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}}

QHeaderView::section:hover {{
    background-color: {c_card_hover_bg};
    color: {c_text_main};
}}

QTableCornerButton::section {{
    background-color: {c_table_hdr_bg};
    border: none;
    border-bottom: 2px solid {c_table_hdr_border};
}}

/* ========== SILLIQ ZAMONAVIY SCROLLBAR ========== */
QScrollBar:vertical {{
    border: none;
    background: {c_scroll_track};
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical {{
    background: {c_scroll_thumb};
    min-height: 24px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: {c_scroll_thumb_hover};
}}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {{
    background: none;
    border: none;
    height: 0px;
}}

QScrollBar:horizontal {{
    border: none;
    background: {c_scroll_track};
    height: 6px;
    margin: 0px;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal {{
    background: {c_scroll_thumb};
    min-width: 24px;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {c_scroll_thumb_hover};
}}

QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal,
QScrollBar::sub-page:horizontal, QScrollBar::add-page:horizontal {{
    background: none;
    border: none;
    width: 0px;
}}

/* ========== KONTEKST MENYU (QMenu) ========== */
QMenu {{
    background-color: {c_menu_bg};
    border: 1px solid {c_menu_border};
    border-radius: 6px;
    padding: 4px 0px;
}}

QMenu::item {{
    padding: 6px 18px 6px 12px;
    color: {c_text_main};
    font-size: {fs_base}px;
    font-weight: 500;
}}

QMenu::item:selected {{
    background-color: {c_menu_hover};
    color: {c_menu_hover_fg};
}}

QMenu::separator {{
    height: 1px;
    background: {c_card_border};
    margin: 3px 6px;
}}

/* ========== STATUS BAR ========== */
QStatusBar {{
    background-color: {c_status_bg};
    color: {c_status_fg};
    border-top: 1px solid {c_status_border};
    font-size: {fs_caption}px;
    min-height: 24px;
    padding: 1px 8px;
}}

QStatusBar QLabel {{
    color: {c_status_fg};
    font-size: {fs_caption}px;
    font-weight: 500;
}}

/* ========== DIALOG VA TABVIEW ========== */
QTabWidget::pane {{
    border: 1px solid {c_card_border};
    border-radius: 6px;
    background-color: {c_card_bg};
    top: -1px;
}}

QTabBar::tab {{
    background-color: {c_tab_inactive_bg};
    color: {c_tab_inactive_fg};
    padding: 6px 14px;
    margin-right: 3px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    font-size: {fs_caption}px;
}}

QTabBar::tab:selected {{
    background-color: {c_tab_active_bg};
    color: {c_tab_active_fg};
    border: 1px solid {c_card_border};
    border-bottom: none;
}}

QTabBar::tab:hover:!selected {{
    background-color: {c_card_hover_bg};
    color: {c_text_main};
}}

/* ========== GROUPBOX ========== */
QGroupBox {{
    border: 1px solid {c_card_border};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 10px;
    font-size: {fs_title_sm}px;
    font-weight: 700;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {'#0284c7' if is_light else '#38bdf8'};
}}

/* ========== TOOLTIP ========== */
QToolTip {{
    background-color: {c_tooltip_bg};
    color: {c_tooltip_fg};
    border: 1px solid {c_tooltip_border};
    border-radius: 5px;
    padding: 4px 8px;
    font-size: {fs_caption}px;
}}

/* ========== PROGRESS BAR ========== */
QProgressBar {{
    background-color: {c_card_border};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    font-size: {fs_micro}px;
    color: {c_text_main};
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #38bdf8);
    border-radius: 4px;
}}
"""
    return qss

# Standart importlar uchun qulay o'zgaruvchilar
DARK_THEME = get_stylesheet("dark", 12)
LIGHT_THEME = get_stylesheet("light", 12)


def create_crisp_pixmap(
    image_path: str,
    target_width: int = 0,
    target_height: int = 0,
    supersample: float = 3.0
):
    """
    Retina / 4K / High-DPI o'lchamli kristall tiniqlikdagi QPixmap yaratish.
    Windows 125%, 150%, 175%, 200% masshtablarida ham rasmlar xira (blurry/hira)
    bo'lib qolmasligi uchun apparat piksellarida yuqori aniqlikda (supersampling)
    masshtablaydi va Qt setDevicePixelRatio ni o'rnatadi.
    """
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap

    if not image_path:
        return QPixmap()

    pix = QPixmap(image_path)
    if pix.isNull():
        return pix

    scale = max(1.0, float(supersample))
    if target_width > 0 and target_height > 0:
        phys_w = int(target_width * scale)
        phys_h = int(target_height * scale)
        scaled = pix.scaled(phys_w, phys_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    elif target_width > 0:
        phys_w = int(target_width * scale)
        scaled = pix.scaledToWidth(phys_w, Qt.SmoothTransformation)
    elif target_height > 0:
        phys_h = int(target_height * scale)
        scaled = pix.scaledToHeight(phys_h, Qt.SmoothTransformation)
    else:
        scaled = pix

    scaled.setDevicePixelRatio(scale)
    return scaled

