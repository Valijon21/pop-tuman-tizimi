"""
Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Compact Edition)
Kichik va o'rta ekranlarga (1366x768, 1080p, 125%/150% High-DPI) mukammal moslashuvchan,
ixcham, professional va silliq Fluent UI QSS dizayni.
"""

DARK_THEME = """
/* ========== UMUMIY ILDIRIZ VA SHIRIFTLAR ========== */
* {
    font-family: "Segoe UI", "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 11.5px;
    color: #f1f5f9;
    outline: none;
}

QMainWindow, QDialog {
    background-color: #0f172a;
}

QWidget {
    background-color: transparent;
}

/* ========== SIDEBAR (CHAP MENYU) ========== */
QFrame#sidebar {
    background-color: #0b1120;
    border-right: 1px solid #1e293b;
    min-width: 222px;
    max-width: 232px;
}

QLabel#sidebar_title {
    font-size: 13px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.5px;
    padding: 2px 0px 1px 0px;
}

QLabel#sidebar_subtitle {
    font-size: 9.5px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

QLabel#sidebar_section {
    font-size: 9.5px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.8px;
    padding: 8px 8px 2px 8px;
    text-transform: uppercase;
}

/* Sidebar Tugmalari */
QPushButton.sidebar_btn {
    text-align: left;
    padding: 6px 10px;
    border: none;
    border-radius: 6px;
    background-color: transparent;
    color: #94a3b8;
    font-size: 11.5px;
    font-weight: 600;
    margin: 1px 4px;
    min-height: 18px;
}

QPushButton.sidebar_btn:hover {
    background-color: #1e293b;
    color: #f8fafc;
}

QPushButton.sidebar_btn:checked, QPushButton.sidebar_btn.active {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6);
    color: #ffffff;
    font-weight: 700;
}

/* ========== ASOSIY KONTENT MAYDONI ========== */
QFrame#content_area {
    background-color: #0f172a;
    border: none;
}

/* ========== KARTALAR (CARDS) ========== */
QFrame.stat_card, QFrame.clickable_card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px;
}

QFrame.stat_card:hover, QFrame.clickable_card:hover {
    border: 1px solid #38bdf8;
    background-color: #243248;
}

QFrame#donut_card, QFrame#bar_card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
}

QLabel.card_title {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

QLabel.card_value {
    font-size: 19px;
    font-weight: 800;
    color: #ffffff;
    margin: 2px 0px;
}

QLabel.card_subtitle {
    font-size: 10px;
    color: #64748b;
}

/* ========== INPUTLAR VA COMBOBOX ========== */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 8px;
    color: #f8fafc;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
    font-size: 11.5px;
    min-height: 16px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1.5px solid #3b82f6;
    background-color: #0b1120;
}

QLineEdit:disabled, QTextEdit:disabled {
    background-color: #0b1120;
    color: #64748b;
    border-color: #1e293b;
}

QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px 8px;
    color: #f8fafc;
    min-height: 20px;
    font-size: 11.5px;
    font-weight: 500;
}

QComboBox:hover {
    border-color: #475569;
}

QComboBox:focus {
    border: 1.5px solid #3b82f6;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-top: 4.5px solid #94a3b8;
    margin-right: 6px;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #f8fafc;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    padding: 3px;
    outline: none;
}

/* ========== TUGMALAR (BUTTONS) ========== */
QPushButton {
    background-color: #334155;
    color: #f8fafc;
    border: none;
    border-radius: 6px;
    padding: 5px 11px;
    font-size: 11.5px;
    font-weight: 600;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #475569;
}

QPushButton:pressed {
    background-color: #1e293b;
}

QPushButton:disabled {
    background-color: #1e293b;
    color: #64748b;
}

/* Primary Button (Moviy) */
QPushButton.btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1d4ed8, stop:1 #2563eb);
}

QPushButton.btn_primary:pressed {
    background-color: #1e40af;
}

/* Success Button (Yashil) */
QPushButton.btn_success {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #10b981);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_success:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #047857, stop:1 #059669);
}

/* Danger Button (Qizil) */
QPushButton.btn_danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #ef4444);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b91c1c, stop:1 #dc2626);
}

/* Warning Button (Sariq / To'q sariq) */
QPushButton.btn_warning {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d97706, stop:1 #f59e0b);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_warning:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b45309, stop:1 #d97706);
}

/* Filter Pill Button (Kategoriya tanlash tugmasi) */
QPushButton.pill_btn {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 3px 10px;
    color: #cbd5e1;
    font-size: 11px;
    font-weight: 600;
    min-height: 16px;
}

QPushButton.pill_btn:hover {
    background-color: #334155;
    color: #ffffff;
    border-color: #475569;
}

QPushButton.pill_btn:checked, QPushButton.pill_btn.active {
    background-color: #2563eb;
    color: #ffffff;
    border-color: #3b82f6;
}

/* ========== JADVAL (QTableView & QTableWidget) ========== */
QTableView, QTableWidget {
    background-color: #1e293b;
    alternate-background-color: #172233;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #243248;
    color: #f8fafc;
    selection-background-color: #1d4ed8;
    selection-color: #ffffff;
    font-size: 11.5px;
    outline: none;
}

QTableView::item {
    padding: 4px 6px;
    border: none;
}

QTableView::item:selected {
    background-color: #2563eb;
    color: #ffffff;
}

QTableView::item:hover {
    background-color: #2d3e58;
}

QHeaderView::section {
    background-color: #0b1120;
    color: #94a3b8;
    padding: 5px 8px;
    border: none;
    border-bottom: 2px solid #334155;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

QHeaderView::section:hover {
    background-color: #1e293b;
    color: #ffffff;
}

QTableCornerButton::section {
    background-color: #0b1120;
    border: none;
    border-bottom: 2px solid #334155;
}

/* ========== SILLIQ ZAMONAVIY SCROLLBAR ========== */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 24px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {
    background: none;
    border: none;
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #0f172a;
    height: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 24px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal:hover {
    background: #475569;
}

QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal,
QScrollBar::sub-page:horizontal, QScrollBar::add-page:horizontal {
    background: none;
    border: none;
    width: 0px;
}

/* ========== KONTEKST MENYU (QMenu) ========== */
QMenu {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 4px 0px;
}

QMenu::item {
    padding: 6px 18px 6px 12px;
    color: #f1f5f9;
    font-size: 11.5px;
    font-weight: 500;
}

QMenu::item:selected {
    background-color: #2563eb;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background: #334155;
    margin: 3px 6px;
}

/* ========== STATUS BAR ========== */
QStatusBar {
    background-color: #0b1120;
    color: #94a3b8;
    border-top: 1px solid #1e293b;
    font-size: 11px;
    min-height: 24px;
    padding: 1px 8px;
}

QStatusBar QLabel {
    color: #94a3b8;
    font-size: 11px;
}

/* ========== DIALOG VA TABVIEW ========== */
QTabWidget::pane {
    border: 1px solid #334155;
    border-radius: 6px;
    background-color: #1e293b;
    top: -1px;
}

QTabBar::tab {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 6px 14px;
    margin-right: 3px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    font-size: 11px;
}

QTabBar::tab:selected {
    background-color: #1e293b;
    color: #38bdf8;
    border: 1px solid #334155;
    border-bottom: none;
}

QTabBar::tab:hover:!selected {
    background-color: #172233;
    color: #ffffff;
}

QGroupBox {
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    font-size: 12px;
    font-weight: 700;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #38bdf8;
}
"""

