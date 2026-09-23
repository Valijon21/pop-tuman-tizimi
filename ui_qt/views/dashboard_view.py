"""
ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5).
Senior-darajadagi zamonaviy statistika kartalari, 60 FPS vektorli interaktiv diagrammalar,
toifalar taqsimoti, tezkor amallar va so'nggi audit jurnali.
"""
from typing import Any, List, Dict, Tuple
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QHeaderView, QTableWidget,
    QTableWidgetItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from ui_qt.components.widgets import (
    ClickableCard, CategoryDonutChart, CategoryLegend, CategoryBarChart
)

class DashboardView(QWidget):
    """PyQt5 Zamonaviy, Professional Dashboard Ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.stat_cards: Dict[str, Tuple[QLabel, QLabel]] = {}
        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(10)

        # Skroll maydoni
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(0, 0, 4, 10)
        c_layout.setSpacing(12)

        # 1. HEADER (Sarlavha + Xush kelibsiz banneri)
        head_banner = QFrame()
        head_banner.setObjectName("dashboard_hero")
        head_banner.setStyleSheet("""
            QFrame#dashboard_hero {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a8a, stop:0.6 #1e40af, stop:1 #2563eb);
                border: 1px solid #3b82f6;
                border-radius: 8px;
            }
        """)
        h_layout = QHBoxLayout(head_banner)
        h_layout.setContentsMargins(16, 12, 16, 12)
        h_layout.setSpacing(14)

        banner_text = QVBoxLayout()
        banner_text.setSpacing(3)
        title = QLabel("🏛 Pop Tumani Tashkilotlari va INN Tizimi")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #ffffff; letter-spacing: 0.3px;")
        sub = QLabel("Raqamli boshqaruv, Mahalla 'Yettiligi' 360° Pasporti va tahliliy monitoring markazi")
        sub.setStyleSheet("font-size: 11px; color: #bfdbfe; font-weight: 500;")
        banner_text.addWidget(title)
        banner_text.addWidget(sub)
        h_layout.addLayout(banner_text, 1)

        # Holat belgisi
        status_pill = QLabel("🟢 SQLite WAL | Tizim Faol")
        status_pill.setStyleSheet("""
            color: #ffffff;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 700;
        """)
        h_layout.addWidget(status_pill)

        # Yangi qo'shish tugmasi
        btn_new_org = QPushButton("➕ Yangi Tashkilot")
        btn_new_org.setCursor(Qt.PointingHandCursor)
        btn_new_org.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e40af;
                font-size: 11.5px;
                font-weight: 800;
                padding: 7px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f8fafc;
                color: #1d4ed8;
            }
        """)
        btn_new_org.clicked.connect(self.app.open_add_dialog)
        h_layout.addWidget(btn_new_org)

        c_layout.addWidget(head_banner)

        # 2. STATISTIKA KARTALARI GRIDI (3x2)
        self.cards_grid = QGridLayout()
        self.cards_grid.setSpacing(10)
        c_layout.addLayout(self.cards_grid)

        # 3. TAHLILIY DIAGRAMMALAR VA TOIFALAR TAQSIMOTI (PROFESSIONAL DIAGRAMS)
        analytics_layout = QHBoxLayout()
        analytics_layout.setSpacing(10)

        # 3.1. Chap Panel: Interaktiv Donut Chart + Legend
        self.donut_card = QFrame()
        self.donut_card.setObjectName("donut_card")
        self.donut_card.setStyleSheet("""
            QFrame#donut_card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
            }
        """)
        d_card_layout = QVBoxLayout(self.donut_card)
        d_card_layout.setContentsMargins(12, 10, 12, 10)
        d_card_layout.setSpacing(8)

        d_head = QHBoxLayout()
        d_title = QLabel("📊 Tashkilotlar Toifaviy Taqsimoti")
        d_title.setStyleSheet("font-size: 12.5px; font-weight: 700; color: #f1f5f9;")
        d_head.addWidget(d_title)
        d_head.addStretch()
        d_hint = QLabel("💡 Saralash uchun toifani bosing")
        d_hint.setStyleSheet("font-size: 10px; color: #64748b; font-style: italic;")
        d_head.addWidget(d_hint)
        d_card_layout.addLayout(d_head)

        d_body = QHBoxLayout()
        d_body.setSpacing(8)

        # Donut Chart vidjeti
        self.donut_chart = CategoryDonutChart()
        self.donut_chart.setMinimumSize(190, 180)
        self.donut_chart.category_clicked.connect(self.on_card_click)
        d_body.addWidget(self.donut_chart, 1)

        # Legend vidjeti
        self.legend = CategoryLegend()
        self.legend.category_selected.connect(self.on_card_click)
        d_body.addWidget(self.legend, 1)

        d_card_layout.addLayout(d_body)
        analytics_layout.addWidget(self.donut_card, 6)

        # 3.2. O'ng Panel: Gorizontal Bar Chart + Tizim Quvvati
        self.bar_card = QFrame()
        self.bar_card.setObjectName("bar_card")
        self.bar_card.setStyleSheet("""
            QFrame#bar_card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
            }
        """)
        b_card_layout = QVBoxLayout(self.bar_card)
        b_card_layout.setContentsMargins(12, 10, 12, 10)
        b_card_layout.setSpacing(8)

        b_title = QLabel("📈 Sohalar Salmog'i va Qamrovi")
        b_title.setStyleSheet("font-size: 12.5px; font-weight: 700; color: #f1f5f9;")
        b_card_layout.addWidget(b_title)

        # Gorizontal solishtirma bar chart
        self.bar_chart = CategoryBarChart()
        b_card_layout.addWidget(self.bar_chart, 1)

        # Mini KPI ko'rsatkichlari paneli
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(6)

        def make_mini_kpi(txt_val, txt_sub, col):
            f = QFrame()
            f.setStyleSheet("background-color: #172233; border: 1px solid #243248; border-radius: 6px; padding: 4px;")
            l = QVBoxLayout(f)
            l.setContentsMargins(4, 2, 4, 2)
            l.setSpacing(0)
            v = QLabel(txt_val)
            v.setStyleSheet(f"font-size: 12px; font-weight: 800; color: {col};")
            v.setAlignment(Qt.AlignCenter)
            s = QLabel(txt_sub)
            s.setStyleSheet("font-size: 9px; color: #94a3b8; font-weight: 600;")
            s.setAlignment(Qt.AlignCenter)
            l.addWidget(v)
            l.addWidget(s)
            return f

        self.kpi_mfy = make_mini_kpi("74 MFY", "Mahallalar", "#10b981")
        self.kpi_edu = make_mini_kpi("133 ta", "Maktab + MTT", "#f59e0b")
        self.kpi_status = make_mini_kpi("100%", "Audit Holati", "#38bdf8")

        kpi_row.addWidget(self.kpi_mfy)
        kpi_row.addWidget(self.kpi_edu)
        kpi_row.addWidget(self.kpi_status)
        b_card_layout.addLayout(kpi_row)

        analytics_layout.addWidget(self.bar_card, 4)
        c_layout.addLayout(analytics_layout)

        # 4. TEZKOR AMALLAR PANELI (QUICK ACTIONS)
        actions_box = QVBoxLayout()
        actions_box.setSpacing(6)
        act_title = QLabel("⚡ Tezkor Xizmatlar va Modullar")
        act_title.setStyleSheet("font-size: 12.5px; font-weight: 700; color: #f1f5f9;")
        actions_box.addWidget(act_title)

        act_grid = QHBoxLayout()
        act_grid.setSpacing(10)

        def make_action_card(title, desc, icon, color, callback):
            card = ClickableCard(hover_color=color, bg_color="#1e293b", border_color="#334155")
            card.setMinimumHeight(68)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 8, 10, 8)
            card_layout.setSpacing(3)

            top = QHBoxLayout()
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet(f"font-size: 16px; background: {color}22; border-radius: 5px; padding: 2px 6px;")
            top.addWidget(icon_lbl)
            top.addStretch()

            go_lbl = QLabel("Kirish →")
            go_lbl.setStyleSheet(f"font-size: 9.5px; font-weight: 700; color: {color};")
            top.addWidget(go_lbl)
            card_layout.addLayout(top)

            t_lbl = QLabel(title)
            t_lbl.setStyleSheet("font-size: 11.5px; font-weight: 700; color: #ffffff;")
            d_lbl = QLabel(desc)
            d_lbl.setStyleSheet("font-size: 10px; color: #94a3b8;")
            card_layout.addWidget(t_lbl)
            card_layout.addWidget(d_lbl)

            card.clicked.connect(callback)
            return card

        card_pasport = make_action_card(
            "Mahalla Pasporti", "7 ta xodim kartasi va QR kod",
            "🏘", "#3b82f6", self.app.open_yettilik
        )
        card_msg = make_action_card(
            "Ommaviy Xabarnoma", "SMS va Telegram xabar",
            "📢", "#06b6d4", self.app.open_broadcast
        )
        card_import = make_action_card(
            "Excel Import", "Yangi bazani yuklash",
            "📥", "#10b981", self.app.open_import
        )
        card_history = make_action_card(
            "Kadrlar Tarixi", "Rotatsiya va audit jurnali",
            "📜", "#8b5cf6", self.app.open_history
        )

        act_grid.addWidget(card_pasport)
        act_grid.addWidget(card_msg)
        act_grid.addWidget(card_import)
        act_grid.addWidget(card_history)
        actions_box.addLayout(act_grid)
        c_layout.addLayout(actions_box)

        # 5. SO'NGGI QO'SHILGAN TASHKILOTLAR JADVALI
        recent_box = QVBoxLayout()
        recent_box.setSpacing(6)
        recent_head = QHBoxLayout()
        r_title = QLabel("📋 So'nggi Tashkilotlar")
        r_title.setStyleSheet("font-size: 12.5px; font-weight: 700; color: #f1f5f9;")
        recent_head.addWidget(r_title)

        recent_head.addStretch()
        btn_all = QPushButton("Barchasini ko'rish →")
        btn_all.setCursor(Qt.PointingHandCursor)
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
        self.table_recent.verticalHeader().setVisible(False)
        self.table_recent.setAlternatingRowColors(True)
        self.table_recent.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_recent.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_recent.setMaximumHeight(160)
        self.table_recent.doubleClicked.connect(lambda: self.app.show_table())
        recent_box.addWidget(self.table_recent)

        c_layout.addLayout(recent_box)

        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)

    def update_stats(self):
        """Statistika kartalarini, diagrammalarni va jadvalni to'ldirish."""
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
            elif "Tibbiyot" in s_val or "Poliklinika" in s_val or "Shifoxona" in s_val:
                counts["Tibbiyot"] += 1
            else:
                counts["Boshqa"] += 1

        # 1. Kartalarni tozalash va qayta yaratish (ClickableCard yordamida - matnlar kesilmaydi!)
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stat_items = [
            ("Jami Tashkilotlar", total_count, "🏢", "#38bdf8", "Barchasi"),
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

        # 2. Diagrammalar ma'lumotlarini yangilash
        chart_data = [
            ("Mahalla (MFY)", counts["Mahalla (MFY)"], "#10b981"),
            ("Maktablar", counts["Maktab"], "#f59e0b"),
            ("Bog'chalar (MTT)", counts["Bog'cha (MTT)"], "#8b5cf6"),
            ("Tibbiyot", counts["Tibbiyot"], "#ec4899"),
            ("Boshqa", counts["Boshqa"], "#06b6d4"),
        ]
        self.donut_chart.set_data(chart_data)
        self.legend.set_data(chart_data)
        self.bar_chart.set_data(chart_data)

        # 3. So'nggi tashkilotlar jadvalini to'ldirish (oxirgi 8 ta)
        recent_items = data[-8:] if len(data) > 8 else data[:]
        recent_items.reverse()
        self.table_recent.setRowCount(len(recent_items))
        for r_idx, it in enumerate(recent_items):
            item_num = QTableWidgetItem(str(r_idx + 1))
            item_num.setTextAlignment(Qt.AlignCenter)
            self.table_recent.setItem(r_idx, 0, item_num)

            item_type = QTableWidgetItem(str(it.get("s", "-")))
            self.table_recent.setItem(r_idx, 1, item_type)

            item_name = QTableWidgetItem(str(it.get("m", "-")))
            item_name.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table_recent.setItem(r_idx, 2, item_name)

            item_fio = QTableWidgetItem(str(it.get("f", "-")))
            item_fio.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table_recent.setItem(r_idx, 3, item_fio)

            item_inn = QTableWidgetItem(str(it.get("inn", "-")))
            item_inn.setTextAlignment(Qt.AlignCenter)
            self.table_recent.setItem(r_idx, 4, item_inn)

            self.table_recent.setRowHeight(r_idx, 27)

    def create_stat_card(self, title: str, count: int, icon: str, color: str, cat_key: str) -> ClickableCard:
        """
        QFrame asosidagi ClickableCard vidjeti.
        QPushButton cheklovlaridan holi, matnlar va raqamlar hech qachon siqilmaydi.
        """
        card = ClickableCard(hover_color=color, bg_color="#1e293b", border_color="#334155")
        card.setMinimumHeight(76)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        # Yuqori qator: Ikonka va Ko'rish havolasi
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 14px; background: {color}22; border-radius: 5px; padding: 2px 5px;")
        top.addWidget(icon_lbl)
        
        top.addStretch()

        badge = QLabel("Ko'rish →")
        badge.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748b;")
        top.addWidget(badge)
        layout.addLayout(top)

        # Raqamli ko'rsatkich (Katta va qalin)
        val_lbl = QLabel(str(count))
        val_lbl.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {color}; margin-top: 1px;")
        layout.addWidget(val_lbl)

        # Toifa nomi
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 10.5px; font-weight: 700; color: #94a3b8; text-transform: uppercase;")
        layout.addWidget(t_lbl)

        card.clicked.connect(lambda: self.on_card_click(cat_key))
        return card

    def on_card_click(self, cat_key: str):
        if hasattr(self.app, "filter_by_category"):
            self.app.filter_by_category(cat_key)

def render_dashboard(parent: Any, app: Any):
    view = DashboardView(parent=parent, app=app)
    return view
