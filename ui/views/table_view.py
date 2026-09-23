import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import pyperclip
import uuid
import webbrowser
from typing import Any, Optional, Dict

from services.qr_service import clean_phone_number, generate_phone_qr_image
from core.validators import validate_inn, validate_phone, clean_inn, validate_jshshir, validate_passport_series

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

    search_entry = ctk.CTkEntry(search_frame, textvariable=app.s_var, width=280, height=40, font=("Segoe UI", 14), placeholder_text="Qidiruv...")
    search_entry.pack(side="left", padx=5)

    ctk.CTkButton(search_frame, text="✖", width=40, height=40, fg_color="#e74c3c", command=lambda: app.s_var.set("")).pack(side="left", padx=5)

    # Harakat tugmalari
    btn_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
    btn_frame.pack(side="right")

    def add_btn(txt, cmd, col, w=96):
        ctk.CTkButton(btn_frame, text=txt, command=cmd, fg_color=col, height=40, font=("Segoe UI", int(app.font_size * 0.78), "bold"), width=w).pack(side="right", padx=2)

    add_btn("🛡 Verifikatsiya", lambda: open_verification_dialog(app), "#0284c7", 108)
    add_btn("🏘 Yettilik", lambda: app.open_yettilik(), "#16a34a", 85)
    add_btn("📜 Tarix", lambda: app.open_history(), "#7c3aed", 75)
    add_btn("📥 Import", lambda: app.open_import(), "#0d9488", 80)
    add_btn("📝 Izoh", app.manual_edit_comment, "#8e44ad", 75)
    add_btn("📱 QR", lambda: show_qr_dialog(app), "#e67e22", 65)
    add_btn("✈ Telegram", lambda: send_telegram_card(app), "#0088cc", 95)
    add_btn("📊 Excel", app.open_export_menu, "#107c41", 75)
    add_btn("✏ Tahrir", lambda: open_record_dialog(app, title="Tahrirlash"), "#f39c12", 75)

    # + Qo'shish
    ctk.CTkButton(btn_frame, text="+ Qo'shish", command=lambda: open_record_dialog(app, title="Yangi qo'shish"), fg_color="#27ae60", height=40, font=("Segoe UI", int(app.font_size * 0.85), "bold"), width=100).pack(side="right", padx=(2, 6))

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

    app.filter_data()

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

    # Tanlangan qatordagi mahalla nomini aniqlash
    v = app.tree.item(item)["values"]
    selected_mahalla = str(v[2]) if v and len(v) > 2 else None

    menu.add_command(label="🛡 Verifikatsiya so'rovi (Dialog)", command=lambda: open_verification_dialog(app))
    menu.add_command(label="⚡ Tezkor Verifikatsiya nusxalash", command=lambda: copy_verification_quick(app))
    menu.add_separator()
    menu.add_command(label="🏘 Mahalla 'Yettiligi' (360° Pasport)", command=lambda: app.open_yettilik(selected_mahalla))
    menu.add_command(label="📜 Kadrlar almashinuvi tarixi", command=lambda: app.open_history(mahalla=selected_mahalla))
    menu.add_command(label="📥 Excel / CSV Ommaviy Import", command=app.open_import)
    menu.add_separator()
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
    win.geometry("480x700")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 240
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 350
    win.geometry(f"+{x}+{y}")

    ctk.CTkLabel(win, text=title, font=("Segoe UI", 22, "bold"), text_color=("#2c3e50", "#ecf0f1")).pack(pady=(20, 5))
    ctk.CTkLabel(win, text="Ma'lumotlarni to'ldiring", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 10))

    cat_opts = app.data_manager.categories
    form_config = [
        ("s", "Tashkilot Turi", "combo", cat_opts),
        ("m", "Tashkilot Nomi", "entry", None),
        ("f", "Rahbar (F.I.SH)", "entry", None),
        ("t", "Telefon Raqam", "entry", None),
        ("inn", "INN (Soliq to'lovchi)", "entry", None),
        ("jshr", "JSHSHIR (PINFL - 14 ta raqam)", "entry", None),
        ("seriya", "Pasport Seriya (AB1234567)", "entry", None),
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
        val_jshr = widgets["jshr"].get().strip()
        val_seriya = widgets["seriya"].get().strip()

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

        if val_jshr:
            is_valid_jshr, jshr_msg = validate_jshshir(val_jshr, allow_empty=True)
            if not is_valid_jshr:
                app.show_toast(jshr_msg, "warning")
                return

        if val_seriya:
            is_valid_ser, ser_msg = validate_passport_series(val_seriya, allow_empty=True)
            if not is_valid_ser:
                app.show_toast(ser_msg, "warning")
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

        # Xodim o'zgargan bo'lsa, avtomatik staff_history ga yozish
        if item:
            old_fio = str(item.get("f", "")).strip()
            new_fio = str(d.get("f", "")).strip()
            if old_fio and new_fio and old_fio != new_fio:
                try:
                    app.data_manager.add_staff_history(
                        org_id=d.get("id"),
                        org_name=d.get("m"),
                        mahalla=d.get("mahalla") or d.get("m"),
                        role=d.get("lavozim") or d.get("s") or "Rahbar",
                        old_fio=old_fio,
                        new_fio=new_fio,
                        old_phone=str(item.get("t", "")),
                        new_phone=str(d.get("t", "")),
                        changed_by=app.current_role or "admin",
                        reason="Tahrirlash oynasi orqali xodim yangilandi"
                    )
                except Exception as ex:
                    print(f"Staff history recording warning: {ex}")

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

def get_selected_organization_item(app: Any) -> Optional[Dict[str, Any]]:
    """Jadvaldan tanlangan tashkilot yozuvini aniqlash."""
    if not hasattr(app, "tree"): return None
    sel = app.tree.focus()
    if not sel and app.tree.selection():
        sel = app.tree.selection()[0]
    if not sel: return None
    
    item = next((i for i in app.data if str(i.get("id")) == sel or str(i.get("uuid")) == sel), None)
    if not item:
        v = app.tree.item(sel)["values"]
        if v and len(v) > 5:
            inn = str(v[5])
            item = next((i for i in app.data if str(i.get("inn")) == inn), None)
    if not item:
        v = app.tree.item(sel)["values"]
        if v and len(v) >= 7:
            item = {
                "s": v[1],
                "m": v[2],
                "f": v[3],
                "t": v[4],
                "inn": v[5],
                "izoh": v[6]
            }
    return item

def copy_verification_quick(app: Any) -> None:
    """Tanlangan tashkilot/xodim uchun darhol verifikatsiya matnini clipboardga nusxalash."""
    item = get_selected_organization_item(app)
    if not item:
        app.show_toast("Iltimos, avval ro'yxatdan xodim yoki tashkilotni tanlang!", "warning")
        return
        
    from services.verification_service import build_verification_text
    text = build_verification_text(item)
    pyperclip.copy(text)
    app.show_toast("✅ Verifikatsiya shablon matni nusxalandi!", "success")

def open_verification_dialog(app: Any) -> None:
    """Professional Verifikatsiya dialog oynasi."""
    item = get_selected_organization_item(app)
    if not item:
        app.show_toast("Iltimos, avval ro'yxatdan xodim yoki tashkilotni tanlang!", "warning")
        return

    from services.verification_service import build_verification_text, extract_identifiers_from_text, format_role
    
    win = ctk.CTkToplevel(app.root)
    win.title("Verifikatsiya So'rovi")
    win.geometry("520x680")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 260
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 340
    win.geometry(f"+{x}+{y}")

    # Sarlavha
    ctk.CTkLabel(win, text="🛡 Verifikatsiya So'rovi", font=("Segoe UI", 20, "bold"), text_color=("#1e3a8a", "#60a5fa")).pack(pady=(20, 5))
    ctk.CTkLabel(win, text="Rasmiy tasdiqlash uchun ma'lumotlar shabloni", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 15))

    container = ctk.CTkScrollableFrame(win, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

    auto_jshr, auto_seriya = extract_identifiers_from_text(item.get("izoh", ""))
    init_jshr = item.get("jshr") or auto_jshr or ""
    init_seriya = item.get("seriya") or auto_seriya or ""
    init_role = format_role(item.get("s", ""), item.get("m", ""))

    fields = [
        ("m", "Tashkilot nomi", item.get("m", "")),
        ("inn", "-INN", item.get("inn", "")),
        ("f", "F.I.O", item.get("f", "")),
        ("jshr", "JSHR (14 xonali)", init_jshr),
        ("seriya", "Pasport Seriya", init_seriya),
        ("role", "Lavozimi", init_role),
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
    
    txt_preview = tk.Text(container, height=8, font=("Consolas", 11), bg="#1e293b", fg="#f8fafc", bd=0, padx=10, pady=8)
    txt_preview.pack(fill="x", pady=(0, 10))

    def update_preview(*args):
        m_val = entries["m"].get().strip()
        inn_val = entries["inn"].get().strip()
        f_val = entries["f"].get().strip()
        jshr_val = entries["jshr"].get().strip()
        seriya_val = entries["seriya"].get().strip()
        role_val = entries["role"].get().strip()
        
        simulated = {"m": m_val, "inn": inn_val, "f": f_val}
        generated = build_verification_text(simulated, jshr=jshr_val, seriya=seriya_val, role=role_val)
        txt_preview.config(state="normal")
        txt_preview.delete("1.0", tk.END)
        txt_preview.insert("1.0", generated)
        txt_preview.config(state="disabled")

    for e in entries.values():
        e.bind("<KeyRelease>", update_preview)

    update_preview()

    # Tugmalar
    btn_frame = ctk.CTkFrame(win, fg_color="transparent")
    btn_frame.pack(fill="x", padx=25, pady=(0, 20))

    def do_copy():
        txt_preview.config(state="normal")
        content = txt_preview.get("1.0", tk.END).strip()
        txt_preview.config(state="disabled")
        pyperclip.copy(content)
        
        # JSHR va Seriyani bazaga saqlab qo'yish
        jshr_val = entries["jshr"].get().strip()
        seriya_val = entries["seriya"].get().strip()
        if (jshr_val or seriya_val) and hasattr(app, "data_manager"):
            real_item = next((i for i in app.data if str(i.get("id")) == str(item.get("id")) or str(i.get("inn")) == str(item.get("inn"))), None)
            if real_item:
                if jshr_val: real_item["jshr"] = jshr_val
                if seriya_val: real_item["seriya"] = seriya_val
                app.data_manager.save_data()
        
        app.show_toast("✅ Verifikatsiya matni nusxalandi!", "success")
        win.destroy()

    def do_send_telegram():
        import urllib.parse
        txt_preview.config(state="normal")
        content = txt_preview.get("1.0", tk.END).strip()
        txt_preview.config(state="disabled")
        encoded = urllib.parse.quote(content)
        webbrowser.open(f"https://t.me/share/url?url={encoded}")

    ctk.CTkButton(btn_frame, text="📋 Nusxalash (Clipboard)", command=do_copy, fg_color="#2563eb", hover_color="#1d4ed8", font=("Segoe UI", 13, "bold"), height=38).pack(side="left", fill="x", expand=True, padx=(0, 5))
    ctk.CTkButton(btn_frame, text="✈ Telegram", command=do_send_telegram, fg_color="#0088cc", hover_color="#006699", font=("Segoe UI", 13, "bold"), height=38, width=110).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Yopish", command=win.destroy, fg_color="#64748b", hover_color="#475569", font=("Segoe UI", 12), height=38, width=80).pack(side="right", padx=(5, 0))