LIGHT_THEME = """
/* ========== UMUMIY ILDIRIZ VA SHIRIFTLAR ========== */
* {
    font-family: "Segoe UI", "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 11.5px;
    color: #1e293b;
    outline: none;
}

QMainWindow, QDialog {
    background-color: #f8fafc;
}

QWidget {
    background-color: transparent;
}

/* ========== SIDEBAR (CHAP MENYU) ========== */
QFrame#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
    min-width: 222px;
    max-width: 232px;
}

QLabel#sidebar_title {
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
    padding: 2px 0px 1px 0px;
}

QLabel#sidebar_subtitle {
    font-size: 9.5px;
    font-weight: 700;
    color: #0284c7;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

QLabel#sidebar_section {
    font-size: 9.5px;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.8px;
    padding: 8px 8px 2px 8px;
    text-transform: uppercase;
}

/* Sidebar Tugmalari */
QPushButton.sidebar_btn {
    text-align: left;
    padding: 6px 10px;
    border: none;
    border-radius: 6px;
    background-color: transparent;
    color: #475569;
    font-size: 11.5px;
    font-weight: 600;
    margin: 1px 4px;
    min-height: 18px;
}

QPushButton.sidebar_btn:hover {
    background-color: #f1f5f9;
    color: #0f172a;
}

QPushButton.sidebar_btn:checked, QPushButton.sidebar_btn.active {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #3b82f6);
    color: #ffffff;
    font-weight: 700;
}

/* ========== ASOSIY KONTENT MAYDONI ========== */
QFrame#content_area {
    background-color: #f8fafc;
    border: none;
}

/* ========== KARTALAR (CARDS) ========== */
QFrame.stat_card, QFrame.clickable_card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px;
}

QFrame.stat_card:hover, QFrame.clickable_card:hover {
    border: 1px solid #93c5fd;
    background-color: #f0f7ff;
}

QFrame#donut_card, QFrame#bar_card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

QLabel.card_title {
    font-size: 11px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

QLabel.card_value {
    font-size: 19px;
    font-weight: 800;
    color: #0f172a;
    margin: 2px 0px;
}

QLabel.card_subtitle {
    font-size: 10px;
    color: #94a3b8;
}

/* ========== INPUTLAR VA COMBOBOX ========== */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 8px;
    color: #0f172a;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    font-size: 11.5px;
    min-height: 16px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1.5px solid #2563eb;
    background-color: #ffffff;
}

QLineEdit:disabled, QTextEdit:disabled {
    background-color: #f1f5f9;
    color: #94a3b8;
    border-color: #e2e8f0;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px 8px;
    color: #0f172a;
    min-height: 20px;
    font-size: 11.5px;
    font-weight: 500;
}

QComboBox:hover {
    border-color: #94a3b8;
}

QComboBox:focus {
    border: 1.5px solid #2563eb;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-top: 4.5px solid #64748b;
    margin-right: 6px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    color: #0f172a;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    padding: 3px;
    outline: none;
}

/* ========== TUGMALAR (BUTTONS) ========== */
QPushButton {
    background-color: #e2e8f0;
    color: #1e293b;
    border: none;
    border-radius: 6px;
    padding: 5px 11px;
    font-size: 11.5px;
    font-weight: 600;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #cbd5e1;
}

QPushButton:pressed {
    background-color: #94a3b8;
}

QPushButton:disabled {
    background-color: #f1f5f9;
    color: #94a3b8;
}

/* Primary Button (Moviy) */
QPushButton.btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1d4ed8, stop:1 #2563eb);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e40af, stop:1 #1d4ed8);
}

/* Success Button (Yashil) */
QPushButton.btn_success {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #047857, stop:1 #059669);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_success:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #065f46, stop:1 #047857);
}

/* Danger Button (Qizil) */
QPushButton.btn_danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b91c1c, stop:1 #dc2626);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #991b1b, stop:1 #b91c1c);
}

/* Warning Button (Sariq) */
QPushButton.btn_warning {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b45309, stop:1 #d97706);
    color: #ffffff;
    font-weight: 700;
}

QPushButton.btn_warning:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #92400e, stop:1 #b45309);
}

/* Filter Pill Button */
QPushButton.pill_btn {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 3px 10px;
    color: #475569;
    font-size: 11px;
    font-weight: 600;
    min-height: 16px;
}

QPushButton.pill_btn:hover {
    background-color: #f1f5f9;
    color: #0f172a;
    border-color: #94a3b8;
}

QPushButton.pill_btn:checked, QPushButton.pill_btn.active {
    background-color: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
}

/* ========== JADVAL (QTableView & QTableWidget) ========== */
QTableView, QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    color: #0f172a;
    selection-background-color: #dbeafe;
    selection-color: #1e40af;
    font-size: 11.5px;
    outline: none;
}

QTableView::item {
    padding: 4px 6px;
    border: none;
}

QTableView::item:selected {
    background-color: #dbeafe;
    color: #1e40af;
    font-weight: 600;
}

QTableView::item:hover {
    background-color: #f1f5f9;
}

QHeaderView::section {
    background-color: #f1f5f9;
    color: #475569;
    padding: 5px 8px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

QHeaderView::section:hover {
    background-color: #e2e8f0;
    color: #0f172a;
}

QTableCornerButton::section {
    background-color: #f1f5f9;
    border: none;
    border-bottom: 2px solid #e2e8f0;
}

/* ========== SILLIQ ZAMONAVIY SCROLLBAR ========== */
QScrollBar:vertical {
    border: none;
    background: #f8fafc;
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 24px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {
    background: none;
    border: none;
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #f8fafc;
    height: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal {
    background: #cbd5e1;
    min-width: 24px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}

QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal,
QScrollBar::sub-page:horizontal, QScrollBar::add-page:horizontal {
    background: none;
    border: none;
    width: 0px;
}

/* ========== KONTEKST MENYU (QMenu) ========== */
QMenu {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 4px 0px;
}

QMenu::item {
    padding: 6px 18px 6px 12px;
    color: #1e293b;
    font-size: 11.5px;
    font-weight: 500;
}

QMenu::item:selected {
    background-color: #eff6ff;
    color: #2563eb;
}

QMenu::separator {
    height: 1px;
    background: #e2e8f0;
    margin: 3px 6px;
}

/* ========== STATUS BAR ========== */
QStatusBar {
    background-color: #ffffff;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    font-size: 11px;
    min-height: 24px;
    padding: 1px 8px;
}

QStatusBar QLabel {
    color: #64748b;
    font-size: 11px;
}

/* ========== DIALOG VA TABVIEW ========== */
QTabWidget::pane {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background-color: #ffffff;
    top: -1px;
}

QTabBar::tab {
    background-color: #f1f5f9;
    color: #64748b;
    padding: 6px 14px;
    margin-right: 3px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    font-size: 11px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #2563eb;
    border: 1px solid #e2e8f0;
    border-bottom: none;
}

QTabBar::tab:hover:!selected {
    background-color: #e2e8f0;
    color: #0f172a;
}

QGroupBox {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    font-size: 12px;
    font-weight: 700;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #0284c7;
}
"""

def get_stylesheet(theme: str = "dark") -> str:
    """Belgilangan mavzu (Dark yoki Light) uchun to'liq QSS stilini qaytaradi."""
    return DARK_THEME if theme.lower() == "dark" else LIGHT_THEME
