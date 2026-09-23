import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import pyperclip
import uuid
from typing import Any, Optional, Dict

from services.qr_service import clean_phone_number, generate_phone_qr_image
from core.validators import validate_inn, validate_phone, clean_inn

def render_table(parent: tk.Widget, app: Any) -> None:
    """Asosiy jadval (Table View) sahifasini ko'rsatish."""
    # ASBOBLAR PANELI (TOOLBAR)
    ctrl = ctk.CTkFrame(parent, fg_color="transparent")
    ctrl.pack(fill="x", padx=20, pady=(20, 10))

    # Qidiruv Konteyneri
    search_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
    search_frame.pack(side="left", fill="x")

    app.f_type = ctk.CTkComboBox(search_frame, values=["Nomi", "F.I.SH", "INN", "Izoh"], width=120, height=40, font=("Segoe UI", 12))
    app.f_type.set("Nomi")
    app.f_type.pack(side="left", padx=(0, 10))

    app.s_var = tk.StringVar()
    app.s_var.trace_add("write", lambda *args: app.filter_data())

    search_entry = ctk.CTkEntry(search_frame, textvariable=app.s_var, width=300, height=40, font=("Segoe UI", 14), placeholder_text="Qidiruv...")
    search_entry.pack(side="left", padx=5)

    ctk.CTkButton(search_frame, text="✖", width=40, height=40, fg_color="#e74c3c", command=lambda: app.s_var.set("")).pack(side="left", padx=5)

    # Harakat tugmalari
    btn_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
    btn_frame.pack(side="right")

    def add_btn(txt, cmd, col):
        ctk.CTkButton(btn_frame, text=txt, command=cmd, fg_color=col, height=40, font=("Segoe UI", int(app.font_size * 0.8), "bold"), width=100).pack(side="right", padx=3)

    add_btn("📝 Izoh", app.manual_edit_comment, "#8e44ad")
    add_btn("📱 QR", lambda: show_qr_dialog(app), "#e67e22")
    add_btn("✈ Telegram", lambda: send_telegram_card(app), "#0088cc")
    add_btn("📊 Excel", app.open_export_menu, "#107c41")
    add_btn("✏ Tahrir", lambda: open_record_dialog(app, title="Tahrirlash"), "#f39c12")

    # + Qo'shish
    ctk.CTkButton(btn_frame, text="+ Qo'shish", command=lambda: open_record_dialog(app, title="Yangi qo'shish"), fg_color="#27ae60", height=40, font=("Segoe UI", int(app.font_size * 0.9), "bold"), width=120).pack(side="right", padx=10)

    # KATEGORIYA TABLARI
    cat_scroll = ctk.CTkScrollableFrame(parent, orientation="horizontal", height=50, fg_color="transparent")
    cat_scroll.pack(fill="x", padx=20, pady=10)

    if not hasattr(app, "cat_var"):
        app.cat_var = tk.StringVar(value="Barchasi")

    app.cat_buttons = {}
    tabs = ["Barchasi"] + app.data_manager.categories

    def update_tab_ui():
        cur = app.cat_var.get()
        for t_name, btn in app.cat_buttons.items():
            if t_name == cur:
                btn.configure(fg_color=("#3b82f6", "#2563eb"), text_color="white")
            else:
                btn.configure(fg_color=("#e2e8f0", "#334155"), text_color=("black", "white"))

    def on_tab_click(val):
        app.cat_var.set(val)
        app.filter_data()
        update_tab_ui()

    for cat in tabs:
        w = max(80, len(cat) * 10 + 20)
        btn = ctk.CTkButton(cat_scroll, text=cat, width=w, height=35, font=("Segoe UI", 12, "bold"), command=lambda c=cat: on_tab_click(c))
        btn.pack(side="left", padx=5)
        app.cat_buttons[cat] = btn

    update_tab_ui()

    # JADVAL KONTEYNERI
    tree_frame = ctk.CTkFrame(parent)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    app.update_treeview_style()

    vsb = ttk.Scrollbar(tree_frame, orient="vertical")
    vsb.pack(side="right", fill="y")

    app.tree = ttk.Treeview(tree_frame, columns=("num", "s", "m", "f", "t", "inn", "izoh"), show="headings", yscrollcommand=vsb.set)

    headers = [("num", "№", 35), ("s", "Turi", 80), ("m", "Tashkilot Nomi", 300), ("f", "F.I.SH", 200),
               ("t", "Tel", 100), ("inn", "INN", 100), ("izoh", "Izoh (Enter=Tahrir)", 200)]

    for col, name, width in headers:
        app.tree.heading(col, text=name, command=lambda c=col: app.sort_treeview(c, False))
        app.tree.column(col, width=width, anchor="center" if col != "m" else "w")

    app.tree.pack(fill="both", expand=True)
    vsb.configure(command=app.tree.yview)

    app.tree.bind("<Button-3>", lambda e: show_context_menu(app, e))
    app.tree.bind("<Double-1>", lambda e: open_record_dialog(app, title="Tahrirlash"))
    app.tree.bind("<Return>", lambda e: edit_comment_inline(app, e))

    # PASTKI RAMKA (Jami hisobi)
    footer = ctk.CTkFrame(parent, fg_color="transparent", height=30)
    footer.pack(fill="x", padx=30, pady=(0, 10))
    app.lbl_count = ctk.CTkLabel(footer, text="Jami: 0", font=("Segoe UI", int(app.font_size * 0.9), "bold"), text_color="gray")
    app.lbl_count.pack(side="right")

    app.update_table(app.filtered_data)

