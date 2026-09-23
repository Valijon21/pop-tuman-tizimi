"""
Pop Tuman Tashkilotlari va INN Tizimi
Mahalla "Yettiligi" Birlashgan Pasporti (Mahalla 360° Passport View)
Tanlangan mahalladagi 7 ta asosiy mas'ul xodimni yaxlit tizimda ko'rish va boshqarish.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pyperclip
from typing import Any, Dict, List, Optional

from core.config import THEMES
from services.verification_service import build_verification_text
from services.qr_service import generate_phone_qr_image, clean_phone_number
from PIL import ImageTk

# 7 ta asosiy lavozim
ROLES_ORDER = [
    ("Mahalla raisi", ["Mahalla", "MFY", "Mahalla (MFY)"], "🏛", "#2563eb"),
    ("Hokim yordamchisi", ["Hokim yordamchisi"], "💼", "#f59e0b"),
    ("Yoshlar yetakchisi", ["Yoshlar yetakchisi"], "🚀", "#10b981"),
    ("Xotin-qizlar faoli", ["Xotin qizlar", "Xotin-qizlar"], "🌸", "#ec4899"),
    ("Ijtimoiy xodim", ["Ijtimoiy xodim", "Ijtimoiy"], "🤝", "#8b5cf6"),
    ("Profilaktika inspektori", ["Profilaktika", "Inspektor", "Ichki ishlar"], "👮", "#0284c7"),
    ("Soliq inspektori", ["Soliq", "Moliya"], "📊", "#059669")
]

def open_mahalla_passport(app: Any, mahalla_name: Optional[str] = None) -> None:
    """Mahalla 'Yettiligi' 360° Pasport dialog oynasi."""
    # Barcha mahallalar ro'yxatini shakllantirish
    all_mahallas = set()
    for item in app.data:
        m_name = str(item.get("m", "")).strip()
        s_val = str(item.get("s", "")).strip()
        if "MFY" in m_name or "Mahalla" in s_val or "Hokim yordamchisi" in s_val:
            all_mahallas.add(m_name)

    mahalla_list = sorted(list(all_mahallas))
    if not mahalla_list:
        mahalla_list = ["Chorkesar MFY", "Yakkatut MFY", "Bog'ishamol MFY"]

    if not mahalla_name or mahalla_name not in mahalla_list:
        mahalla_name = mahalla_list[0]

    win = ctk.CTkToplevel(app.root)
    win.title(f"Mahalla Yettiligi: {mahalla_name}")
    win.geometry("900x720")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 450
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 360
    win.geometry(f"+{x}+{y}")

    # Yuqori sarlavha va Mahalla tanlash
    header = ctk.CTkFrame(win, fg_color="transparent")
    header.pack(fill="x", padx=30, pady=(20, 10))

    ctk.CTkLabel(header, text="🏘 Mahalla 'Yettiligi' Pasporti", font=("Segoe UI", 22, "bold"), text_color=("#1e3a8a", "#60a5fa")).pack(side="left")

    sel_frame = ctk.CTkFrame(header, fg_color="transparent")
    sel_frame.pack(side="right")
    ctk.CTkLabel(sel_frame, text="Mahallani tanlang:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=5)
    
    cb_mahalla = ctk.CTkComboBox(sel_frame, values=mahalla_list, width=220, height=35, font=("Segoe UI", 13))
    cb_mahalla.set(mahalla_name)
    cb_mahalla.pack(side="left")

    # Kontent konteyneri
    cards_container = ctk.CTkScrollableFrame(win, fg_color="transparent")
    cards_container.pack(fill="both", expand=True, padx=30, pady=10)

    def render_yettilik(selected_m: str):
        # Eskilarni tozalash
        for w in cards_container.winfo_children():
            w.destroy()

        win.title(f"Mahalla Yettiligi: {selected_m}")

        # O'sha mahallaga tegishli yozuvlarni topish
        m_items = [i for i in app.data if str(i.get("m", "")).strip().lower() == selected_m.lower()]

        grid = ctk.CTkFrame(cards_container, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        summary_rows = []

        for idx, (role_title, aliases, icon, color) in enumerate(ROLES_ORDER):
            # Mos xodimni qidirish
            assigned_item = None
            for item in m_items:
                s_val = str(item.get("s", "")).strip()
                if any(alias.lower() in s_val.lower() for alias in aliases):
                    assigned_item = item
                    break

            r = idx // 2
            c = idx % 2

            card = ctk.CTkFrame(grid, fg_color=("white", "#1e293b"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#334155"))
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

            # Rangli chap chiziq
            tk.Frame(card, bg=color, width=5).pack(side="left", fill="y")

            c_content = ctk.CTkFrame(card, fg_color="transparent")
            c_content.pack(fill="both", expand=True, padx=12, pady=10)

            # Lavozim sarlavhasi
            top_bar = ctk.CTkFrame(c_content, fg_color="transparent")
            top_bar.pack(fill="x")
            ctk.CTkLabel(top_bar, text=f"{icon} {role_title}", font=("Segoe UI", 14, "bold"), text_color=color).pack(side="left")

            if assigned_item:
                fio = assigned_item.get("f") or "(F.I.SH kiritilmagan)"
                tel = assigned_item.get("t") or "-"
                inn = assigned_item.get("inn") or "-"
                jshr = assigned_item.get("jshr") or "-"
                
                status_lbl = ctk.CTkLabel(top_bar, text="● Tayinlangan", font=("Segoe UI", 11, "bold"), text_color="#10b981")
                status_lbl.pack(side="right")

                ctk.CTkLabel(c_content, text=fio, font=("Segoe UI", 13, "bold"), anchor="w").pack(fill="x", pady=(5, 2))
                
                info_text = f"📞 {tel}  |  🆔 INN: {inn}"
                if jshr != "-": info_text += f"  |  JSHR: {jshr}"
                ctk.CTkLabel(c_content, text=info_text, font=("Segoe UI", 11), text_color="gray", anchor="w").pack(fill="x")

                summary_rows.append(f"{role_title}: {fio} ({tel}, INN: {inn})")

                # Tezkor amallar
                act_row = ctk.CTkFrame(c_content, fg_color="transparent")
                act_row.pack(fill="x", pady=(8, 0))

                def make_copy_verif(it=assigned_item):
                    txt = build_verification_text(it)
                    pyperclip.copy(txt)
                    app.show_toast(f"✅ {it.get('f', '')} verifikatsiya matni nusxalandi!", "success")

                def make_show_qr(it=assigned_item):
                    cl = clean_phone_number(it.get("t", ""))
                    if not cl:
                        messagebox.showwarning("Telefon", "Telefon raqami yo'q!")
                        return
                    img = generate_phone_qr_image(cl, size=200)
                    qw = tk.Toplevel(win)
                    qw.title(f"QR: {it.get('f')}")
                    qw.geometry("260x320")
                    ph = ImageTk.PhotoImage(img)
                    lbl = tk.Label(qw, image=ph)
                    lbl.image = ph
                    lbl.pack(pady=15)
                    tk.Label(qw, text=it.get("f", ""), font=("Segoe UI", 11, "bold")).pack()
                    tk.Label(qw, text=cl, font=("Segoe UI", 13, "bold"), fg="#10b981").pack()

                ctk.CTkButton(act_row, text="🛡 Verifikatsiya", command=make_copy_verif, height=28, width=105, font=("Segoe UI", 11, "bold"), fg_color="#2563eb").pack(side="left", padx=2)
                ctk.CTkButton(act_row, text="📱 QR", command=make_show_qr, height=28, width=65, font=("Segoe UI", 11), fg_color="#f59e0b").pack(side="left", padx=2)
                ctk.CTkButton(act_row, text="📞 Nusxa", command=lambda t=tel: (pyperclip.copy(t), app.show_toast("Telefon nusxalandi!")), height=28, width=75, font=("Segoe UI", 11), fg_color="#64748b").pack(side="left", padx=2)
            else:
                ctk.CTkLabel(top_bar, text="○ Vakant (Bo'sh)", font=("Segoe UI", 11, "bold"), text_color="#ef4444").pack(side="right")
                ctk.CTkLabel(c_content, text="Xodim biriktirilmagan", font=("Segoe UI", 12), text_color="gray", anchor="w").pack(fill="x", pady=10)
                summary_rows.append(f"{role_title}: Vakant (Bo'sh)")

        # Pastki umumiy tugmalar
        btn_bar = ctk.CTkFrame(cards_container, fg_color="transparent")
        btn_bar.pack(fill="x", pady=(20, 10))

        def copy_full_passport():
            header_txt = f"🏛 {selected_m} YETTILIGI PASPORTI:\n" + ("="*40) + "\n"
            full_text = header_txt + "\n".join(summary_rows)
            pyperclip.copy(full_text)
            app.show_toast(f"✅ {selected_m} to'liq pasporti nusxalandi!", "success")

        ctk.CTkButton(btn_bar, text="📋 To'liq Pasportni Nusxalash", command=copy_full_passport, height=38, font=("Segoe UI", 13, "bold"), fg_color="#10b981", hover_color="#059669").pack(side="left", padx=5)

    cb_mahalla.configure(command=render_yettilik)
    render_yettilik(mahalla_name)

    # Pastki yopish tugmasi
    footer = ctk.CTkFrame(win, fg_color="transparent")
    footer.pack(fill="x", padx=30, pady=(0, 20))
    ctk.CTkButton(footer, text="Yopish", command=win.destroy, fg_color="#64748b", hover_color="#475569", width=100, height=36).pack(side="right")
