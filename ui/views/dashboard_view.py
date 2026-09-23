import tkinter as tk
from typing import Any
import customtkinter as ctk
from PIL import Image, ImageTk
from core.config import THEMES, CHART_COLORS, ICON_PATH

def render_dashboard(parent: tk.Widget, app: Any) -> None:
    """Boshqaruv paneli (Dashboard) sahifasini chizish."""
    t = THEMES[app.current_theme]

    # Asosiy aylanuvchi konteyner
    scroll_dash = ctk.CTkScrollableFrame(parent, fg_color="transparent")
    scroll_dash.pack(fill="both", expand=True)

    # Sarlavha paneli
    head_frame = ctk.CTkFrame(scroll_dash, fg_color=t["content_bg"])
    head_frame.pack(fill="x", padx=40, pady=(30, 20))

    tk.Label(
        head_frame,
        text="Boshqaruv Paneli",
        font=app.head_font,
        bg=t["content_bg"],
        fg=t["text"]
    ).pack(side="left")

    # Logo
    try:
        dash_img = Image.open(ICON_PATH).resize((100, 100))
        dash_photo = ImageTk.PhotoImage(dash_img)
        lbl = tk.Label(head_frame, image=dash_photo, bg=t["content_bg"])
        lbl.image = dash_photo
        lbl.pack(side="right")
    except Exception:
        pass

    # Ajratilgan ramka (Chap: Kartalar, O'ng: Diagramma)
    split_frame = ctk.CTkFrame(scroll_dash, fg_color=t["content_bg"])
    split_frame.pack(fill="x", padx=30)

    # CHAP: STATISTIKA KARTALARI
    left_side = ctk.CTkFrame(split_frame, fg_color=t["content_bg"])
    left_side.pack(side="left", fill="both", expand=True)

    # 1. Jami tashkilotlar
    create_modern_card(left_side, "Jami Tashkilotlar", len(app.data), "#2c3e50", "🏢", app, pady=10)

    # To'g'ridan-to'g'ri jadvalni ochish tugmasi
    ctk.CTkButton(
        left_side,
        text=f"📋 Barcha Tashkilotlar Ro'yxatini Ochish ({len(app.data)} ta)",
        command=lambda: (app.cat_var.set("Barchasi"), app.show_table()),
        fg_color="#2563eb",
        hover_color="#1d4ed8",
        height=38,
        font=("Segoe UI", 12, "bold")
    ).pack(fill="x", pady=(0, 10))

    # Grid Container
    grid_frame = ctk.CTkFrame(left_side, fg_color="transparent")
    grid_frame.pack(fill="both", expand=True, pady=10)

    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_columnconfigure(1, weight=1)
    grid_frame.grid_columnconfigure(2, weight=1)

    chart_data = []
    total_categorized = 0

    for idx, cat in enumerate(app.data_manager.categories):
        count = 0
        for item in app.data:
            s_val = str(item.get("s", "")).strip()
            is_match = (s_val == cat)
            if not is_match:
                if cat == "Mahalla (MFY)" and s_val in ["Mahalla", "MFY"]: is_match = True
                elif cat == "Maktab" and s_val in ["Maktablar"]: is_match = True
                elif cat == "Bog'cha (MTT)" and s_val in ["MTT", "Bog'cha"]: is_match = True
            if is_match:
                count += 1

        total_categorized += count
        col = CHART_COLORS[idx % len(CHART_COLORS)]
        chart_data.append((cat, count, col))

        icon = "📌"
        if "Mahalla" in cat: icon = "🏘"
        elif "Maktab" in cat: icon = "🏫"
        elif "Bog'cha" in cat: icon = "🧸"

        r = idx // 3
        c = idx % 3
        create_grid_card(grid_frame, cat, count, col, icon, r, c, app)

    # Qo'shimcha kategoriyasiz qolganlar
    total_items = len(app.data)
    if total_categorized < total_items:
        diff = total_items - total_categorized
        chart_data.append(("Boshqa (Kategoriyasiz)", diff, "#95a5a6"))

    # O'NG: DIAGRAMMA (DONUT CHART)
    right_side = tk.Frame(split_frame, bg=t["content_bg"])
    right_side.pack(side="right", padx=20, fill="y")

    draw_donut_chart(right_side, chart_data, app)

    # SO'NGGI FAOLIYAT
    tk.Label(
        scroll_dash,
        text="So'nggi Faoliyat",
        font=("Segoe UI", int(app.font_size * 1.2), "bold"),
        bg=t["content_bg"],
        fg=t["text"]
    ).pack(anchor="w", padx=40, pady=(40, 15))

    log_frame = tk.Frame(scroll_dash, bg=t["card_bg"], highlightbackground="#e2e8f0", highlightthickness=1)
    log_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))

    row_col = "#f1f5f9" if app.current_theme == "light" else "#334155"
    recent_logs = app.data_manager.activity_log[:5] if app.data_manager.activity_log else []

    if not recent_logs:
        for _ in range(3):
            f = tk.Frame(log_frame, bg=t["card_bg"])
            f.pack(fill="x", pady=1)
            tk.Label(f, text="• Tizim faoliyatga tayyor", font=("Segoe UI", int(app.font_size * 0.9)), bg=t["card_bg"], fg=t["text"]).pack(side="left", padx=15, pady=12)
            tk.Frame(log_frame, height=1, bg=row_col).pack(fill="x")
    else:
        for log in recent_logs:
            f = tk.Frame(log_frame, bg=t["card_bg"])
            f.pack(fill="x", pady=1)
            txt = f"• {log.get('user', '?').upper()}: {log.get('action')} - {log.get('details')}"
            tk.Label(f, text=txt, font=("Segoe UI", int(app.font_size * 0.9)), bg=t["card_bg"], fg=t["text"]).pack(side="left", padx=15, pady=12)
            tk.Label(f, text=str(log.get("time", ""))[-8:], font=("Segoe UI", int(app.font_size * 0.7)), bg=t["card_bg"], fg="#94a3b8").pack(side="right", padx=15)
            tk.Frame(log_frame, height=1, bg=row_col).pack(fill="x")

