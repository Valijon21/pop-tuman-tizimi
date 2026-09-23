import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Any

def render_trash(parent: tk.Widget, app: Any) -> None:
    """Chiqindi qutisi (Trash) sahifasini ko'rsatish."""
    # Sarlavha
    ctk.CTkLabel(
        parent,
        text="Chiqindi Qutisi (Trash)",
        font=("Segoe UI", int(app.font_size * 1.7), "bold"),
        text_color=("#c0392b", "#e74c3c")
    ).pack(anchor="w", padx=30, pady=20)

    ctk.CTkLabel(
        parent,
        text="O'chirilgan ma'lumotlarni tiklashingiz yoki butunlay o'chirishingiz mumkin",
        font=("Segoe UI", int(app.font_size * 0.8)),
        text_color="gray"
    ).pack(anchor="w", padx=35)

    # Jadval konteyneri
    tree_frame = ctk.CTkFrame(parent)
    tree_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

    app.update_treeview_style()
    app.trash_tree = ttk.Treeview(tree_frame, columns=("m", "f", "date"), show="headings")

    app.trash_tree.heading("m", text="Tashkilot Nomi")
    app.trash_tree.column("m", width=300)
    app.trash_tree.heading("f", text="Rahbar")
    app.trash_tree.column("f", width=200)
    app.trash_tree.heading("date", text="O'chirilgan vaqt")
    app.trash_tree.column("date", width=150)

    app.trash_tree.pack(fill="both", expand=True, padx=5, pady=5)

    # Ma'lumotlarni yuklash (iid bilan)
    for i in app.data_manager.trash:
        item_id = str(i.get("id") or i.get("uuid") or "")
        app.trash_tree.insert("", "end", iid=item_id, values=(i.get("m"), i.get("f"), i.get("deleted_at", "-")))

    # Amallar tugmalari
    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(fill="x", padx=30, pady=20)

    ctk.CTkButton(
        btn_frame,
        text="♻ Tiklash",
        fg_color="#27ae60",
        height=40,
        font=("Segoe UI", 12, "bold"),
        command=app.restore_item
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="🔥 Butunlay O'chirish",
        fg_color="#c0392b",
        height=40,
        hover_color="#a93226",
        font=("Segoe UI", 12, "bold"),
        command=app.perm_delete_item
    ).pack(side="left", padx=5)
