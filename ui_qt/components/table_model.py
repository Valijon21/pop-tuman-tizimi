"""
ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel.
60 FPS tezlik, xotirani tejash va o'n minglab yozuvlarni bir zumda qayta ishlash.
"""
from typing import List, Dict, Any, Optional
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant

class OrganizationTableModel(QAbstractTableModel):
    """Tashkilotlar jadvali uchun maxsus optimallashgan Qt Model."""

    COLUMNS = [
        ("№", 50),
        ("Turi", 110),
        ("Tashkilot Nomi", 280),
        ("F.I.SH", 210),
        ("Telefon", 130),
        ("INN", 100),
        ("Izoh", 220),
    ]

    FIELD_KEYS = ["_idx", "s", "m", "f", "t", "inn", "izoh"]

    def __init__(self, data: Optional[List[Dict[str, Any]]] = None):
        super().__init__()
        self._data: List[Dict[str, Any]] = data or []
        self._sort_column: int = -1
        self._sort_order: Qt.SortOrder = Qt.AscendingOrder

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return QVariant()

        row = index.row()
        col = index.column()

        if row < 0 or row >= len(self._data):
            return QVariant()

        item = self._data[row]

        if role == Qt.DisplayRole:
            if col == 0:
                return str(row + 1)
            elif col == 1:
                return str(item.get("s", "") or "-")
            elif col == 2:
                return str(item.get("m", "") or "-")
            elif col == 3:
                return str(item.get("f", "") or "-")
            elif col == 4:
                return str(item.get("t", "") or "-")
            elif col == 5:
                return str(item.get("inn", "") or "-")
            elif col == 6:
                return str(item.get("izoh", "") or "")

        elif role == Qt.TextAlignmentRole:
            if col in (0, 1, 4, 5):
                return Qt.AlignCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.ToolTipRole:
            inn = item.get("inn", "-")
            jshr = item.get("jshr", "-")
            seriya = item.get("seriya", "-")
            lavozim = item.get("lavozim", "-")
            return (
                f"Tashkilot: {item.get('m', '-')}\n"
                f"Turi: {item.get('s', '-')}\n"
                f"Rahbar: {item.get('f', '-')}\n"
                f"Lavozimi: {lavozim}\n"
                f"Tel: {item.get('t', '-')}\n"
                f"INN: {inn}\n"
                f"JSHSHIR: {jshr}\n"
                f"Pasport: {seriya}\n"
                f"Izoh: {item.get('izoh', '-')}"
            )

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if 0 <= section < len(self.COLUMNS):
                return self.COLUMNS[section][0]
        return QVariant()

    def set_data(self, new_data: List[Dict[str, Any]]) -> None:
        """Jadval ma'lumotlarini yangilash."""
        self.beginResetModel()
        self._data = list(new_data)
        self.endResetModel()

    def get_item_by_row(self, row: int) -> Optional[Dict[str, Any]]:
        """Tanlangan qator bo'yicha tashkilot obyektini olish."""
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        """Jadval ustunlari bo'yicha professional saralash."""
        if not self._data:
            return

        self.layoutAboutToBeChanged.emit()
        self._sort_column = column
        self._sort_order = order

        reverse = (order == Qt.DescendingOrder)

        if column == 0:
            # Qator tartib raqami
            pass
        elif column == 1:
            self._data.sort(key=lambda x: str(x.get("s", "")).lower(), reverse=reverse)
        elif column == 2:
            self._data.sort(key=lambda x: str(x.get("m", "")).lower(), reverse=reverse)
        elif column == 3:
            self._data.sort(key=lambda x: str(x.get("f", "")).lower(), reverse=reverse)
        elif column == 4:
            self._data.sort(key=lambda x: str(x.get("t", "")).lower(), reverse=reverse)
        elif column == 5:
            # INN bo'yicha raqamli saralash
            def inn_key(x):
                val = str(x.get("inn", "")).strip()
                return int(val) if val.isdigit() else 0
            self._data.sort(key=inn_key, reverse=reverse)
        elif column == 6:
            self._data.sort(key=lambda x: str(x.get("izoh", "")).lower(), reverse=reverse)

        self.layoutChanged.emit()
