"""
ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5).
Senior-darajadagi zamonaviy statistika kartalari, toifalar taqsimoti va tezkor amallar.
"""
from typing import Any, List, Dict
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QHeaderView, QTableWidget,
    QTableWidgetItem
)
from PyQt5.QtCore import Qt
from core.config import THEMES

class DashboardView(QWidget):
    """PyQt5 Zamonaviy Dashboard Ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(12)

        # Skroll maydoni
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(14)

        # 1. HEADER (Sarlavha + Xush kelibsiz banneri)
        head_banner = QFrame()
        head_banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a8a, stop:0.5 #1e40af, stop:1 #2563eb);
                border-radius: 8px;
                padding: 8px 14px;
            }
        """)
        h_layout = QHBoxLayout(head_banner)
        h_layout.setContentsMargins(12, 8, 12, 8)

        banner_text = QVBoxLayout()
        banner_text.setSpacing(2)
        title = QLabel("Pop Tumani Tashkilotlari va INN Tizimi")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #ffffff;")
        sub = QLabel("Raqamli boshqaruv, Mahalla 'Yettiligi' 360° Pasporti va ma'lumotlar bazasi")
        sub.setStyleSheet("font-size: 11px; color: #bfdbfe; font-weight: 500;")
        banner_text.addWidget(title)
        banner_text.addWidget(sub)
        h_layout.addLayout(banner_text)

        h_layout.addStretch()

        btn_new_org = QPushButton("➕ Yangi Qo'shish")
        btn_new_org.setStyleSheet("""
            background-color: #ffffff;
            color: #1e40af;
            font-size: 11.5px;
            font-weight: 800;
            padding: 6px 14px;
            border-radius: 6px;
        """)
        btn_new_org.clicked.connect(self.app.open_add_dialog)
        h_layout.addWidget(btn_new_org)

        c_layout.addWidget(head_banner)

        # 2. STATISTIKA KARTALARI GRIDI
        self.cards_grid = QGridLayout()
        self.cards_grid.setSpacing(10)
        c_layout.addLayout(self.cards_grid)

        # 3. TEZKOR AMALLAR PANELI
        actions_box = QVBoxLayout()
        actions_box.setSpacing(8)
        act_title = QLabel("⚡ Tezkor Amallar va Xizmatlar")
        act_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #f1f5f9;")
        actions_box.addWidget(act_title)

        act_grid = QHBoxLayout()
        act_grid.setSpacing(10)

        def make_action_card(title, desc, icon, color, callback):
            card = QPushButton()
            card.setStyleSheet(f"""
                QPushButton {{
                    background-color: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 8px;
                    padding: 8px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    border: 1.5px solid {color};
                    background-color: #243248;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(6, 6, 6, 6)
            card_layout.setSpacing(3)

            top = QHBoxLayout()
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet(f"font-size: 18px; background: {color}22; border-radius: 6px; padding: 2px 6px;")
            top.addWidget(icon_lbl)
            top.addStretch()
            card_layout.addLayout(top)

            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #ffffff;")
            d_lbl = QLabel(desc)
            d_lbl.setStyleSheet("font-size: 10px; color: #94a3b8;")
            card_layout.addWidget(t_lbl)
            card_layout.addWidget(d_lbl)

            card.clicked.connect(callback)
            return card

        card_pasport = make_action_card(
            "Mahalla Pasporti", "7 ta xodim kartasi",
            "🏘", "#3b82f6", self.app.open_yettilik
        )
        card_msg = make_action_card(
            "Ommaviy Xabarnoma", "SMS / Telegram xabar",
            "📢", "#06b6d4", self.app.open_broadcast
        )
        card_import = make_action_card(
            "Excel Import", "Yangi bazani yuklash",
            "📥", "#10b981", self.app.open_import
        )
        card_history = make_action_card(
            "Kadrlar Tarixi", "Rotatsiya auditi",
            "📜", "#8b5cf6", self.app.open_history
        )

        act_grid.addWidget(card_pasport)
        act_grid.addWidget(card_msg)
        act_grid.addWidget(card_import)
        act_grid.addWidget(card_history)
        actions_box.addLayout(act_grid)
        c_layout.addLayout(actions_box)

        # 4. SO'NGGI QO'SHILGANLAR / PREVIEW
        recent_box = QVBoxLayout()
        recent_box.setSpacing(6)
        recent_head = QHBoxLayout()
        r_title = QLabel("📋 So'nggi Tashkilotlar")
        r_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #f1f5f9;")
        recent_head.addWidget(r_title)

        recent_head.addStretch()
        btn_all = QPushButton("Barchasini ko'rish →")
        btn_all.setStyleSheet("background: transparent; color: #38bdf8; font-weight: 700; font-size: 11.5px; border: none;")
        btn_all.clicked.connect(self.app.show_table)
        recent_head.addWidget(btn_all)
        recent_box.addLayout(recent_head)

        self.table_recent = QTableWidget()
        self.table_recent.setColumnCount(5)
        self.table_recent.setHorizontalHeaderLabels(["№", "Turi", "Tashkilot Nomi", "Mas'ul F.I.SH", "INN"])
        self.table_recent.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_recent.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_recent.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_recent.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_recent.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table_recent.setMaximumHeight(160)
        recent_box.addWidget(self.table_recent)

        c_layout.addLayout(recent_box)

        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)

    def update_stats(self):
        """Statistika kartalarini va jadvalni to'ldirish."""
        if not self.app or not hasattr(self.app, "data"):
            return

        data = self.app.data
        total_count = len(data)

        # Kategoriya bo'yicha hisoblash
        counts = {
            "Mahalla (MFY)": 0,
            "Maktab": 0,
            "Bog'cha (MTT)": 0,
            "Tibbiyot": 0,
            "Boshqa": 0
        }

        for item in data:
            s_val = str(item.get("s", "")).strip()
            if "Mahalla" in s_val or "MFY" in s_val:
                counts["Mahalla (MFY)"] += 1
            elif "Maktab" in s_val:
                counts["Maktab"] += 1
            elif "Bog'cha" in s_val or "MTT" in s_val:
                counts["Bog'cha (MTT)"] += 1
            elif "Tibbiyot" in s_val:
                counts["Tibbiyot"] += 1
            else:
                counts["Boshqa"] += 1

        # Kartalarni tozalash
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stat_items = [
            ("Jami Tashkilotlar", total_count, "🏢", "#2563eb", "Barchasi"),
            ("Mahallalar (MFY)", counts["Mahalla (MFY)"], "🏘", "#10b981", "Mahalla (MFY)"),
            ("Maktablar", counts["Maktab"], "🏫", "#f59e0b", "Maktab"),
            ("Bog'chalar (MTT)", counts["Bog'cha (MTT)"], "🧸", "#8b5cf6", "Bog'cha (MTT)"),
            ("Tibbiyot Muassasalari", counts["Tibbiyot"], "🏥", "#ec4899", "Tibbiyot"),
            ("Boshqa Tashkilotlar", counts["Boshqa"], "📌", "#06b6d4", "Boshqa"),
        ]

        for idx, (title, count, icon, color, cat_key) in enumerate(stat_items):
            card = self.create_stat_card(title, count, icon, color, cat_key)
            r = idx // 3
            c = idx % 3
            self.cards_grid.addWidget(card, r, c)

        # So'nggi tashkilotlar jadvalini to'ldirish (oxirgi 8 ta)
        recent_items = data[-8:] if len(data) > 8 else data[:]
        recent_items.reverse()
        self.table_recent.setRowCount(len(recent_items))
        for r_idx, it in enumerate(recent_items):
            self.table_recent.setItem(r_idx, 0, QTableWidgetItem(str(r_idx + 1)))
            self.table_recent.setItem(r_idx, 1, QTableWidgetItem(str(it.get("s", "-"))))
            self.table_recent.setItem(r_idx, 2, QTableWidgetItem(str(it.get("m", "-"))))
            self.table_recent.setItem(r_idx, 3, QTableWidgetItem(str(it.get("f", "-"))))
            self.table_recent.setItem(r_idx, 4, QTableWidgetItem(str(it.get("inn", "-"))))

    def create_stat_card(self, title, count, icon, color, cat_key):
        card = QPushButton()
        card.setStyleSheet(f"""
            QPushButton {{
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 10px;
                text-align: left;
            }}
            QPushButton:hover {{
                border: 1.5px solid {color};
                background-color: #243248;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(2)

        top = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 16px; background: {color}22; border-radius: 6px; padding: 2px 5px;")
        top.addWidget(icon_lbl)
        top.addStretch()

        badge = QLabel("Ko'rish →")
        badge.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748b;")
        top.addWidget(badge)
        layout.addLayout(top)

        val_lbl = QLabel(str(count))
        val_lbl.setStyleSheet(f"font-size: 19px; font-weight: 800; color: {color};")
        layout.addWidget(val_lbl)

        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 11.5px; font-weight: 600; color: #94a3b8;")
        layout.addWidget(t_lbl)

        card.clicked.connect(lambda: self.on_card_click(cat_key))
        return card

    def on_card_click(self, cat_key):
        if hasattr(self.app, "filter_by_category"):
            self.app.filter_by_category(cat_key)

def render_dashboard(parent: Any, app: Any):
    view = DashboardView(parent=parent, app=app)
    return view
