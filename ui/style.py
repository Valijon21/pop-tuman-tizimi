from tkinter import ttk
import customtkinter as ctk

def apply_treeview_style(style: ttk.Style, font_size: int, mode: str = "Light") -> None:
    """Treeview ranglari va shriftlarini Light/Dark rejimga moslashtirish."""
    bg = "#2b2b2b" if mode == "Dark" else "white"
    fg = "white" if mode == "Dark" else "#333333"
    field = "#2b2b2b" if mode == "Dark" else "white"
    header_bg = "#34495e" if mode == "Dark" else "#e5e7eb"
    header_fg = "white" if mode == "Dark" else "#1f2937"

    style.theme_use("clam")

    # Qatorlar stili
    style.configure(
        "Treeview",
        background=bg,
        foreground=fg,
        fieldbackground=field,
        rowheight=int(font_size * 2.5),
        borderwidth=0,
        font=("Segoe UI", font_size)
    )

    # Sarlavha stili
    style.configure(
        "Treeview.Heading",
        background=header_bg,
        foreground=header_fg,
        relief="flat",
        font=("Segoe UI", max(11, int(font_size * 0.9)), "bold")
    )

    style.map("Treeview", background=[("selected", "#3b82f6")])
