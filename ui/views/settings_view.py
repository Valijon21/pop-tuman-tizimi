import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from typing import Any
from core.security import hash_password

def render_settings(parent: tk.Widget, app: Any) -> None:
    """Sozlamalar (Settings) sahifasini ko'rsatish."""
    ctk.CTkLabel(
        parent,
        text="Sozlamalar",
        font=("Segoe UI", 26, "bold"),
        text_color=("#2c3e50", "white")
    ).pack(anchor="w", padx=30, pady=20)

    # Tablar
    tabs = ctk.CTkTabview(parent)
    tabs.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    tab_cat = tabs.add("Kategoriyalar")
    tab_font = tabs.add("Ko'rinish (Shrift)")
    tab_log = tabs.add("Tarix (Logs)")
    tab_tools = tabs.add("Asboblar (Tools)")

    # --- TAB 1: KATEGORIYALAR ---
    add_frame = ctk.CTkFrame(tab_cat)
    add_frame.pack(fill="x", padx=10, pady=10)

    new_cat_var = tk.StringVar()
    ctk.CTkLabel(add_frame, text="Yangi tur qo'shish:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10, pady=10)
    ctk.CTkEntry(add_frame, textvariable=new_cat_var, width=220, height=35, placeholder_text="Masalan: Hokim Yordamchilari").pack(side="left", padx=5)

    list_frame = ctk.CTkFrame(tab_cat)
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)
    scroll_cat = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
    scroll_cat.pack(fill="both", expand=True, padx=5, pady=5)

    def refresh_cat_list():
        for w in scroll_cat.winfo_children():
            w.destroy()
        for cat in app.data_manager.categories:
            r = ctk.CTkFrame(scroll_cat, fg_color=("white", "#333"), height=40)
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=cat, font=("Segoe UI", 12)).pack(side="left", padx=15, pady=5)
            if cat not in ["Mahalla (MFY)", "Maktab", "Bog'cha (MTT)"]:
                ctk.CTkButton(
                    r, text="🗑", width=30, height=30, fg_color="#c0392b",
                    command=lambda c=cat: delete_cat(c)
                ).pack(side="right", padx=5, pady=5)

    def add_cat():
        new_c = new_cat_var.get().strip()
        if not new_c:
            return
        if new_c in app.data_manager.categories:
            app.show_toast("Bu tur allaqachon mavjud!")
            return
        app.data_manager.categories.append(new_c)
        app.data_manager.save_categories()
        app.data_manager.log_activity(app.current_role, "Kategoriya Qo'shildi", f"Nomi: {new_c}")
        new_cat_var.set("")
        app.show_toast(f"'{new_c}' qo'shildi!")
        refresh_cat_list()

    def delete_cat(cat: str):
        if messagebox.askyesno("O'chirish", f"'{cat}' turini o'chirmoqchimisiz?"):
            app.data_manager.categories.remove(cat)
            app.data_manager.save_categories()
            app.data_manager.log_activity(app.current_role, "Kategoriya O'chirildi", f"Nomi: {cat}")
            refresh_cat_list()
            app.show_toast("O'chirildi!")

    ctk.CTkButton(add_frame, text="+ Qo'shish", command=add_cat, fg_color="#27ae60", width=100, height=35).pack(side="left", padx=10)
    refresh_cat_list()

    # --- TAB 2: SHRIFT O'LCHAMI ---
    font_frame = ctk.CTkFrame(tab_font, fg_color="transparent")
    font_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(font_frame, text="Dastur Shrifti O'lchami:", font=("Segoe UI", 18, "bold")).pack(pady=10)
    ctk.CTkLabel(font_frame, text="O'zgartirishlar darhol qisman qo'llaniladi, qayta ishga tushirilganda to'liq saqlanadi.", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 20))

    def set_font(size: int):
        app.data_manager.log_activity(app.current_role, "Shrift O'zgardi", f"Yangi o'lcham: {size}")
        app.change_font_size(size)
        app.show_toast(f"Shrift {size} ga o'zgardi!")

    btn_box = ctk.CTkFrame(font_frame, fg_color="transparent")
    btn_box.pack(pady=10)

    sizes = [("Kichik", 12), ("O'rta (Standard)", 15), ("Katta", 18), ("Juda Katta", 22)]
    for label, sz in sizes:
        col = "#3b82f6" if app.font_size == sz else "gray"
        ctk.CTkButton(
            btn_box, text=f"{label} ({sz})",
            command=lambda s=sz: set_font(s),
            width=150, height=45, fg_color=col, font=("Segoe UI", 14)
        ).pack(side="left", padx=10)

    manual_frame = ctk.CTkFrame(font_frame, fg_color="transparent")
    manual_frame.pack(pady=20)
    ctk.CTkLabel(manual_frame, text="Yoki aniq o'lchamni kiriting:", font=("Segoe UI", 14)).pack(side="left", padx=10)

    manual_var = tk.StringVar(value=str(app.font_size))
    entry_font = ctk.CTkEntry(manual_frame, textvariable=manual_var, width=80, font=("Segoe UI", 14))
    entry_font.pack(side="left", padx=5)

    def save_manual():
        try:
            val = int(manual_var.get())
            if val < 8 or val > 50:
                app.show_toast("O'lcham 8 va 50 orasida bo'lishi kerak!")
                return
            set_font(val)
        except Exception:
            app.show_toast("Iltimos, raqam kiriting!")

    ctk.CTkButton(manual_frame, text="✅ Qo'llash", command=save_manual, width=100, fg_color="#27ae60").pack(side="left", padx=10)

    # --- TAB 3: HARAKATLAR TARIXI (LOGS) ---
    log_frame = ctk.CTkFrame(tab_log)
    log_frame.pack(fill="both", expand=True, padx=10, pady=10)

    cols = ("time", "user", "action", "details")
    log_tree = ttk.Treeview(log_frame, columns=cols, show="headings", height=20)
    log_tree.heading("time", text="Vaqt"); log_tree.column("time", width=150, anchor="center")
    log_tree.heading("user", text="Foydalanuvchi"); log_tree.column("user", width=120, anchor="center")
    log_tree.heading("action", text="Harakat"); log_tree.column("action", width=180, anchor="w")
    log_tree.heading("details", text="Tafsilotlar"); log_tree.column("details", width=400, anchor="w")
    log_tree.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(log_frame, orient="vertical", command=log_tree.yview)
    vsb.place(relx=1, rely=0, relheight=1, anchor="ne")
    log_tree.configure(yscrollcommand=vsb.set)

    for log in app.data_manager.activity_log:
        log_tree.insert("", "end", values=(log.get("time"), log.get("user"), log.get("action"), log.get("details")))

    # --- TAB 4: ASBOBLAR (TOOLS) ---
    tools_frame = ctk.CTkFrame(tab_tools, fg_color="transparent")
    tools_frame.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(tools_frame, text="Ma'lumotlar Bazasi Asboblari", font=("Segoe UI", 18, "bold")).pack(pady=10)

    # 1. DUBLIKATLARNI TOPISH
    dup_frame = ctk.CTkFrame(tools_frame)
    dup_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(dup_frame, text="🔍 Dublikatlarni Topish (Bir xil INN)", font=("Segoe UI", 14, "bold")).pack(side="left", padx=15, pady=15)

    def find_duplicates():
        inn_map = {}
        for item in app.data:
            inn = item.get("inn")
            if inn and inn.isdigit():
                if inn not in inn_map:
                    inn_map[inn] = []
                inn_map[inn].append(item)

        duplicates = {k: v for k, v in inn_map.items() if len(v) > 1}
        if not duplicates:
            app.show_toast("Dublikatlar topilmadi! Baza toza.")
            return

        dw = ctk.CTkToplevel(app.root)
        dw.title(f"Topildi: {len(duplicates)} ta guruh")
        dw.geometry("600x500")
        dw.transient(app.root)

        ctk.CTkLabel(dw, text=f"⚠️ {len(duplicates)} ta INN bo'yicha takrorlanishlar topildi", font=("Segoe UI", 16, "bold"), text_color="#e74c3c").pack(pady=10)
        scroll_dup = ctk.CTkScrollableFrame(dw)
        scroll_dup.pack(fill="both", expand=True, padx=10, pady=10)

        for inn, items in duplicates.items():
            g_frame = ctk.CTkFrame(scroll_dup, fg_color="transparent")
            g_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(g_frame, text=f"INN: {inn} ({len(items)} ta)", font=("Segoe UI", 13, "bold")).pack(anchor="w")

            for it in items:
                r = ctk.CTkFrame(g_frame, border_width=1, border_color="gray")
                r.pack(fill="x", padx=10, pady=2)
                info = f"{it.get('m')} | {it.get('f')}"
                ctk.CTkLabel(r, text=info, font=("Segoe UI", 12)).pack(side="left", padx=5)

                def delete_dup(target=it, w=r):
                    if messagebox.askyesno("O'chirish", f"Chindan ham '{target.get('m')}' ni o'chirmoqchimisiz?"):
                        app.data_manager.move_to_trash(target)
                        w.destroy()
                        app.data_manager.log_activity(app.current_role, "Dublikat O'chirildi", f"{target.get('m')}")
                        app.filter_data()
                        app.sync_background()

                ctk.CTkButton(r, text="🗑", width=30, height=30, fg_color="#c0392b", command=delete_dup).pack(side="right", padx=5, pady=2)

    ctk.CTkButton(dup_frame, text="Tekshirish", command=find_duplicates, font=("Segoe UI", 13), width=150).pack(side="right", padx=15)

    # 2. PAROLLARNI BOSHQARISH
    pwd_frame = ctk.CTkFrame(tools_frame)
    pwd_frame.pack(fill="x", pady=10)
    ctk.CTkLabel(pwd_frame, text="🔑 Parollarni O'zgartirish (Admin / Operator)", font=("Segoe UI", 14, "bold")).pack(side="left", padx=15, pady=15)

    def open_change_pwd_dialog():
        pw_win = ctk.CTkToplevel(app.root)
        pw_win.title("Parol O'zgartirish")
        pw_win.geometry("380x320")
        pw_win.transient(app.root)
        pw_win.grab_set()

        ctk.CTkLabel(pw_win, text="Parollarni Yangilash", font=("Segoe UI", 16, "bold")).pack(pady=15)

        ctk.CTkLabel(pw_win, text="Foydalanuvchi roli:", font=("Segoe UI", 12)).pack(anchor="w", padx=30)
        role_combo = ctk.CTkComboBox(pw_win, values=["admin", "operator"], width=320, state="readonly")
        role_combo.set("admin")
        role_combo.pack(pady=5)

        ctk.CTkLabel(pw_win, text="Yangi parol:", font=("Segoe UI", 12)).pack(anchor="w", padx=30, pady=(10, 0))
        new_pwd_entry = ctk.CTkEntry(pw_win, show="*", width=320, placeholder_text="Yangi parol kiriting...")
        new_pwd_entry.pack(pady=5)

        def save_new_pwd():
            new_p = new_pwd_entry.get().strip()
            if not new_p:
                messagebox.showerror("Xato", "Parol bo'sh bo'lishi mumkin emas!")
                return
            sel_role = role_combo.get()
            if "passwords" not in app.data_manager.settings:
                app.data_manager.settings["passwords"] = {}
            app.data_manager.settings["passwords"][sel_role] = hash_password(new_p)
            app.data_manager.save_settings()
            app.data_manager.log_activity(app.current_role, "Parol Yangilandi", f"{sel_role.upper()} paroli o'zgartirildi")
            messagebox.showinfo("OK", f"{sel_role.upper()} paroli muvaffaqiyatli saqlandi!")
            pw_win.destroy()

        ctk.CTkButton(pw_win, text="Saqlash", command=save_new_pwd, fg_color="#27ae60", width=320, height=40).pack(pady=20)

    ctk.CTkButton(pwd_frame, text="O'zgartirish", command=open_change_pwd_dialog, font=("Segoe UI", 13), width=150).pack(side="right", padx=15)
