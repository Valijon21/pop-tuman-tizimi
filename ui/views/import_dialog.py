"""
Pop Tuman Tashkilotlari va INN Tizimi
Excel va CSV Ommaviy Import Muloqot Oynasi (Batch Import Dialog)
Dublikatlarni aqlli aniqlash va xavfsiz yuklash.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from typing import Any, List, Dict

from services.excel_service import import_organizations_from_file

def open_batch_import_dialog(app: Any) -> None:
    """Ommaviy import dialogini ochish."""
    if not app.check_password():
        return

    filepath = filedialog.askopenfilename(
        title="Excel yoki CSV faylni tanlang",
        filetypes=[("Excel va CSV fayllari", "*.xlsx;*.xls;*.csv"), ("Barcha fayllar", "*.*")]
    )
    if not filepath:
        return

    imported_items, warnings = import_organizations_from_file(filepath)
    if not imported_items:
        msg = "\n".join(warnings) if warnings else "Fayldan yaroqli ma'lumot topilmadi!"
        messagebox.showerror("Import Xatosi", msg)
        return

    # Dublikatlarni aniqlash (mavjud INN lar bilan solishtirish)
    existing_inns = {str(item.get("inn", "")).strip(): item for item in app.data if str(item.get("inn", "")).strip()}
    
    duplicates = []
    new_records = []
    for item in imported_items:
        item_inn = str(item.get("inn", "")).strip()
        if item_inn and item_inn in existing_inns:
            duplicates.append(item)
        else:
            new_records.append(item)

    win = ctk.CTkToplevel(app.root)
    win.title("Ommaviy Importni Tasdiqlash")
    win.geometry("750x620")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 375
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 310
    win.geometry(f"+{x}+{y}")

    # Header
    ctk.CTkLabel(win, text="📥 Ommaviy Import Xulosasi", font=("Segoe UI", 20, "bold"), text_color=("#1e3a8a", "#60a5fa")).pack(pady=(20, 5))
    ctk.CTkLabel(win, text=f"Fayl: {filepath}", font=("Segoe UI", 11), text_color="gray").pack(pady=(0, 15))

    # Statistika kartasi
    stat_frame = ctk.CTkFrame(win, fg_color=("white", "#1e293b"), corner_radius=10)
    stat_frame.pack(fill="x", padx=30, pady=(0, 15))

    stat_cols = [
        ("Jami o'qildi", len(imported_items), "#3b82f6"),
        ("Yangi tashkilotlar", len(new_records), "#10b981"),
        ("Mavjud (Dublikat INN)", len(duplicates), "#f59e0b" if duplicates else "#64748b")
    ]
    for idx, (lbl, val, col) in enumerate(stat_cols):
        c_box = ctk.CTkFrame(stat_frame, fg_color="transparent")
        c_box.pack(side="left", fill="both", expand=True, pady=12)
        ctk.CTkLabel(c_box, text=str(val), font=("Segoe UI", 20, "bold"), text_color=col).pack()
        ctk.CTkLabel(c_box, text=lbl, font=("Segoe UI", 11), text_color="gray").pack()

    # Dublikat siyosati
    dup_policy = tk.StringVar(value="update" if duplicates else "new_only")
    
    policy_frame = ctk.CTkFrame(win, fg_color="transparent")
    policy_frame.pack(fill="x", padx=30, pady=(0, 10))
    
    ctk.CTkLabel(policy_frame, text="Mavjud (dublikat INN) yozuvlar bo'yicha amal:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
    
    ctk.CTkRadioButton(policy_frame, text="Mavjudlarini yangilash (Tavsiya etiladi - eski ma'lumotlar ustiga yoziladi)", variable=dup_policy, value="update").pack(anchor="w", pady=3)
    ctk.CTkRadioButton(policy_frame, text="Dublikatlarni o'tkazib yuborish (Faqat yangi tashkilotlar qo'shiladi)", variable=dup_policy, value="skip").pack(anchor="w", pady=3)
    ctk.CTkRadioButton(policy_frame, text="Barchasini yangi nusxa sifatida qo'shish", variable=dup_policy, value="all").pack(anchor="w", pady=3)

    # Preview Table
    ctk.CTkLabel(win, text="Ko'rib chiqish (Dastlabki 6 ta qator):", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30, pady=(10, 5))
    
    prev_box = ctk.CTkFrame(win)
    prev_box.pack(fill="both", expand=True, padx=30, pady=(0, 15))

    tree = ttk.Treeview(prev_box, columns=("s", "m", "f", "t", "inn"), show="headings", height=5)
    headers = [("s", "Turi", 80), ("m", "Nomi", 220), ("f", "Rahbar", 180), ("t", "Tel", 100), ("inn", "INN", 90)]
    for col, name, width in headers:
        tree.heading(col, text=name)
        tree.column(col, width=width, anchor="center" if col != "m" else "w")

    for item in imported_items[:6]:
        tree.insert("", "end", values=(
            item.get("s", "-"), item.get("m", "-"), item.get("f", "-"),
            item.get("t", "-"), item.get("inn", "-")
        ))
    tree.pack(fill="both", expand=True)

    # Tugmalar
    footer = ctk.CTkFrame(win, fg_color="transparent")
    footer.pack(fill="x", padx=30, pady=(0, 20))

    def do_import():
        policy = dup_policy.get()
        added_count = 0
        updated_count = 0

        for item in imported_items:
            item_inn = str(item.get("inn", "")).strip()
            if item_inn and item_inn in existing_inns:
                if policy == "update":
                    existing = existing_inns[item_inn]
                    existing.update({
                        "s": item.get("s") or existing.get("s"),
                        "m": item.get("m") or existing.get("m"),
                        "f": item.get("f") or existing.get("f"),
                        "t": item.get("t") or existing.get("t"),
                        "izoh": item.get("izoh") or existing.get("izoh"),
                        "jshr": item.get("jshr") or existing.get("jshr"),
                        "seriya": item.get("seriya") or existing.get("seriya")
                    })
                    updated_count += 1
                elif policy == "skip":
                    continue
                elif policy == "all":
                    app.data.append(item)
                    added_count += 1
            else:
                app.data.append(item)
                added_count += 1

        app.save_data()
        app.filter_data()
        app.data_manager.log_activity(
            user=app.current_role or "admin",
            action="Ommaviy Import",
            details=f"{added_count} ta qo'shildi, {updated_count} ta yangilandi"
        )
        app.sync_background()

        app.show_toast(f"✅ Import muvaffaqiyatli: {added_count} ta qo'shildi, {updated_count} ta yangilandi!", "success")
        win.destroy()

    ctk.CTkButton(footer, text="✅ Tasdiqlash va Bazaga Yuklash", command=do_import, fg_color="#10b981", hover_color="#059669", font=("Segoe UI", 13, "bold"), height=38).pack(side="left", padx=(0, 10))
    ctk.CTkButton(footer, text="Bekor qilish", command=win.destroy, fg_color="#64748b", hover_color="#475569", font=("Segoe UI", 12), height=38, width=100).pack(side="right")