def edit_comment_inline(app: Any, event: Any = None) -> None:
    """Jadval ichida (inline) izohni tezkor tahrirlash."""
    sel = app.tree.focus()
    if not sel: return

    app.tree.see(sel)
    app.root.update_idletasks()

    try:
        bbox = app.tree.bbox(sel, "izoh")
        if not bbox: return
        x, y, w, h = bbox
    except Exception: return

    entry = tk.Entry(app.tree, font=("Segoe UI", app.font_size))
    entry.place(x=x, y=y, width=w, height=h)

    current_val = app.tree.item(sel)["values"][6]
    entry.insert(0, str(current_val or ""))
    entry.select_range(0, tk.END)
    entry.focus_force()

    def save_edit(e=None):
        new_text = entry.get()
        current_values = list(app.tree.item(sel)["values"])
        current_values[6] = new_text
        app.tree.item(sel, values=current_values)

        item = next((i for i in app.data if str(i.get("id")) == sel or str(i.get("uuid")) == sel), None)
        if not item:
            inn = str(current_values[5])
            item = next((i for i in app.data if str(i.get("inn")) == inn), None)
        if item:
            item["izoh"] = new_text
            app.data_manager.save_data()

        entry.destroy()
        try:
            app.tree.focus_set()
            next_item = app.tree.next(sel)
            if next_item:
                app.tree.selection_set(next_item)
                app.tree.focus(next_item)
                app.tree.see(next_item)
        except Exception: pass
        app.sync_background()

    def cancel_edit(e=None):
        entry.destroy()
        app.tree.focus_set()

    entry.bind("<Return>", save_edit)
    entry.bind("<Escape>", cancel_edit)

def show_context_menu(app: Any, event: Any) -> None:
    """O'ng tugma (Context menu) menyusini ochish."""
    item = app.tree.identify_row(event.y)
    if not item: return

    app.tree.selection_set(item)
    menu = tk.Menu(app.root, tearoff=0)

    menu.add_command(label="📞 Tel nusxalash", command=lambda: app.copy_cell(4))
    menu.add_command(label="🆔 INN nusxalash", command=lambda: app.copy_cell(5))
    menu.add_command(label="📝 Izohni nusxalash", command=lambda: app.copy_cell(6))
    menu.add_separator()
    menu.add_command(label="📋 Qatorni nusxalash", command=app.copy_row)
    menu.add_separator()
    menu.add_command(label="🧹 Belgilangan Izohlarni Tozalash", command=app.clear_comments)
    menu.add_command(label="🗑 BARCHA Izohlarni Tozalash", command=app.clear_all_comments)
    menu.add_separator()
    menu.add_command(label="🗑 Chiqindiga tashlash", command=app.delete_selected_item, foreground="red")

    menu.post(event.x_root, event.y_root)

