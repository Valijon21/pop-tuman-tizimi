"""
ui_qt.components.smart_completer: Zamonaviy va Aqlli Qidiruv Auto-Complete (Takliflar) Tizimi.
QLineEdit uchun to'liq moslashgan, substring bo'yicha tezkor qidiruvchi (Qt.MatchContains),
Dark va Light mavzuga moslashgan qidiruv takliflari popapi.
"""
from typing import List, Optional, Callable
from PyQt5.QtWidgets import QCompleter, QLineEdit, QListView
from PyQt5.QtCore import Qt, QStringListModel


def get_completer_popup_style(theme: str = "dark") -> str:
    """Auto-complete popapining Fluent UI uslubidagi stylesheeti."""
    is_light = (theme == "light")
    if is_light:
        return """
            QListView {
                background-color: #ffffff;
                color: #0f172a;
                border: 1.5px solid #0284c7;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                font-weight: 600;
                outline: none;
            }
            QListView::item {
                padding: 6px 12px;
                border-radius: 6px;
                margin: 1px 2px;
            }
            QListView::item:hover {
                background-color: #f0f9ff;
                color: #0284c7;
            }
            QListView::item:selected {
                background-color: #0284c7;
                color: #ffffff;
            }
        """
    else:
        return """
            QListView {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1.5px solid #38bdf8;
                border-radius: 8px;
                padding: 4px;
                font-size: 12px;
                font-weight: 600;
                outline: none;
            }
            QListView::item {
                padding: 6px 12px;
                border-radius: 6px;
                margin: 1px 2px;
            }
            QListView::item:hover {
                background-color: #334155;
                color: #38bdf8;
            }
            QListView::item:selected {
                background-color: #0284c7;
                color: #ffffff;
            }
        """


class SmartSearchCompleter(QCompleter):
    """Senior darajadagi aqlli qidiruv takliflari (Auto-complete) klassi."""

    def __init__(self, parent=None, items: Optional[List[str]] = None, theme: str = "dark"):
        self.model_str = QStringListModel(items or [], parent)
        super().__init__(self.model_str, parent)
        self.theme = theme

        # Ichki sozlamalar
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setMaxVisibleItems(10)

        # Popapni stilizatsiya qilish
        popup = self.popup()
        if popup:
            popup.setStyleSheet(get_completer_popup_style(self.theme))
            popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            popup.setCursor(Qt.PointingHandCursor)

    def set_theme(self, theme: str):
        """Mavzuni yangilash (Dark / Light)."""
        self.theme = theme
        popup = self.popup()
        if popup:
            popup.setStyleSheet(get_completer_popup_style(theme))

    def update_items(self, items: List[str]):
        """Takliflar ro'yxatini tezkor yangilash."""
        unique_items = list(dict.fromkeys(items))
        self.model_str.setStringList(unique_items)


def attach_smart_completer(
    line_edit: QLineEdit,
    items: List[str],
    theme: str = "dark",
    on_selected: Optional[Callable[[str], None]] = None
) -> SmartSearchCompleter:
    """
    Ixtiyoriy QLineEdit maydoniga aqlli qidiruv auto-complete tizimini biriktirish.
    """
    completer = SmartSearchCompleter(parent=line_edit, items=items, theme=theme)
    line_edit.setCompleter(completer)

    def handle_activated(text: str):
        # Agar "203599806 — Chorkesar MFY" formatida bo'lsa, chiroyli qidiruv so'zini qo'yish
        clean_text = text
        if " — " in text:
            parts = text.split(" — ")
            clean_text = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        line_edit.setText(clean_text)
        if on_selected:
            on_selected(clean_text)

    completer.activated[str].connect(handle_activated)
    return completer
