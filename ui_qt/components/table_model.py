"""
ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel.
60 FPS tezlik, xotirani tejash, saralash va dinamik maxsus ustunlar qo'llab-quvvatlashi.
"""
from typing import List, Dict, Any, Optional, Tuple
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant

class OrganizationTableModel(QAbstractTableModel):
    """Tashkilotlar jadvali uchun maxsus optimallashgan Qt Model (Dinamik ustunlar bilan)."""

    BASE_COLUMNS: List[Tuple[str, int, str]] = [
        ("№", 50, "_idx"),
        ("Turi", 110, "s"),
        ("Tashkilot Nomi", 280, "m"),
        ("F.I.SH", 210, "f"),
        ("Telefon", 130, "t"),
        ("INN", 100, "inn"),
        ("Izoh", 220, "izoh"),
    ]

    # Orqaga moslik (Backward compatibility)
    COLUMNS = [(c[0], c[1]) for c in BASE_COLUMNS]
    FIELD_KEYS = [c[2] for c in BASE_COLUMNS]

    def __init__(self, data: Optional[List[Dict[str, Any]]] = None, custom_columns: Optional[List[Dict[str, Any]]] = None):
        super().__init__()
        self._data: List[Dict[str, Any]] = data or []
        self._sort_column: int = -1
        self._sort_order: Qt.SortOrder = Qt.AscendingOrder
        self.on_izoh_changed = None
        self.on_cell_changed = None
        self._custom_columns: List[Dict[str, Any]] = custom_columns or []

    def get_all_columns(self) -> List[Tuple[str, int, str]]:
        """Baza va maxsus qo'shilgan barcha ustunlar ro'yxatini olish."""
        cols = list(self.BASE_COLUMNS)
        for cc in self._custom_columns:
            name = str(cc.get("name", "Ustun"))
            width = int(cc.get("width", 150))
            key = str(cc.get("key", ""))
            cols.append((name, width, key))
        return cols

    def set_custom_columns(self, custom_columns: List[Dict[str, Any]]) -> None:
        """Dinamik ustunlar ro'yxatini yangilash va jadvalni qayta render qilish."""
        self.beginResetModel()
        self._custom_columns = list(custom_columns)
        self.endResetModel()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        base_flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        col = index.column()
        # Izoh (col 6) yoki maxsus qo'shilgan ustunlar (col >= 7) tahrirlanuvchan
        if col == 6 or col >= len(self.BASE_COLUMNS):
            return base_flags | Qt.ItemIsEditable
        return base_flags

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False

        row = index.row()
        col = index.column()
        if 0 <= row < len(self._data):
            cols = self.get_all_columns()
            if 0 <= col < len(cols):
                _, _, col_key = cols[col]
                if col_key == "izoh" or col >= len(self.BASE_COLUMNS):
                    new_val = str(value or "").strip()
                    item = self._data[row]
                    old_val = str(item.get(col_key) or "").strip()
                    if new_val != old_val:
                        item[col_key] = new_val
                        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
                        if col_key == "izoh" and self.on_izoh_changed and callable(self.on_izoh_changed):
                            self.on_izoh_changed(item, new_val)
                        if self.on_cell_changed and callable(self.on_cell_changed):
                            self.on_cell_changed(item, col_key, new_val)
                    return True
        return False

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self.get_all_columns())

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return QVariant()

        row = index.row()
        col = index.column()

        if row < 0 or row >= len(self._data):
            return QVariant()

        item = self._data[row]
        cols = self.get_all_columns()
        if col < 0 or col >= len(cols):
            return QVariant()

        _, _, col_key = cols[col]

        if role == Qt.DisplayRole:
            if col_key == "_idx":
                return str(row + 1)
            val = item.get(col_key)
            if val is None:
                return "-" if col < len(self.BASE_COLUMNS) - 1 else ""
            val_str = str(val).strip()
            if not val_str:
                return "-" if col < len(self.BASE_COLUMNS) - 1 else ""
            return val_str

        elif role == Qt.TextAlignmentRole:
            if col_key in ("_idx", "s", "t", "inn", "bux_tel", "aparat_soni", "ulangan_soni"):
                return Qt.AlignCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.ToolTipRole:
            lines = [f"{c[0]}: {item.get(c[2], '-')}" for c in cols if c[2] != "_idx"]
            return "\n".join(lines[:10])

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            cols = self.get_all_columns()
            if 0 <= section < len(cols):
                return cols[section][0]
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
        """Jadval ustunlari bo'yicha professional saralash (barcha ustunlar uchun)."""
        if not self._data:
            return

        cols = self.get_all_columns()
        if column < 0 or column >= len(cols):
            return

        self.layoutAboutToBeChanged.emit()
        self._sort_column = column
        self._sort_order = order

        reverse = (order == Qt.DescendingOrder)
        _, _, col_key = cols[column]

        if col_key == "_idx":
            pass
        elif col_key == "inn":
            def inn_key(x):
                val = str(x.get("inn", "")).strip()
                return int(val) if val.isdigit() else 0
            self._data.sort(key=inn_key, reverse=reverse)
        elif col_key in ("aparat_soni", "ulangan_soni"):
            def num_key(x):
                val = x.get(col_key)
                try:
                    return int(val) if val not in (None, "") else -1
                except Exception:
                    return -1
            self._data.sort(key=num_key, reverse=reverse)
        else:
            self._data.sort(key=lambda x: str(x.get(col_key, "") or "").lower(), reverse=reverse)

        self.layoutChanged.emit()
