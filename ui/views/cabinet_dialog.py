"""
Pop Tuman Tashkilotlari va INN Tizimi
Kabinetga Dostup Dialog Oynasi (Cabinet Access Dialog)
Foydalanuvchi talabiga asosan tashkilot va xodimlar uchun shaxsiy kabinet ruxsati shabloni.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pyperclip
import webbrowser
import urllib.parse
from typing import Any, Optional, Dict

from services.cabinet_service import build_cabinet_access_text, get_cabinet_portal_url

def resolve_selected_item(app: Any, item: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Tanlangan tashkilot yozuvini aniqlash."""
    if item:
        return item
    
    if hasattr(app, "tree") and app.tree:
        sel = app.tree.focus()
        if not sel and app.tree.selection():
            sel = app.tree.selection()[0]
        if sel:
            found = next((i for i in app.data if str(i.get("id")) == sel or str(i.get("uuid")) == sel), None)
            if not found:
                v = app.tree.item(sel)["values"]
                if v and len(v) > 5:
                    inn = str(v[5])
                    found = next((i for i in app.data if str(i.get("inn")) == inn), None)
            if not found:
                v = app.tree.item(sel)["values"]
                if v and len(v) >= 7:
                    found = {"s": v[1], "m": v[2], "f": v[3], "t": v[4], "inn": v[5], "izoh": v[6]}
            if found:
                return found
    return None

def copy_cabinet_quick(app: Any, item: Optional[Dict[str, Any]] = None) -> None:
    """Tanlangan tashkilot uchun darhol 'Kabinetga dostup' matnini clipboardga nusxalash."""
    target = resolve_selected_item(app, item)
    if not target:
        app.show_toast("Iltimos, avval ro'yxatdan tashkilot yoki xodimni tanlang!", "warning")
        return

    text = build_cabinet_access_text(target)
    pyperclip.copy(text)
    app.show_toast("✅ Kabinetga dostup matni nusxalandi!", "success")

def open_cabinet_dialog(app: Any, item: Optional[Dict[str, Any]] = None) -> None:
    """Professional Kabinetga Dostup dialog oynasi."""
    target = resolve_selected_item(app, item)
    if not target:
        app.show_toast("Iltimos, avval ro'yxatdan tashkilot yoki xodimni tanlang!", "warning")
        return

    win = ctk.CTkToplevel(app.root)
    win.title("Kabinetga Dostup So'rovi")
    win.geometry("520x620")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 260
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 310
    win.geometry(f"+{x}+{y}")

    # Sarlavha
    ctk.CTkLabel(win, text="🔑 Kabinetga Dostup So'rovi", font=("Segoe UI", 20, "bold"), text_color=("#b45309", "#f59e0b")).pack(pady=(20, 5))
    ctk.CTkLabel(win, text="Shaxsiy kabinet / Ruxsat so'rovi uchun standart shablon", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 15))

    container = ctk.CTkScrollableFrame(win, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

    fields = [
        ("m", "Tashkilot nomi", target.get("m", "")),
        ("inn", "INN", target.get("inn", "")),
        ("f", "F.I.O", target.get("f", "")),
        ("action", "So'rov matni", "cabinetga dostup"),
    ]

    entries = {}
    for key, label_txt, default_val in fields:
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=4)
        ctk.CTkLabel(row, text=label_txt, font=("Segoe UI", 12, "bold"), anchor="w", width=140).pack(side="left")
        e = ctk.CTkEntry(row, font=("Segoe UI", 13), height=34)
        e.pack(side="right", fill="x", expand=True)
        e.insert(0, str(default_val or ""))
        entries[key] = e

    # Live Preview Box
    ctk.CTkLabel(container, text="📄 Shablon ko'rinishi (Jonli):", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(15, 5))

    txt_preview = tk.Text(container, height=6, font=("Consolas", 12), bg="#1e293b", fg="#38bdf8", bd=0, padx=12, pady=10)
    txt_preview.pack(fill="x", pady=(0, 10))

    def update_preview(*args):
        m_val = entries["m"].get().strip()
        inn_val = entries["inn"].get().strip()
        f_val = entries["f"].get().strip()
        act_val = entries["action"].get().strip() or "cabinetga dostup"

        simulated = {"m": m_val, "inn": inn_val, "f": f_val}
        generated = build_cabinet_access_text(simulated, action_text=act_val)
        txt_preview.config(state="normal")
        txt_preview.delete("1.0", tk.END)
        txt_preview.insert("1.0", generated)
        txt_preview.config(state="disabled")

    for e in entries.values():
        e.bind("<KeyRelease>", update_preview)

    update_preview()

    # Portal ma'lumoti
    portal_url = get_cabinet_portal_url(target.get("s", ""))
    portal_frame = ctk.CTkFrame(container, fg_color=("white", "#1e293b"), corner_radius=8)
    portal_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(portal_frame, text=f"🌐 Tavsiya etilgan portal: {portal_url}", font=("Segoe UI", 11), text_color=("#2563eb", "#60a5fa")).pack(side="left", padx=10, pady=8)

    # Tugmalar
    btn_frame = ctk.CTkFrame(win, fg_color="transparent")
    btn_frame.pack(fill="x", padx=25, pady=(0, 20))

    def do_copy():
        txt_preview.config(state="normal")
        content = txt_preview.get("1.0", tk.END).strip()
        txt_preview.config(state="disabled")
        pyperclip.copy(content)
        app.show_toast("✅ Kabinetga dostup matni nusxalandi!", "success")
        win.destroy()

    def do_send_telegram():
        txt_preview.config(state="normal")
        content = txt_preview.get("1.0", tk.END).strip()
        txt_preview.config(state="disabled")
        encoded = urllib.parse.quote(content)
        webbrowser.open(f"https://t.me/share/url?url={encoded}")

    def do_open_portal():
        webbrowser.open(portal_url)

    ctk.CTkButton(btn_frame, text="📋 Nusxalash", command=do_copy, fg_color="#d97706", hover_color="#b45309", font=("Segoe UI", 13, "bold"), height=38).pack(side="left", fill="x", expand=True, padx=(0, 4))
    ctk.CTkButton(btn_frame, text="✈ Telegram", command=do_send_telegram, fg_color="#0088cc", hover_color="#006699", font=("Segoe UI", 12, "bold"), height=38, width=105).pack(side="left", padx=4)
    ctk.CTkButton(btn_frame, text="🌐 Portal", command=do_open_portal, fg_color="#059669", hover_color="#047857", font=("Segoe UI", 12, "bold"), height=38, width=85).pack(side="left", padx=4)
    ctk.CTkButton(btn_frame, text="Yopish", command=win.destroy, fg_color="#64748b", hover_color="#475569", font=("Segoe UI", 12), height=38, width=70).pack(side="right", padx=(4, 0))
