"""
ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari.
- ClickableCard: Matnlari siqilib qolmaydigan, to'liq boshqariladigan karta vidjeti (Dark va Light mavzuni qo'llaydi).
- CategoryDonutChart: QPainter yordamida chiziladigan zamonaviy, silliq Donut (aylana) diagrammasi.
- CategoryLegend: Interaktiv toifalar statistikasi va foiz ko'rsatkichlari.
- CategoryBarChart: Gorizontal taqsimot diagrammasi.
"""
import math
from typing import List, Tuple, Dict, Any, Optional, Callable
from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPoint
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QPaintEvent,
    QMouseEvent, QPainterPath
)

class ClickableCard(QFrame):
    """
    Tugma (QPushButton) cheklovlarisiz, matnlarni siqib qo'ymaydigan
    va to'liq dizayn nazoratiga ega bosiladigan karta vidjeti.
    Kunduzgi va tungi rejimlarni to'liq qo'llab-quvvatlaydi.
    """
    clicked = pyqtSignal()

    def __init__(self, parent=None, hover_color="#38bdf8", bg_color=None, border_color=None, theme="dark"):
        super().__init__(parent)
        self.hover_color = hover_color
        self.theme = theme
        self.custom_bg = bg_color is not None
        self.custom_border = border_color is not None
        
        if self.custom_bg:
            self.bg_color = bg_color
        else:
            self.bg_color = "#1e293b" if theme == "dark" else "#ffffff"

        if self.custom_border:
            self.border_color = border_color
        else:
            self.border_color = "#334155" if theme == "dark" else "#e2e8f0"

        self.hover_bg = "#243248" if theme == "dark" else "#f0f7ff"

        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("class", "clickable_card")
        self.update_style(False)

    def set_theme(self, theme: str):
        self.theme = theme
        if not self.custom_bg:
            self.bg_color = "#1e293b" if theme == "dark" else "#ffffff"
        if not self.custom_border:
            self.border_color = "#334155" if theme == "dark" else "#e2e8f0"
        self.hover_bg = "#243248" if theme == "dark" else "#f0f7ff"
        self.update_style(False)

    def update_style(self, is_hover: bool):
        border = self.hover_color if is_hover else self.border_color
        bg = self.hover_bg if is_hover else self.bg_color
        self.setStyleSheet(f"""
            QFrame.clickable_card {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
        """)

    def enterEvent(self, event):
        self.update_style(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_style(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class CategoryDonutChart(QWidget):
    """
    PyQt5 QPainter yordamida chiziladigan professional, 60 FPS Donut diagrammasi.
    Hech qanday og'ir tashqi kutubxonalarsiz, silliq antialiasing va markaziy ma'lumotlar bilan.
    Dark va Light rejimlarga dinamik moslashadi.
    """
    category_clicked = pyqtSignal(str)

    def __init__(self, parent=None, theme="dark"):
        super().__init__(parent)
        self.theme = theme
        self.setMinimumSize(200, 180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.segments: List[Tuple[str, int, QColor]] = []
        self.total: int = 0
        self.hovered_index: int = -1
        self.setMouseTracking(True)

    def set_theme(self, theme: str):
        self.theme = theme
        self.update()

    def set_data(self, data: List[Tuple[str, int, str]]):
        """
        data: [(nomi, soni, rang_hex), ...]
        """
        self.segments = []
        self.total = sum(item[1] for item in data)
        for cat, cnt, col_hex in data:
            if cnt > 0:
                self.segments.append((cat, cnt, QColor(col_hex)))
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        size = min(w, h) - 20
        if size <= 30:
            return

        cx = w / 2.0
        cy = h / 2.0
        outer_radius = size / 2.0
        inner_radius = outer_radius * 0.62  # Donut teshigi

        rect = QRectF(cx - outer_radius, cy - outer_radius, outer_radius * 2, outer_radius * 2)

        is_light = (self.theme == "light")

        if self.total == 0 or not self.segments:
            # Bo'sh holatdagi nozik doira
            pen_color = QColor("#e2e8f0") if is_light else QColor("#334155")
            pen = QPen(pen_color, 8)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QRectF(cx - outer_radius + 4, cy - outer_radius + 4, (outer_radius - 4) * 2, (outer_radius - 4) * 2))
            return

        start_angle = 90.0 * 16.0  # Soat 12 dan boshlash
        gap_span = 1.2 * 16.0 if len(self.segments) > 1 else 0.0

        # Bo'laklarni chizish
        for idx, (cat_name, count, color) in enumerate(self.segments):
            fraction = count / self.total
            span_angle = -(fraction * 360.0 * 16.0)

            # Silliq segment yo'li (Donut slice path)
            path = QPainterPath()
            actual_span = span_angle + (gap_span if span_angle < -gap_span else 0.0)

            path.arcMoveTo(rect, start_angle / 16.0)
            path.arcTo(rect, start_angle / 16.0, actual_span / 16.0)

            inner_rect = QRectF(cx - inner_radius, cy - inner_radius, inner_radius * 2, inner_radius * 2)
            path.arcTo(inner_rect, (start_angle + actual_span) / 16.0, -actual_span / 16.0)
            path.closeSubpath()

            draw_color = color.lighter(115) if idx == self.hovered_index else color

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(draw_color))
            painter.drawPath(path)

            start_angle += span_angle

        # Markazdagi ma'lumotlar (Total Count & Label)
        total_text_color = QColor("#0f172a") if is_light else QColor("#ffffff")
        sub_text_color = QColor("#64748b") if is_light else QColor("#94a3b8")

        painter.setPen(total_text_color)
        font_total = QFont("Segoe UI", max(13, int(outer_radius * 0.22)), QFont.Bold)
        painter.setFont(font_total)
        painter.drawText(
            QRectF(cx - inner_radius, cy - inner_radius * 0.65, inner_radius * 2, inner_radius * 0.8),
            Qt.AlignCenter, str(self.total)
        )

        painter.setPen(sub_text_color)
        font_sub = QFont("Segoe UI", max(9, int(outer_radius * 0.11)), QFont.DemiBold)
        painter.setFont(font_sub)
        painter.drawText(
            QRectF(cx - inner_radius, cy + 2, inner_radius * 2, inner_radius * 0.6),
            Qt.AlignCenter, "JAMI TASHKILOT"
        )

    def _slice_at(self, pos: QPoint) -> int:
        if self.total == 0 or not self.segments:
            return -1
        w = self.width()
        h = self.height()
        size = min(w, h) - 20
        if size <= 30:
            return -1
        cx = w / 2.0
        cy = h / 2.0
        outer_radius = size / 2.0
        inner_radius = outer_radius * 0.62

        dx = pos.x() - cx
        dy = pos.y() - cy
        dist = math.hypot(dx, dy)
        if dist < inner_radius or dist > outer_radius:
            return -1

        clock_angle = (math.degrees(math.atan2(dy, dx)) + 90.0) % 360.0
        curr = 0.0
        for idx, (cat_name, count, color) in enumerate(self.segments):
            span = (count / self.total) * 360.0
            if curr <= clock_angle <= (curr + span):
                return idx
            curr += span
        return -1

    def mouseMoveEvent(self, event: QMouseEvent):
        idx = self._slice_at(event.pos())
        if idx != self.hovered_index:
            self.hovered_index = idx
            if idx != -1:
                cat, cnt, _ = self.segments[idx]
                pct = (cnt / self.total) * 100.0
                self.setToolTip(f"<b>{cat}</b>: {cnt} ta ({pct:.1f}%)<br/><i>Bosib jadvalda saralash</i>")
                self.setCursor(Qt.PointingHandCursor)
            else:
                self.setToolTip("")
                self.setCursor(Qt.ArrowCursor)
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if self.hovered_index != -1:
            self.hovered_index = -1
            self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            idx = self._slice_at(event.pos())
            if idx != -1:
                cat_name = self.segments[idx][0]
                self.category_clicked.emit(cat_name)
        super().mousePressEvent(event)


class CategoryLegend(QWidget):
    """
    Donut diagramma yonidagi interaktiv, foizli va rangli tushuntirish paneli (Legend).
    Dark va Light mavzuni to'liq qo'llaydi.
    """
    category_selected = pyqtSignal(str)

    def __init__(self, parent=None, theme="dark"):
        super().__init__(parent)
        self.theme = theme
        self.last_data: List[Tuple[str, int, str]] = []
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(6)

    def set_theme(self, theme: str):
        self.theme = theme
        if self.last_data:
            self.set_data(self.last_data)

    def set_data(self, data: List[Tuple[str, int, str]]):
        self.last_data = data
        # Eski elementlarni tozalash
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        total = sum(x[1] for x in data)
        if total == 0:
            return

        is_light = (self.theme == "light")
        bg_card = "#f8fafc" if is_light else "#172233"
        border_card = "#e2e8f0" if is_light else "#243248"
        name_color = "#1e293b" if is_light else "#f1f5f9"
        count_color = "#0f172a" if is_light else "#ffffff"

        for cat_name, count, col_hex in data:
            if count == 0:
                continue

            pct = (count / total) * 100.0
            row_card = ClickableCard(hover_color=col_hex, bg_color=bg_card, border_color=border_card, theme=self.theme)
            row_layout = QHBoxLayout(row_card)
            row_layout.setContentsMargins(8, 4, 8, 4)
            row_layout.setSpacing(8)

            # Rangli indikator doirasi
            dot = QLabel()
            dot.setFixedSize(10, 10)
            dot.setStyleSheet(f"background-color: {col_hex}; border-radius: 5px;")
            row_layout.addWidget(dot)

            # Toifa nomi
            lbl_name = QLabel(cat_name)
            lbl_name.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {name_color};")
            row_layout.addWidget(lbl_name, 1)

            # Soni
            lbl_count = QLabel(f"{count} ta")
            lbl_count.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {count_color};")
            row_layout.addWidget(lbl_count)

            # Foiz belgisi
            lbl_pct = QLabel(f"{pct:.1f}%")
            lbl_pct.setStyleSheet(f"font-size: 10px; font-weight: 700; color: {col_hex}; background: {col_hex}15; border-radius: 4px; padding: 2px 5px;")
            row_layout.addWidget(lbl_pct)

            row_card.clicked.connect(lambda c=cat_name: self.category_selected.emit(c))
            self.layout.addWidget(row_card)

        self.layout.addStretch()


class CategoryBarChart(QWidget):
    """
    Toifalar taqsimotini solishtirish uchun zamonaviy gorizontal progress bar diagrammasi.
    Dark va Light mavzuni to'liq qo'llaydi.
    """
    def __init__(self, parent=None, theme="dark"):
        super().__init__(parent)
        self.theme = theme
        self.last_data: List[Tuple[str, int, str]] = []
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setSpacing(6)

    def set_theme(self, theme: str):
        self.theme = theme
        if self.last_data:
            self.set_data(self.last_data)

    def set_data(self, data: List[Tuple[str, int, str]]):
        self.last_data = data
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not data:
            return

        is_light = (self.theme == "light")
        lbl_name_color = "#475569" if is_light else "#94a3b8"
        track_bg = "#e2e8f0" if is_light else "#334155"

        max_count = max((x[1] for x in data), default=1)
        if max_count == 0:
            max_count = 1

        for cat_name, count, col_hex in data:
            pct = int((count / max_count) * 100)

            row = QVBoxLayout()
            row.setSpacing(2)

            top_row = QHBoxLayout()
            lbl_n = QLabel(cat_name)
            lbl_n.setStyleSheet(f"font-size: 10.5px; color: {lbl_name_color}; font-weight: 600;")
            lbl_v = QLabel(f"{count} ta")
            lbl_v.setStyleSheet(f"font-size: 10.5px; color: {col_hex}; font-weight: 700;")
            top_row.addWidget(lbl_n)
            top_row.addStretch()
            top_row.addWidget(lbl_v)
            row.addLayout(top_row)

            # Bar fon va to'ldiruvchi
            bar_bg = QFrame()
            bar_bg.setFixedHeight(5)
            bar_bg.setStyleSheet(f"background-color: {track_bg}; border-radius: 2px;")
            
            bar_layout = QHBoxLayout(bar_bg)
            bar_layout.setContentsMargins(0, 0, 0, 0)
            
            bar_fill = QFrame()
            bar_fill.setStyleSheet(f"background-color: {col_hex}; border-radius: 2px;")
            bar_layout.addWidget(bar_fill, pct)
            bar_layout.addStretch(100 - pct)

            row.addWidget(bar_bg)
            self.layout.addLayout(row)

        self.layout.addStretch()
