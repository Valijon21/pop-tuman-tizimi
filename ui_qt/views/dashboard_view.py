"""
ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5).
Senior-darajadagi zamonaviy statistika kartalari, 60 FPS vektorli interaktiv diagrammalar,
toifalar taqsimoti, tezkor amallar va so'nggi audit jurnali.
Kunduzgi (Light) va Tungi (Dark) rejimlarni to'liq, mukammal qo'llab-quvvatlaydi.
"""
from typing import Any, List, Dict, Tuple
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QHeaderView, QTableWidget,
    QTableWidgetItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from core.config import ICON_PATH
from ui_qt.components.widgets import (
    ClickableCard, CategoryDonutChart, CategoryLegend, CategoryBarChart
)
from ui_qt.styles import hex_to_rgba, create_crisp_pixmap

class DashboardView(QWidget):
    """PyQt5 Zamonaviy, Professional Dashboard Ekrani."""

    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.current_theme: str = getattr(app, "current_theme", "dark")
        self.action_cards: List[Tuple[ClickableCard, QLabel, QLabel]] = []
        self.kpi_items: List[Tuple[QFrame, QLabel, QLabel]] = []
        self.setup_ui()
        self.update_stats()
        # Dastlabki mavzuni qo'llash
        self.set_theme(self.current_theme)

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
        self.head_banner = QFrame()
        self.head_banner.setObjectName("dashboard_hero")
        h_layout = QHBoxLayout(self.head_banner)
        h_layout.setContentsMargins(16, 12, 16, 12)
        h_layout.setSpacing(14)

        if os.path.exists(ICON_PATH):
            self.lbl_hero_icon = QLabel()
            pix = create_crisp_pixmap(ICON_PATH, target_width=48, target_height=48, supersample=3.0)
            self.lbl_hero_icon.setPixmap(pix)
            self.lbl_hero_icon.setStyleSheet(
                "background: rgba(255, 255, 255, 0.08); "
                "border: 1px solid rgba(255, 255, 255, 0.16); "
                "border-radius: 10px; "
                "padding: 3px;"
            )
            h_layout.addWidget(self.lbl_hero_icon)

        banner_text = QVBoxLayout()
        banner_text.setSpacing(3)
        self.title_lbl = QLabel("Pop Tumani Tashkilotlari va INN Tizimi")
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 800; color: #ffffff; letter-spacing: 0.3px;")
        self.sub_lbl = QLabel("Raqamli boshqaruv, Mahalla 'Yettiligi' 360° Pasporti va tahliliy monitoring markazi")
        self.sub_lbl.setStyleSheet("font-size: 11px; color: #bfdbfe; font-weight: 500;")
        banner_text.addWidget(self.title_lbl)
        banner_text.addWidget(self.sub_lbl)
        h_layout.addLayout(banner_text, 1)

        # Holat belgisi
        self.status_pill = QLabel("🟢 SQLite WAL | Tizim Faol")
        self.status_pill.setStyleSheet("""
            color: #ffffff;
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 700;
        """)
        h_layout.addWidget(self.status_pill)

        # Yangi qo'shish tugmasi
        btn_new_org = QPushButton("➕ Yangi Tashkilot")
        btn_new_org.setCursor(Qt.PointingHandCursor)
        btn_new_org.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e40af;
                font-size: 12px;
                font-weight: 700;
                padding: 7px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                color: #1d4ed8;
            }
        """)
        if self.app and hasattr(self.app, "open_add_dialog"):
            btn_new_org.clicked.connect(self.app.open_add_dialog)
        h_layout.addWidget(btn_new_org)

        c_layout.addWidget(self.head_banner)

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
        d_card_layout = QVBoxLayout(self.donut_card)
        d_card_layout.setContentsMargins(12, 10, 12, 10)
        d_card_layout.setSpacing(8)

        d_head = QHBoxLayout()
        self.d_title = QLabel("📊 Tashkilotlar Toifaviy Taqsimoti")
        d_head.addWidget(self.d_title)
        d_head.addStretch()
        self.d_hint = QLabel("💡 Saralash uchun toifani bosing")
        d_head.addWidget(self.d_hint)
        d_card_layout.addLayout(d_head)

        d_body = QHBoxLayout()
        d_body.setSpacing(8)

        # Donut Chart vidjeti
        self.donut_chart = CategoryDonutChart(theme=self.current_theme)
        self.donut_chart.setMinimumSize(190, 180)
        self.donut_chart.category_clicked.connect(self.on_card_click)
        d_body.addWidget(self.donut_chart, 1)

        # Legend vidjeti
        self.legend = CategoryLegend(theme=self.current_theme)
        self.legend.category_selected.connect(self.on_card_click)
        d_body.addWidget(self.legend, 1)

        d_card_layout.addLayout(d_body)
        analytics_layout.addWidget(self.donut_card, 6)

        # 3.2. O'ng Panel: Gorizontal Bar Chart + Tizim Quvvati
        self.bar_card = QFrame()
        self.bar_card.setObjectName("bar_card")
        b_card_layout = QVBoxLayout(self.bar_card)
        b_card_layout.setContentsMargins(12, 10, 12, 10)
        b_card_layout.setSpacing(8)

        self.b_title = QLabel("📈 Sohalar Salmog'i va Qamrovi")
        b_card_layout.addWidget(self.b_title)

        # Gorizontal solishtirma bar chart
        self.bar_chart = CategoryBarChart(theme=self.current_theme)
        b_card_layout.addWidget(self.bar_chart, 1)

        # Mini KPI ko'rsatkichlari paneli
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(6)

        def make_mini_kpi(txt_val, txt_sub, col):
            f = QFrame()
            l = QVBoxLayout(f)
            l.setContentsMargins(4, 2, 4, 2)
            l.setSpacing(0)
            v = QLabel(txt_val)
            v.setStyleSheet(f"font-size: 12px; font-weight: 800; color: {col};")
            v.setAlignment(Qt.AlignCenter)
            s = QLabel(txt_sub)
            s.setAlignment(Qt.AlignCenter)
            l.addWidget(v)
            l.addWidget(s)
            return (f, v, s)

        self.kpi_mfy = make_mini_kpi("74 MFY", "Mahallalar", "#10b981")
        self.kpi_edu = make_mini_kpi("133 ta", "Maktab + MTT", "#f59e0b")
        self.kpi_status = make_mini_kpi("100%", "Audit Holati", "#38bdf8")

        self.kpi_items = [self.kpi_mfy, self.kpi_edu, self.kpi_status]

        kpi_row.addWidget(self.kpi_mfy[0])
        kpi_row.addWidget(self.kpi_edu[0])
        kpi_row.addWidget(self.kpi_status[0])
        b_card_layout.addLayout(kpi_row)

        analytics_layout.addWidget(self.bar_card, 4)
        c_layout.addLayout(analytics_layout)

        # 4. TEZKOR AMALLAR PANELI (QUICK ACTIONS)
        actions_box = QVBoxLayout()
        actions_box.setSpacing(6)
        self.act_title = QLabel("⚡ Tezkor Xizmatlar va Modullar")
        actions_box.addWidget(self.act_title)

        act_grid = QHBoxLayout()
        act_grid.setSpacing(10)

        def make_action_card(title, desc, icon, color, callback):
            card = ClickableCard(hover_color=color, theme=self.current_theme)
            card.setMinimumHeight(76)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 10, 12, 10)
            card_layout.setSpacing(4)

            top = QHBoxLayout()
            top.setContentsMargins(0, 0, 0, 0)
            icon_bg = hex_to_rgba(color, 0.12 if self.current_theme == "light" else 0.18)
            icon_border = hex_to_rgba(color, 0.25 if self.current_theme == "light" else 0.35)
            icon_lbl = QLabel(icon)
            icon_lbl.setFixedSize(30, 30)
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setStyleSheet(f"font-size: 14px; background: {icon_bg}; border: 1px solid {icon_border}; border-radius: 7px;")
            top.addWidget(icon_lbl)
            top.addStretch()

            badge_bg = hex_to_rgba(color, 0.08 if self.current_theme == "light" else 0.12)
            go_lbl = QLabel("Kirish →")
            go_lbl.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {badge_bg}; border-radius: 4px; padding: 2px 6px;")
            top.addWidget(go_lbl)
            card_layout.addLayout(top)

            t_lbl = QLabel(title)
            d_lbl = QLabel(desc)
            card_layout.addWidget(t_lbl)
            card_layout.addWidget(d_lbl)

            card.clicked.connect(callback)
            self.action_cards.append((card, t_lbl, d_lbl))
            return card

        card_pasport = make_action_card(
            "Mahalla Pasporti", "7 ta xodim kartasi va QR kod",
            "🏘", "#3b82f6", getattr(self.app, "open_yettilik", lambda: None)
        )
        card_msg = make_action_card(
            "Ommaviy Xabarnoma", "SMS va Telegram xabar",
            "📢", "#06b6d4", getattr(self.app, "open_broadcast", lambda: None)
        )
        card_import = make_action_card(
            "Excel Import", "Yangi bazani yuklash",
            "📥", "#10b981", getattr(self.app, "open_import", lambda: None)
        )
        card_history = make_action_card(
            "Kadrlar Tarixi", "Rotatsiya va audit jurnali",
            "📜", "#8b5cf6", getattr(self.app, "open_history", lambda: None)
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
        self.r_title = QLabel("📋 So'nggi Tashkilotlar")
        recent_head.addWidget(self.r_title)

        recent_head.addStretch()
        self.btn_all = QPushButton("Barchasini ko'rish →")
        self.btn_all.setCursor(Qt.PointingHandCursor)
        self.btn_all.setStyleSheet("background: transparent; color: #38bdf8; font-weight: 700; font-size: 12px; border: none;")
        if hasattr(self.app, "show_table"):
            self.btn_all.clicked.connect(self.app.show_table)
        recent_head.addWidget(self.btn_all)
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
        self.table_recent.setMinimumHeight(190)
        self.table_recent.setMaximumHeight(230)
        self.table_recent.doubleClicked.connect(lambda: self.app.show_table())
        recent_box.addWidget(self.table_recent)

        c_layout.addLayout(recent_box)

        scroll.setWidget(container)
        main_layout.addWidget(scroll, 1)

    def set_theme(self, theme: str):
        """
        Dashboard'ning barcha vidjetlarini (kartalar, diagrammalar, sarlavhalar)
        tanlangan mavzuga (dark / light) to'liq moslashtirish.
        """
        self.current_theme = theme
        is_light = (theme == "light")

        # 1. Hero banner
        if is_light:
            self.head_banner.setStyleSheet("""
                QFrame#dashboard_hero {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1d4ed8, stop:0.6 #2563eb, stop:1 #3b82f6);
                    border: 1px solid #60a5fa;
                    border-radius: 8px;
                }
            """)
        else:
            self.head_banner.setStyleSheet("""
                QFrame#dashboard_hero {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a8a, stop:0.6 #1e40af, stop:1 #2563eb);
                    border: 1px solid #3b82f6;
                    border-radius: 8px;
                }
            """)

        # 2. Donut va Bar kartalarining foni va chegarasi
        card_bg = "#ffffff" if is_light else "#1e293b"
        card_border = "#e2e8f0" if is_light else "#334155"
        self.donut_card.setStyleSheet(f"""
            QFrame#donut_card {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 8px;
            }}
        """)
        self.bar_card.setStyleSheet(f"""
            QFrame#bar_card {{
                background-color: {card_bg};
                border: 1px solid {card_border};
                border-radius: 8px;
            }}
        """)

        # 3. Sarlavha yozuvlarining rangi
        title_col = "#0f172a" if is_light else "#f1f5f9"
        self.d_title.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {title_col};")
        self.b_title.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {title_col};")
        self.act_title.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {title_col};")
        self.r_title.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {title_col};")
        self.d_hint.setStyleSheet(f"font-size: 11px; color: {'#64748b' if is_light else '#94a3b8'}; font-style: italic;")

        if hasattr(self, "btn_all"):
            self.btn_all.setStyleSheet(f"background: transparent; color: {'#0284c7' if is_light else '#38bdf8'}; font-weight: 700; font-size: 12px; border: none;")

        # 4. Ichki vidjetlar (Donut, Legend, Bar)
        self.donut_chart.set_theme(theme)
        self.legend.set_theme(theme)
        self.bar_chart.set_theme(theme)

        # 5. Mini KPI bloklari
        for f, v, s in self.kpi_items:
            if is_light:
                f.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 4px;")
                s.setStyleSheet("font-size: 10px; color: #64748b; font-weight: 600;")
            else:
                f.setStyleSheet("background-color: #172233; border: 1px solid #243248; border-radius: 6px; padding: 4px;")
                s.setStyleSheet("font-size: 10px; color: #94a3b8; font-weight: 600;")

        # 6. Tezkor amallar kartalari
        for card, t_lbl, d_lbl in self.action_cards:
            card.set_theme(theme)
            if is_light:
                t_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #0f172a;")
                d_lbl.setStyleSheet("font-size: 11px; color: #64748b;")
            else:
                t_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #ffffff;")
                d_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")

        # 7. Stat kartalarini yangilash
        self.update_stats()

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

        # 1. Kartalarni tozalash va qayta yaratish (ClickableCard - tanlangan mavzuda)
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        stat_items = [
            ("Jami Tashkilotlar", total_count, "🏢", ("#38bdf8", "#0284c7"), "Barchasi"),
            ("Mahallalar (MFY)", counts["Mahalla (MFY)"], "🏘", ("#34d399", "#059669"), "Mahalla (MFY)"),
            ("Maktablar", counts["Maktab"], "🏫", ("#fbbf24", "#d97706"), "Maktab"),
            ("Bog'chalar (MTT)", counts["Bog'cha (MTT)"], "🧸", ("#a78bfa", "#7c3aed"), "Bog'cha (MTT)"),
            ("Tibbiyot Muassasalari", counts["Tibbiyot"], "🏥", ("#f472b6", "#db2777"), "Tibbiyot"),
            ("Boshqa Tashkilotlar", counts["Boshqa"], "📌", ("#22d3ee", "#0891b2"), "Boshqa"),
        ]

        for idx, (title, count, icon, color_spec, cat_key) in enumerate(stat_items):
            card = self.create_stat_card(title, count, icon, color_spec, cat_key)
            r = idx // 3
            c = idx % 3
            self.cards_grid.addWidget(card, r, c)

        # 2. Diagrammalar ma'lumotlarini yangilash
        is_light = (self.current_theme == "light")
        chart_data = [
            ("Mahalla (MFY)", counts["Mahalla (MFY)"], "#059669" if is_light else "#10b981"),
            ("Maktablar", counts["Maktab"], "#d97706" if is_light else "#f59e0b"),
            ("Bog'chalar (MTT)", counts["Bog'cha (MTT)"], "#7c3aed" if is_light else "#8b5cf6"),
            ("Tibbiyot", counts["Tibbiyot"], "#db2777" if is_light else "#ec4899"),
            ("Boshqa", counts["Boshqa"], "#0891b2" if is_light else "#06b6d4"),
        ]
        self.donut_chart.set_data(chart_data)
        self.legend.set_data(chart_data)
        self.bar_chart.set_data(chart_data)

        # Mini KPI ko'rsatkichlarini dinamik yangilash
        if hasattr(self, "kpi_mfy") and self.kpi_mfy:
            mfy_cnt = counts.get("Mahalla (MFY)", 0)
            edu_cnt = counts.get("Maktab", 0) + counts.get("Bog'cha (MTT)", 0)
            with_inn_cnt = sum(1 for it in data if str(it.get("inn", "")).strip())
            inn_pct = int((with_inn_cnt / total_count * 100)) if total_count > 0 else 0

            self.kpi_mfy[1].setText(f"{mfy_cnt} MFY")
            self.kpi_edu[1].setText(f"{edu_cnt} ta")
            self.kpi_status[1].setText(f"{inn_pct}%")
            self.kpi_status[2].setText("INN Qamrovi")

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

    def create_stat_card(self, title: str, count: int, icon: str, color_spec: Any, cat_key: str) -> ClickableCard:
        """
        Senior-darajadagi zamonaviy, mukammal balanslangan KPI statistika kartasi.
        Maydon 4 burchakka proporsional taqsimlangan:
        - Yuqori chap: Toifa nomi (12px, semi-bold)
        - Yuqori o'ng: Nafis ixcham nishon (30x30, 14px emoji squircle)
        - Quyi chap: Katta va qalin raqamli ko'rsatkich (26px, 800)
        - Quyi o'ng: 'Ko'rish →' interaktiv tugma nishoni
        """
        is_light = (self.current_theme == "light")
        if isinstance(color_spec, (tuple, list)):
            color = color_spec[1] if is_light else color_spec[0]
        else:
            color = color_spec

        card = ClickableCard(hover_color=color, theme=self.current_theme)
        card.setMinimumHeight(86)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(6)

        # 1. YUQORI QATOR: Toifa nomi (chapda) + Nafis ikonka nishoni (o'ngda)
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)

        t_col = "#64748b" if is_light else "#94a3b8"
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {t_col};")
        top.addWidget(t_lbl)

        top.addStretch()

        icon_bg = hex_to_rgba(color, 0.10 if is_light else 0.15)
        icon_border = hex_to_rgba(color, 0.20 if is_light else 0.30)
        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(30, 30)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 14px; background: {icon_bg}; border: 1px solid {icon_border}; border-radius: 7px;")
        top.addWidget(icon_lbl)
        layout.addLayout(top)

        # 2. QUYI QATOR: Katta ko'rsatkich (chapda) + 'Ko'rish →' nishoni (o'ngda)
        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)

        val_lbl = QLabel(f"{count:,}".replace(",", " "))
        val_lbl.setStyleSheet(f"font-size: 26px; font-weight: 800; color: {color};")
        bottom.addWidget(val_lbl)

        bottom.addStretch()

        badge_bg = hex_to_rgba(color, 0.08 if is_light else 0.12)
        badge = QLabel("Ko'rish →")
        badge.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color}; background: {badge_bg}; border-radius: 4px; padding: 2px 8px;")
        bottom.addWidget(badge, alignment=Qt.AlignBottom)
        layout.addLayout(bottom)

        card.clicked.connect(lambda: self.on_card_click(cat_key))
        return card

    def on_card_click(self, cat_key: str):
        if hasattr(self.app, "filter_by_category"):
            self.app.filter_by_category(cat_key)

def render_dashboard(parent: Any, app: Any):
    view = DashboardView(parent=parent, app=app)
    return view
