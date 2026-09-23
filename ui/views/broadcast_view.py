"""
Pop Tuman Tashkilotlari va INN Tizimi
Ommaviy Xabarnoma Muloqot Oynasi (Broadcast Notification Dialog)
Favqulodda yig'ilish, sayyor qabul va tezkor topshiriqlar uchun ommaviy SMS va Telegram xabarnoma markazi.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pyperclip
import webbrowser
import urllib.parse
from typing import Any, List, Dict

from services.broadcast_service import (
    DEFAULT_TEMPLATES, AUDIENCE_GROUPS,
    filter_audience_recipients, extract_clean_phone_list, calculate_sms_segments
)

def open_broadcast_dialog(app: Any) -> None:
    """Ommaviy xabarnoma jo'natish dialogini ochish."""
    if not app.check_password():
        return

    win = ctk.CTkToplevel(app.root)
    win.title("Ommaviy Xabarnoma Markazi (SMS & Telegram)")
    win.geometry("820x720")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 410
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 360
    win.geometry(f"+{x}+{y}")

    # Header
    head_frame = ctk.CTkFrame(win, fg_color="transparent")
    head_frame.pack(fill="x", padx=25, pady=(20, 10))

    ctk.CTkLabel(head_frame, text="📢 Ommaviy Xabarnoma Markazi", font=("Segoe UI", 22, "bold"), text_color=("#1e3a8a", "#60a5fa")).pack(side="left")
    ctk.CTkLabel(head_frame, text="Favqulodda yig'ilish, sayyor qabul va topshiriqlar", font=("Segoe UI", 12), text_color="gray").pack(side="right", pady=(5, 0))

    # 1. Auditoriya tanlash paneli
    top_ctrl = ctk.CTkFrame(win, fg_color=("white", "#1e293b"), corner_radius=10)
    top_ctrl.pack(fill="x", padx=25, pady=(0, 10))

    ctk.CTkLabel(top_ctrl, text="Qabul qiluvchilar auditoriyasi:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, padx=15, pady=10, sticky="w")
    
    group_labels = [label for label, key in AUDIENCE_GROUPS]
    combo_group = ctk.CTkComboBox(top_ctrl, values=group_labels, width=280, height=35, font=("Segoe UI", 12))
    combo_group.set(group_labels[2])  # Default: Hokim yordamchilari
    combo_group.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(top_ctrl, text="Mahalla (ixtiyoriy):", font=("Segoe UI", 12, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="w")
    entry_mahalla = ctk.CTkEntry(top_ctrl, width=180, height=35, placeholder_text="Filtr...")
    entry_mahalla.grid(row=0, column=3, padx=10, pady=10, sticky="w")

    # 2. Shablon tanlash
    tpl_frame = ctk.CTkFrame(win, fg_color="transparent")
    tpl_frame.pack(fill="x", padx=25, pady=(0, 8))

    ctk.CTkLabel(tpl_frame, text="Shablon:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10))

    def on_tpl_select(tpl_key):
        txt_body.delete("1.0", tk.END)
        txt_body.insert("1.0", DEFAULT_TEMPLATES.get(tpl_key, ""))
        update_stats()

    ctk.CTkButton(tpl_frame, text="🚨 Favqulodda yig'ilish", command=lambda: on_tpl_select("emergency"), height=30, fg_color="#ef4444", font=("Segoe UI", 11, "bold")).pack(side="left", padx=3)
    ctk.CTkButton(tpl_frame, text="🏛 Sayyor qabul", command=lambda: on_tpl_select("reception"), height=30, fg_color="#3b82f6", font=("Segoe UI", 11, "bold")).pack(side="left", padx=3)
    ctk.CTkButton(tpl_frame, text="⚡ Tezkor topshiriq", command=lambda: on_tpl_select("urgent_task"), height=30, fg_color="#f59e0b", font=("Segoe UI", 11, "bold")).pack(side="left", padx=3)
    ctk.CTkButton(tpl_frame, text="🧹 Tozalash", command=lambda: on_tpl_select("custom"), height=30, fg_color="#64748b", font=("Segoe UI", 11)).pack(side="left", padx=3)

    # 3. Xabar matni maydoni
    msg_container = ctk.CTkFrame(win, fg_color="transparent")
    msg_container.pack(fill="x", padx=25, pady=(0, 8))

    txt_body = tk.Text(msg_container, height=5, font=("Segoe UI", 12), bg="#1e293b", fg="#f8fafc", bd=0, padx=12, pady=10)
    txt_body.pack(fill="x", pady=(0, 5))
    txt_body.insert("1.0", DEFAULT_TEMPLATES["emergency"])

    # Xabar statistikasi (SMS segmentlari & belgilar)
    lbl_sms_stat = ctk.CTkLabel(msg_container, text="", font=("Segoe UI", 11), text_color="gray", anchor="w")
    lbl_sms_stat.pack(fill="x")

    # 4. Qabul qiluvchilar jadvali
    ctk.CTkLabel(win, text="Xabarnoma yuboriladigan xodimlar ro'yxati:", font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", padx=25, pady=(5, 3))

    table_frame = ctk.CTkFrame(win)
    table_frame.pack(fill="both", expand=True, padx=25, pady=(0, 10))

    vsb = ttk.Scrollbar(table_frame, orient="vertical")
    vsb.pack(side="right", fill="y")

    cols = ("num", "role", "name", "org", "phone")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=vsb.set)
    vsb.configure(command=tree.yview)

    tree.heading("num", text="№")
    tree.heading("role", text="Lavozimi / Toifa")
    tree.heading("name", text="Mas'ul F.I.SH")
    tree.heading("org", text="Mahalla / Tashkilot")
    tree.heading("phone", text="Telefon Raqam")

    tree.column("num", width=35, anchor="center")
    tree.column("role", width=140, anchor="w")
    tree.column("name", width=190, anchor="w")
    tree.column("org", width=220, anchor="w")
    tree.column("phone", width=130, anchor="center")

    tree.pack(fill="both", expand=True)

    # Pastki hisoblagich
    current_recipients: List[Dict[str, Any]] = []

    def refresh_recipients(*args):
        nonlocal current_recipients
        sel_label = combo_group.get()
        group_key = next((k for lbl, k in AUDIENCE_GROUPS if lbl == sel_label), "all")
        m_filter = entry_mahalla.get().strip()

        current_recipients = filter_audience_recipients(app.data, group_key, m_filter)

        tree.delete(*tree.get_children())
        for idx, r in enumerate(current_recipients, 1):
            tree.insert("", "end", values=(
                idx,
                r.get("s", "-"),
                r.get("f", "-"),
                r.get("m", "-"),
                r.get("t", "-")
            ))
        update_stats()

    def update_stats(*args):
        text = txt_body.get("1.0", tk.END).strip()
        sms_info = calculate_sms_segments(text)
        phones = extract_clean_phone_list(current_recipients)
        lbl_sms_stat.configure(
            text=f"📊 Belgilar: {sms_info['length']} ta | {sms_info['parts']} ta SMS ({sms_info['encoding']}) | "
                 f"Qabul qiluvchilar: {len(current_recipients)} ta ({len(phones)} ta to'g'ri telefon raqami)"
        )

    combo_group.configure(command=refresh_recipients)
    entry_mahalla.bind("<KeyRelease>", refresh_recipients)
    txt_body.bind("<KeyRelease>", update_stats)

    refresh_recipients()

    # 5. Harakat tugmalari
    btn_bar = ctk.CTkFrame(win, fg_color="transparent")
    btn_bar.pack(fill="x", padx=25, pady=(0, 20))

    def copy_phone_numbers():
        phones = extract_clean_phone_list(current_recipients)
        if not phones:
            messagebox.showwarning("Xato", "Tanlangan guruhda telefon raqamlari topilmadi!")
            return
        result = ", ".join(phones)
        pyperclip.copy(result)
        app.show_toast(f"✅ {len(phones)} ta telefon raqami nusxalandi!", "success")

    def copy_message_and_numbers():
        text = txt_body.get("1.0", tk.END).strip()
        phones = extract_clean_phone_list(current_recipients)
        full_payload = f"XABAR:\n{text}\n\nQABUL QILUVCHILAR ({len(phones)} ta):\n" + "\n".join(phones)
        pyperclip.copy(full_payload)
        app.show_toast("✅ Xabar va barcha telefonlar nusxalandi!", "success")

    def send_via_telegram_bot():
        text = txt_body.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Xato", "Xabar matni bo'sh bo'lishi mumkin emas!")
            return

        bot_token = app.data_manager.settings.get("telegram_bot_token", "")
        if not bot_token:
            if messagebox.askyesno("Bot Tokeni Topilmadi", "Telegram bot tokeni sozlanmagan. Sozlamalar bo'limiga o'tasizmi?"):
                win.destroy()
                app.show_settings()
            return

        from services.telegram_bot import TelegramBotService
        bot_service = TelegramBotService(bot_token, app.data_manager)
        res = bot_service.broadcast_message(f"📢 <b>RASMIY BILDIRISHNOMA</b>\n\n{text}")
        if res["total"] == 0:
            messagebox.showinfo("Obunachilar yo'q", "Botga hali hech kim /start bosib ulanmagan. Mas'ullar avval botga /start yuborishi kerak.")
        else:
            app.show_toast(f"✅ {res['sent']} ta Telegram obunachiga yuborildi!", "success")
            messagebox.showinfo("Natija", f"Telegram orqali yuborildi:\nYetkazildi: {res['sent']} ta\nXato: {res['failed']} ta")

    def share_on_telegram():
        text = txt_body.get("1.0", tk.END).strip()
        if not text: return
        encoded = urllib.parse.quote(f"📢 RASMIY BILDIRISHNOMA:\n\n{text}")
        webbrowser.open(f"https://t.me/share/url?url={encoded}")

    ctk.CTkButton(btn_bar, text="✈ Telegram Botga Yuborish", command=send_via_telegram_bot, fg_color="#0088cc", hover_color="#006699", font=("Segoe UI", 12, "bold"), height=38).pack(side="left", padx=(0, 4))
    ctk.CTkButton(btn_bar, text="📱 SMS Raqamlarni Nusxalash", command=copy_phone_numbers, fg_color="#10b981", hover_color="#059669", font=("Segoe UI", 12, "bold"), height=38).pack(side="left", padx=4)
    ctk.CTkButton(btn_bar, text="📋 Xabar + Raqamlar", command=copy_message_and_numbers, fg_color="#2563eb", hover_color="#1d4ed8", font=("Segoe UI", 12, "bold"), height=38).pack(side="left", padx=4)
    ctk.CTkButton(btn_bar, text="🌐 Ulashish", command=share_on_telegram, fg_color="#f59e0b", hover_color="#d97706", font=("Segoe UI", 12, "bold"), height=38, width=80).pack(side="left", padx=4)
    ctk.CTkButton(btn_bar, text="Yopish", command=win.destroy, fg_color="#64748b", font=("Segoe UI", 12), height=38, width=70).pack(side="right", padx=(4, 0))