def create_modern_card(parent: tk.Widget, title: str, value: int, color: str, icon: str, app: Any, pady: int = 5) -> None:
    t = THEMES[app.current_theme]
    card_border = tk.Frame(parent, bg="#e2e8f0" if app.current_theme == "light" else "#334155", padx=1, pady=1)
    card_border.pack(side="top", fill="x", expand=True, pady=pady)

    card = tk.Frame(card_border, bg=t["card_bg"])
    card.pack(fill="both", expand=True)

    tk.Frame(card, bg=color, width=4).pack(side="left", fill="y")

    content = tk.Frame(card, bg=t["card_bg"], padx=15, pady=15)
    content.pack(fill="both", expand=True)

    icon_lbl = tk.Label(content, text=icon, font=("Segoe UI", 18), bg=t["card_bg"], fg=color)
    icon_lbl.pack(side="left", anchor="center")

    info = tk.Frame(content, bg=t["card_bg"])
    info.pack(side="left", padx=(15, 0))
    lbl_title = tk.Label(info, text=title, font=("Segoe UI", int(app.font_size * 0.6), "bold"), fg="#64748b", bg=t["card_bg"])
    lbl_title.pack(anchor="w")
    lbl_val = tk.Label(info, text=str(value), font=("Segoe UI", int(app.font_size * 1.2), "bold"), fg=t["text"], bg=t["card_bg"])
    lbl_val.pack(anchor="w")

    def on_click(e):
        app.cat_var.set("Barchasi")
        app.show_table()
        app.filter_data()

    for w in [card, content, icon_lbl, info, lbl_title, lbl_val]:
        w.bind("<Button-1>", on_click)
        try: w.configure(cursor="hand2")
        except Exception: pass