def open_record_dialog(app: Any, title: str = "Tahrirlash") -> None:
    """Tashkilot qo'shish yoki tahrirlash dialogi."""
    if not app.check_password(): return

    item = None
    if title == "Tahrirlash":
        sel = app.tree.focus()
        if not sel: return
        item = next((i for i in app.data if str(i.get("id")) == sel or str(i.get("uuid")) == sel), None)
        if not item:
            v = app.tree.item(sel)["values"]
            if v and len(v) > 5:
                item = next((i for i in app.data if str(i.get("inn")) == str(v[5])), None)
        if not item: return

    win = ctk.CTkToplevel(app.root)
    win.title(title)
    win.geometry("450x620")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 225
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 310
    win.geometry(f"+{x}+{y}")

    ctk.CTkLabel(win, text=title, font=("Segoe UI", 22, "bold"), text_color=("#2c3e50", "#ecf0f1")).pack(pady=(25, 5))
    ctk.CTkLabel(win, text="Ma'lumotlarni to'ldiring", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 15))

    cat_opts = app.data_manager.categories
    form_config = [
        ("s", "Tashkilot Turi", "combo", cat_opts),
        ("m", "Tashkilot Nomi", "entry", None),
        ("f", "Rahbar (F.I.SH)", "entry", None),
        ("t", "Telefon Raqam", "entry", None),
        ("inn", "INN (Soliq to'lovchi)", "entry", None),
        ("izoh", "Qo'shimcha Izoh", "entry", None),
    ]

    widgets = {}
    container = ctk.CTkScrollableFrame(win, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    for key, lbl, w_type, opts in form_config:
        ctk.CTkLabel(container, text=lbl, font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(5, 0))
        if w_type == "combo":
            w = ctk.CTkComboBox(container, values=opts, height=35, font=("Segoe UI", 13))
        else:
            w = ctk.CTkEntry(container, height=35, font=("Segoe UI", 13))
        w.pack(fill="x", pady=(0, 8))
        widgets[key] = w

        if item:
            val = item.get(key, "")
            if w_type == "combo": w.set(val)
            else: w.insert(0, str(val))

    if "t" in widgets:
        widgets["t"].bind("<KeyRelease>", app.format_phone_input)

    def save():
        val_inn = widgets["inn"].get().strip()
        val_name = widgets["m"].get().strip()
        val_phone = widgets["t"].get().strip()

        if not val_name:
            app.show_toast("Xatolik: Tashkilot nomi kiritilmadi!", "warning")
            return

        if val_inn:
            is_valid_inn, inn_msg = validate_inn(val_inn, allow_empty=True)
            if not is_valid_inn:
                app.show_toast(inn_msg, "warning")
                return

        if val_phone:
            is_valid_phone, phone_msg = validate_phone(val_phone, allow_empty=True)
            if not is_valid_phone:
                app.show_toast(phone_msg, "warning")
                return

        if val_inn:
            target_id = item.get("id") if item else None
            exists = next((x for x in app.data if x.get("inn") == val_inn and (not target_id or x.get("id") != target_id)), None)
            if exists:
                msg = f"DIQQAT: Bu INN ({val_inn}) allaqachon mavjud!\n\nTashkilot: {exists.get('m')}\nRahbar: {exists.get('f')}\n\nBaribir saqlansinmi?"
                if not messagebox.askyesno("Dublikat Topildi", msg):
                    return

        d = {}
        for key, _, _, _ in form_config:
            d[key] = widgets[key].get().strip()

        d["id"] = item.get("id") if (item and item.get("id")) else str(uuid.uuid4())

        if item:
            target_id = d["id"]
            idx = -1
            for cand_idx, cand in enumerate(app.data):
                if cand.get("id") == target_id:
                    idx = cand_idx
                    break
            if idx >= 0:
                app.data[idx] = d
            elif item in app.data:
                app.data[app.data.index(item)] = d
            else:
                app.data.append(d)
            app.data_manager.log_activity(app.current_role, "Tahrirlash", f"{d.get('m')} yangilandi")
        else:
            app.data.append(d)
            app.data_manager.log_activity(app.current_role, "Qo'shish", f"{d.get('m')} yangi qo'shildi")

        app.save_data()
        app.filter_data()
        win.destroy()
        app.show_toast("Muvaffaqiyatli saqlandi!", "success")
        app.sync_background()

    ctk.CTkButton(win, text="SAQLASH", command=save, height=45, font=("Segoe UI", 14, "bold"), fg_color="#27ae60", hover_color="#2ecc71").pack(fill="x", padx=40, pady=15)

def show_qr_dialog(app: Any) -> None:
    """Tanlangan tashkilot uchun xotirada QR-kod yaratib ko'rsatish."""
    sel = app.tree.focus()
    if not sel: return

    v = app.tree.item(sel)["values"]
    raw_tel = str(v[4])
    clean_tel = clean_phone_number(raw_tel)

    if not clean_tel:
        app.show_toast("Telefon raqami topilmadi!")
        return

    try:
        pil_img = generate_phone_qr_image(clean_tel, size=250)

        w = tk.Toplevel(app.root)
        w.title("QR Kod (Telefon)")
        w.geometry("320x450")
        w.transient(app.root)

        img_photo = ImageTk.PhotoImage(pil_img)
        lbl = tk.Label(w, image=img_photo)
        lbl.image = img_photo
        lbl.pack(pady=20)

        tk.Label(w, text=f"{v[2]}", font=("Segoe UI", 12, "bold")).pack()
        tk.Label(w, text=f"{v[3]}", font=("Segoe UI", 10), fg="gray").pack()
        tk.Label(w, text=f"{clean_tel}", font=("Segoe UI", 16, "bold"), fg="#27ae60").pack(pady=5)
        tk.Label(w, text="(Skaner qiling va qo'ng'iroq qiling)", font=("Segoe UI", 9), fg="gray").pack(pady=5)
    except Exception as e:
        messagebox.showerror("QR Xatosi", f"QR Kod yaratishda xatolik: {e}")

def send_telegram_card(app: Any) -> None:
    """Telegramga nusxalash kartasi."""
    sel = app.tree.focus()
    if not sel: return
    v = app.tree.item(sel)["values"]
    izoh = f"\n📝 {v[6]}" if v[6] else ""
    text = f"🏢 {v[1]} {v[2]}\n👤 {v[3]}\n📞 {v[4]}\n🆔 {v[5]}{izoh}"
    pyperclip.copy(text)
    app.show_toast("Telegram kartasi nusxalandi!", "success")
