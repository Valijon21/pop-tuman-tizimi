"""
Pop Tuman Tashkilotlari va INN Tizimi
Xodimlar Rotatsiyasi va Kadrlar Tarixi Ko'rinishi (Staff History View)
Lavozimlarda ishlagan sobiq va joriy mas'ullar tarixi arxivi.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from typing import Any, Optional, Dict, List

def open_staff_history_dialog(app: Any, org_id: Optional[str] = None, mahalla: Optional[str] = None) -> None:
    """Xodimlar almashinuvi tarixi dialog oynasi."""
    win = ctk.CTkToplevel(app.root)
    title_suffix = f": {mahalla}" if mahalla else ""
    win.title(f"Xodimlar Almashinuvi Tarixi{title_suffix}")
    win.geometry("950x600")
    win.transient(app.root)
    win.grab_set()

    x = app.root.winfo_x() + (app.root.winfo_width() // 2) - 475
    y = app.root.winfo_y() + (app.root.winfo_height() // 2) - 300
    win.geometry(f"+{x}+{y}")

    # Header
    head = ctk.CTkFrame(win, fg_color="transparent")
    head.pack(fill="x", padx=25, pady=(20, 10))

    ctk.CTkLabel(head, text="📜 Kadrlar Almashinuvi va Rotatsiya Tarixi", font=("Segoe UI", 20, "bold"), text_color=("#1e3a8a", "#60a5fa")).pack(side="left")

    # Qidiruv / Filtr
    filter_frame = ctk.CTkFrame(win, fg_color="transparent")
    filter_frame.pack(fill="x", padx=25, pady=(0, 10))

    s_var = tk.StringVar()
    ctk.CTkLabel(filter_frame, text="Qidiruv:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 5))
    s_entry = ctk.CTkEntry(filter_frame, textvariable=s_var, width=280, height=34, placeholder_text="F.I.SH, Mahalla yoki Lavozim...")
    s_entry.pack(side="left", padx=5)

    # Table Frame
    tree_frame = ctk.CTkFrame(win)
    tree_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

    vsb = ttk.Scrollbar(tree_frame, orient="vertical")
    vsb.pack(side="right", fill="y")

    cols = ("date", "mahalla", "role", "name", "phone", "inn", "note")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", yscrollcommand=vsb.set)
    vsb.configure(command=tree.yview)

    headers = [
        ("date", "Sana", 120),
        ("mahalla", "Mahalla / Tashkilot", 180),
        ("role", "Lavozim", 150),
        ("name", "Xodim (F.I.SH)", 200),
        ("phone", "Telefon", 110),
        ("inn", "INN", 90),
        ("note", "Izoh / Sabab", 140)
    ]
    for col, name, width in headers:
        tree.heading(col, text=name)
        tree.column(col, width=width, anchor="center" if col in ["date", "phone", "inn"] else "w")

    tree.pack(fill="both", expand=True)

    def load_data(*args):
        for r in tree.get_children():
            tree.delete(r)

        raw_history = app.data_manager.get_staff_history(org_id=org_id, mahalla=mahalla)
        q = s_var.get().strip().lower()

        filtered = []
        for h in raw_history:
            if not q or (
                q in str(h.get("full_name", "")).lower() or
                q in str(h.get("mahalla", "")).lower() or
                q in str(h.get("role", "")).lower() or
                q in str(h.get("inn", "")).lower()
            ):
                filtered.append(h)

        if not filtered and not raw_history:
            tree.insert("", "end", values=("-", "Tarixiy ma'lumotlar hozircha yo'q", "-", "-", "-", "-", "-"))
        else:
            for item in filtered:
                tree.insert("", "end", values=(
                    str(item.get("change_date", ""))[:16],
                    item.get("mahalla") or "-",
                    item.get("role") or "-",
                    item.get("full_name") or "-",
                    item.get("phone") or "-",
                    item.get("inn") or "-",
                    item.get("note") or ""
                ))

    s_var.trace_add("write", load_data)
    load_data()

    # Footer
    footer = ctk.CTkFrame(win, fg_color="transparent")
    footer.pack(fill="x", padx=25, pady=(0, 20))

    ctk.CTkButton(footer, text="Yopish", command=win.destroy, fg_color="#64748b", hover_color="#475569", width=100, height=36).pack(side="right")