def create_grid_card(parent: tk.Widget, title: str, value: int, color: str, icon: str, row: int, col: int, app: Any) -> ctk.CTkFrame:
    t = THEMES[app.current_theme]
    card = ctk.CTkFrame(parent, fg_color=t["card_bg"], corner_radius=8)

    def on_click(e):
        app.filter_from_chart(title)

    bar = tk.Frame(card, bg=color, width=4)
    bar.pack(side="left", fill="y", padx=(0, 5))

    lbl_icon = tk.Label(card, text=icon, font=("Segoe UI", 18), bg=t["card_bg"], fg=color)
    lbl_icon.pack(side="left", padx=5)

    info_frame = tk.Frame(card, bg=t["card_bg"])
    info_frame.pack(side="left", fill="both", expand=True, pady=10, padx=5)

    lbl_title = tk.Label(info_frame, text=title, font=("Segoe UI", int(app.font_size * 0.85), "bold"), fg="#64748b", bg=t["card_bg"], anchor="w")
    lbl_title.pack(fill="x")

    lbl_val = tk.Label(info_frame, text=str(value), font=("Segoe UI", int(app.font_size * 1.4), "bold"), fg=t["text"], bg=t["card_bg"], anchor="w")
    lbl_val.pack(fill="x")

    for w in [card, bar, lbl_icon, info_frame, lbl_title, lbl_val]:
        w.bind("<Button-1>", on_click)
        try: w.configure(cursor="hand2")
        except Exception: pass

    card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    return card

def draw_donut_chart(parent: tk.Widget, data: list, app: Any) -> None:
    t = THEMES[app.current_theme]
    sz = 340
    canvas = tk.Canvas(parent, width=sz, height=sz, bg=t["content_bg"], bd=0, highlightthickness=0)
    canvas.pack()

    total = sum(d[1] for d in data)
    if total == 0:
        canvas.create_text(sz/2, sz/2, text="Ma'lumot yo'q", font=("Segoe UI", 12), fill="gray")
        return

    start_deg = 90
    center = sz / 2
    radius = 120
    width = 40

    legend_frame = tk.Frame(parent, bg=t["content_bg"])
    legend_frame.pack(pady=(10, 0))

    data_items = []
    for name, val, col in data:
        percent = (val / total * 100) if total > 0 else 0

        if val > 0:
            extent = (val / total) * 360
            tag_name = f"slice_{name}"
            safe_tag = "".join(x for x in tag_name if x.isalnum())

            canvas.create_arc(
                center-radius, center-radius, center+radius, center+radius,
                start=start_deg, extent=-extent, style="arc", outline=col, width=width,
                tags=(safe_tag, "slice")
            )
            canvas.tag_bind(safe_tag, "<Button-1>", lambda e, n=name: app.filter_from_chart(n))
            data_items.append((name, val, col, safe_tag))
            start_deg -= extent

        l_row = tk.Frame(legend_frame, bg=t["content_bg"])
        l_row.pack(anchor="w", pady=1)

        tk.Frame(l_row, bg=col, width=10, height=10).pack(side="left", padx=(0, 5))
        tk.Label(l_row, text=f"{name}:", font=("Segoe UI", int(app.font_size*0.9), "bold"), bg=t["content_bg"], fg=t["text"]).pack(side="left")
        tk.Label(l_row, text=f"{val} ({percent:.1f}%)", font=("Segoe UI", int(app.font_size*0.9)), bg=t["content_bg"], fg="#64748b").pack(side="left", padx=5)

    c_title = canvas.create_text(center, center-15, text="Statistika", font=("Segoe UI", int(app.font_size*0.9), "bold"), fill="#94a3b8")
    c_val = canvas.create_text(center, center+20, text=f"{total}", font=("Segoe UI", int(app.font_size*1.8), "bold"), fill=t["text"])

    def on_enter(e, tag, name, val):
        canvas.itemconfigure(tag, width=width+10)
        canvas.config(cursor="hand2")
        canvas.itemconfigure(c_title, text=name)
        canvas.itemconfigure(c_val, text=str(val))

    def on_leave(e, tag):
        canvas.itemconfigure(tag, width=width)
        canvas.config(cursor="")
        canvas.itemconfigure(c_title, text="Statistika")
        canvas.itemconfigure(c_val, text=str(total))

    for name, val, col, s_tag in data_items:
        canvas.tag_bind(s_tag, "<Enter>", lambda e, t=s_tag, n=name, v=val: on_enter(e, t, n, v))
        canvas.tag_bind(s_tag, "<Leave>", lambda e, t=s_tag: on_leave(e, t))

    tk.Label(parent, text="(Bo'limni ko'rish uchun diagrammaga bosing)", font=("Segoe UI", max(8, int(app.font_size*0.5))), bg=t["content_bg"], fg="#94a3b8").pack(pady=5)
