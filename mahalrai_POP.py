
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import pyperclip
import qrcode
import webbrowser
import csv
import requests
import openpyxl
import shutil
import time
import math # Added for charts
import customtkinter as ctk # MODERN UI
from PIL import Image, ImageTk
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading
import logging
import traceback
import re

# Setup Logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Fayl sozlamalari
# Fayl sozlamalari
DB_FILE = "mahalla_bazasi.json"
TRASH_FILE = "trash.json"
BACKUP_DIR = "backups"

import time
import shutil

class DataManager:
    def __init__(self):
        self.data = self.load_json(DB_FILE)
        self.trash = self.load_json(TRASH_FILE)
        self.categories = self.load_json("categories.json")
        if not self.categories:
             self.categories = ["Mahalla (MFY)", "Maktab", "Bog'cha (MTT)", "Boshqa"]
        self.ensure_backup_dir()

    def ensure_backup_dir(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

    def load_json(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        self.save_json(DB_FILE, self.data)

    def save_trash(self):
        self.save_json(TRASH_FILE, self.trash)

    def save_categories(self):
        self.save_json("categories.json", self.categories)

    def save_json(self, filepath, data):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def move_to_trash(self, item):
        if item in self.data:
            self.data.remove(item)
            item["deleted_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.trash.append(item)
            self.save_data()
            self.save_trash()
            return True
        return False

    def restore_from_trash(self, item):
        if item in self.trash:
            self.trash.remove(item)
            if "deleted_at" in item: del item["deleted_at"]
            self.data.append(item)
            self.save_data()
            self.save_trash()
            return True
        return False

    def permanent_delete(self, item):
        if item in self.trash:
            self.trash.remove(item)
            self.save_trash()
            return True
        return False

    def backup_data(self):
        if os.path.exists(DB_FILE):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}.json")
            try:
                shutil.copy2(DB_FILE, backup_path)
                # Keep only last 10 backups
                backups = sorted([os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR)])
                while len(backups) > 10:
                    os.remove(backups.pop(0))
            except: pass

class MahallaDasturi:
    def __init__(self, root):
        self.root = root
        self.root.title("Pop Tumani Smart Boshqaruv Tizimi (PRO)")
        self.root.geometry("1350x800")
        self.root.configure(bg="#f4f7f6")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.data_manager = DataManager()
        self.data = self.data_manager.data
        self.font_size = 15
        self.filtered_data = self.data[:]
        self.setup_ui()

    def on_close(self):
        self.data_manager.backup_data()
        self.root.destroy()

    def save_data(self):
        self.data_manager.save_data()

    def load_sync_config(self):
        default_url = "https://docs.google.com/spreadsheets/d/1l4MVpVGoyWMP_9Px9QG4V3hWLdQf9LlJ/edit"
        try:
            with open("sync_config.json", "r") as f:
                return json.load(f).get("sheet_id", default_url)
        except: return default_url

    def save_sync_config(self, sheet_id):
        with open("sync_config.json", "w") as f:
            json.dump({"sheet_id": sheet_id}, f)

    def setup_ui(self):
        # THEME CONFIG: Modern Palette (Slate & Blue)
        self.themes = {
            "light": {
                "bg": "#f8fafc", "fg": "#334155", 
                "content_bg": "#f1f5f9", 
                "sidebar": "#1e293b", "sidebar_text": "#e2e8f0", 
                "card_bg": "white", "text": "#1e293b", "accent": "#3b82f6"
            },
            "dark": {
                "bg": "#0f172a", "fg": "#e2e8f0", 
                "content_bg": "#1e293b", 
                "sidebar": "#020617", "sidebar_text": "#94a3b8", 
                "card_bg": "#1e293b", "text": "#f8fafc", "accent": "#60a5fa"
            }
        }
        self.current_theme = "light"
        self.admin_password = "123" # Default
        self.last_auth_time = 0; self.auth_timeout = 20 * 60
        
        # Load Sync Config
        self.sheet_identifier = self.load_sync_config()
        
        # Modern Font
        self.lbl_font = ("Segoe UI", 15)
        self.head_font = ("Segoe UI", 32, "bold") # Much Bigger Title
        
        # Absolute Path Fix
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.base_dir, "popdata.png")
        
        # Set Icon
        try:
            icon_img = ImageTk.PhotoImage(file=self.icon_path)
            self.root.iconphoto(False, icon_img)
            self.root.title("POP Tuman") 
        except Exception as e: print(f"Icon Load Fail: {e}")
        self.btn_font = ("Segoe UI", 13, "bold")
        
        # User Roles
        self.current_role = None
        self.users = {"admin": "123", "operator": "1"}

        # MAIN LAYOUT
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=("white", "#1a1a1a"))
        self.main_container.pack(fill="both", expand=True)

        # SIDEBAR
        self.sidebar = tk.Frame(self.main_container, bg=self.themes["light"]["sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Fixed width
        
        # LOGO AREA
        try:
             # Load Image Absolute
             pil_img = Image.open(self.icon_path)
             pil_img = pil_img.resize((150, 150)) # Resize Bigger
             logo_photo = ImageTk.PhotoImage(pil_img)
             
             self.logo_lbl = tk.Label(self.sidebar, image=logo_photo, bg=self.themes["light"]["sidebar"], pady=10)
             self.logo_lbl.image = logo_photo # Keep ref
             self.logo_lbl.pack(pady=(20, 10))
             
             tk.Label(self.sidebar, text="POP TUMANI\nSMART TIZIM", fg="white", bg=self.themes["light"]["sidebar"], font=("Segoe UI", 16, "bold")).pack(fill="x")
        except Exception as e:
             print(f"Logo Fail: {e}")
             self.logo_lbl = tk.Label(self.sidebar, text="POP TUMANI\nSMART TIZIM", fg="white", bg=self.themes["light"]["sidebar"], font=("Segoe UI", 16, "bold"), pady=30)
             self.logo_lbl.pack(fill="x")
        
        # NAVIGATION
        ctk.CTkLabel(self.sidebar, text="ASOSIY", font=("Segoe UI", 12, "bold"), text_color="#95a5a6", anchor="w").pack(fill="x", padx=30, pady=(10,5))
        self.create_sidebar_btn("📊 Dashboard", self.show_dashboard)
        self.create_sidebar_btn("📋 Ro'yxat", self.show_table)
        self.create_sidebar_btn("⚙ Sozlamalar", self.show_settings)
        
        ctk.CTkLabel(self.sidebar, text="TIZIM", font=("Segoe UI", 12, "bold"), text_color="#95a5a6", anchor="w").pack(fill="x", padx=30, pady=(20,5))
        self.create_sidebar_btn("🗑 Chiqindi Qutisi", self.show_trash)
        self.create_sidebar_btn("☁ Cloud Sync", self.open_cloud_menu)
        
        # Bottom controls
        self.btn_theme = self.create_sidebar_btn("🌙 Tungi Rejim", self.toggle_theme)
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#34495e").pack(fill="x", padx=20, pady=10) # Divider
        
        # Sync Status Label
        self.lbl_sync = ctk.CTkLabel(self.sidebar, text="☁ Integratsiya", text_color="gray", font=("Segoe UI", 11))
        self.lbl_sync.pack(fill="x", pady=(0, 5))

        self.create_sidebar_btn("🚪 Chiqish", self.on_close, text_color="#ef4444")

        # CONTENT AREA
        self.content_area = tk.Frame(self.main_container, bg=self.themes["light"]["content_bg"])
        self.content_area.pack(side="right", fill="both", expand=True)

        # Holatni saqlash
        self.current_view = None
        self.style = ttk.Style()
        self.update_style() # Initial style
        self.show_dashboard()

    def create_sidebar_btn(self, text, cmd, fg_color="transparent", hover_color="#34495e", text_color=None):
        btn = ctk.CTkButton(self.sidebar, text=text, command=cmd, 
                            fg_color=fg_color, hover_color=hover_color, text_color=text_color if text_color else "white",
                            font=("Segoe UI", 16), anchor="w", height=45, corner_radius=8)
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def check_password(self):
        # 1. Vaqtni tekshirish (Session check)
        current_time = time.time()
        if (current_time - self.last_auth_time) < self.auth_timeout:
            return True # 20 daqiqa o'tmagan, ruxsat beriladi
        
        # 2. Modern Password Dialog (Blocking)
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Xavfsizlik")
        dialog.geometry("340x220")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center Dialog
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - 170
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - 110
        dialog.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(dialog, text="🔑 Tizimga kirish", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(dialog, text="Davom etish uchun parolni kiriting", font=("Segoe UI", 12), text_color="gray").pack()
        
        entry = ctk.CTkEntry(dialog, show="*", width=220, height=35, font=("Segoe UI", 14), placeholder_text="Parol...")
        entry.pack(pady=15)
        entry.focus()
        
        self.password_result = None
        def on_confirm(event=None):
            self.password_result = entry.get()
            dialog.destroy()
            
        entry.bind("<Return>", on_confirm)
        ctk.CTkButton(dialog, text="Tasdiqlash", command=on_confirm, width=220, height=35, font=("Segoe UI", 12, "bold")).pack(pady=5)
        
        self.root.wait_window(dialog)
        
        # Verify
        role = None
        for r, p in self.users.items():
            if self.password_result == p:
                role = r
                break
        
        if role:
            self.last_auth_time = time.time()
            self.current_role = role
            self.show_toast(f"Muvaffaqiyatli kirildi! ({role.upper()})")
            return True
        else:
            if self.password_result is not None:
                messagebox.showerror("Xato", "Parol noto'g'ri!")
            return False

    def toggle_theme(self):
        # Toggle Mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.current_theme = "light"
            self.btn_theme.configure(text="🌙 Tungi Rejim")
        else:
            ctk.set_appearance_mode("Dark")
            self.current_theme = "dark"
            self.btn_theme.configure(text="☀ Kunduzgi Rejim")
            
        # Manually update Treeview
        self.update_treeview_style()
        
        # Refresh View
        if self.current_view == "dashboard": self.show_dashboard()
        elif self.current_view == "table": self.show_table()
        elif self.current_view == "trash": self.show_trash()
        
        # Update Styles for Treeview
    def update_treeview_style(self):
        # Native Treeview needs manual coloring to match CTk
        mode = ctk.get_appearance_mode()
        
        # Colors for Light/Dark
        bg = "#2b2b2b" if mode == "Dark" else "white"
        fg = "white" if mode == "Dark" else "#333333" 
        field = "#2b2b2b" if mode == "Dark" else "white"
        header_bg = "#34495e" if mode == "Dark" else "#e5e7eb"
        header_fg = "white" if mode == "Dark" else "#1f2937"
        
        self.style.theme_use("clam")
        
        # Configure Rows
        self.style.configure("Treeview", 
                             background=bg, 
                             foreground=fg, 
                             fieldbackground=field, 
                             rowheight=45, # Taller rows for readability
                             borderwidth=0, 
                             font=("Segoe UI", 14)) # Bigger Font
                             
        # Configure Header
        self.style.configure("Treeview.Heading", 
                             background=header_bg, 
                             foreground=header_fg, 
                             relief="flat",
                             font=("Segoe UI", 13, "bold"))
                             
        self.style.map("Treeview", background=[("selected", "#3b82f6")])



    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        self.current_view = "dashboard"
        
        t = self.themes[self.current_theme]
        
        # Header Frame
        head_frame = tk.Frame(self.content_area, bg=t["content_bg"])
        head_frame.pack(fill="x", padx=40, pady=(30,20))
        
        # Text
        tk.Label(head_frame, text="Boshqaruv Paneli", font=self.head_font, bg=t["content_bg"], fg=t["text"]).pack(side="left")
        
        # Logo Image in Dashboard
        try:
            dash_img = Image.open(self.icon_path).resize((100, 100))
            dash_photo = ImageTk.PhotoImage(dash_img)
            lbl = tk.Label(head_frame, image=dash_photo, bg=t["content_bg"])
            lbl.image = dash_photo 
            lbl.pack(side="right")
        except: pass
        
        # MAIN SPLIT FRAME (Left: Cards, Right: Chart)
        split_frame = tk.Frame(self.content_area, bg=t["content_bg"])
        split_frame.pack(fill="x", padx=30)
        
        # LEFT: STATS CARDS
        left_side = tk.Frame(split_frame, bg=t["content_bg"])
        left_side.pack(side="left", fill="both", expand=True)

        # 1. Row of cards
        self.create_modern_card(left_side, "Jami Tashkilotlar", len(self.data), "#3b82f6", "🏢")
        
        mahalla = sum(1 for i in self.data if "mfy" in str(i.get("m", "")).lower())
        maktab = sum(1 for i in self.data if "maktab" in str(i.get("m", "")).lower())
        bogcha = sum(1 for i in self.data if "mtt" in str(i.get("m", "")).lower())
        
        self.create_modern_card(left_side, "Mahallalar", mahalla, "#10b981", "🏘", pady=10)
        self.create_modern_card(left_side, "Maktablar", maktab, "#f59e0b", "🏫", pady=10)
        self.create_modern_card(left_side, "Bog'chalar", bogcha, "#8b5cf6", "🧸", pady=10)

        # RIGHT: DONUT CHART
        right_side = tk.Frame(split_frame, bg=t["content_bg"])
        right_side.pack(side="right", padx=20)
        
        self.draw_donut_chart(right_side, [
            ("Mahalla", mahalla, "#10b981"),
            ("Maktab", maktab, "#f59e0b"),
            ("Bog'cha", bogcha, "#8b5cf6")
        ])

        # Recent Activity
        tk.Label(self.content_area, text="So'nggi Faoliyat", font=("Segoe UI", 18, "bold"), bg=t["content_bg"], fg=t["text"]).pack(anchor="w", padx=40, pady=(40,15))
        
        # Log container
        log_frame = tk.Frame(self.content_area, bg=t["card_bg"], highlightbackground="#e2e8f0", highlightthickness=1)
        log_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        row_col = "#f1f5f9" if self.current_theme == "light" else "#334155"
        for i in range(5): # Dummy rows
            f = tk.Frame(log_frame, bg=t["card_bg"])
            f.pack(fill="x", pady=1)
            tk.Label(f, text=f"• Tizimga muvaffaqiyatli kirildi", font=("Segoe UI", 13), bg=t["card_bg"], fg=t["text"]).pack(side="left", padx=15, pady=12)
            tk.Label(f, text=time.strftime("%H:%M"), font=("Segoe UI", 11), bg=t["card_bg"], fg="#94a3b8").pack(side="right", padx=15)
            tk.Frame(log_frame, height=1, bg=row_col).pack(fill="x")

    def draw_donut_chart(self, parent, data):
        # Canvas based modern chart
        t = self.themes[self.current_theme]
        sz = 220
        canvas = tk.Canvas(parent, width=sz, height=sz, bg=t["content_bg"], bd=0, highlightthickness=0)
        canvas.pack()
        
        total = sum(d[1] for d in data)
        if total == 0: return
        
        start_deg = 90
        center = sz/2
        radius = 80
        width = 25
        
        for name, val, col in data:
            if val == 0: continue
            extent = (val / total) * 360
            
            # Draw Arc with Tag
            tag_name = f"slice_{name}"
            canvas.create_arc(center-radius, center-radius, center+radius, center+radius, 
                              start=start_deg, extent=-extent, style="arc", outline=col, width=width, tags=(tag_name, "slice"))
            
            # Bind Click
            canvas.tag_bind(tag_name, "<Button-1>", lambda e, n=name: self.filter_from_chart(n))
            canvas.tag_bind(tag_name, "<Enter>", lambda e, c=canvas, t=tag_name: c.itemconfigure(t, width=width+5))
            canvas.tag_bind(tag_name, "<Leave>", lambda e, c=canvas, t=tag_name: c.itemconfigure(t, width=width))
            
            start_deg -= extent
            
        # Draw Center Text
        canvas.create_text(center, center-10, text="Statistika", font=("Segoe UI", 10, "bold"), fill="#94a3b8")
        canvas.create_text(center, center+15, text=f"{total}", font=("Segoe UI", 20, "bold"), fill=t["text"])
        
        # Helper text
        tk.Label(parent, text="(Bo'limni ko'rish uchun bosing)", font=("Segoe UI", 8), bg=t["content_bg"], fg="#94a3b8").pack()

    def filter_from_chart(self, category):
        # Interactive filter
        map_cat = {
            "Mahalla": "Mahallalar",
            "Maktab": "Maktablar",
            "Bog'cha": "Bog'chalar"
        }
        target = map_cat.get(category, "Barchasi")
        self.cat_var.set(target)
        self.show_table() # Switch to table
        self.filter_data() # Apply filter
        self.show_toast(f"{target} bo'yicha saralandi!")

    def show_toast(self, message):
        # Modern non-blocking notification
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.geometry(f"300x50+{self.root.winfo_x() + self.root.winfo_width() - 320}+{self.root.winfo_y() + self.root.winfo_height() - 70}")
        toast.configure(bg="#333")
        
        tk.Label(toast, text=message, fg="white", bg="#333", font=("Segoe UI", 10)).pack(expand=True, fill="both")
        
        # Animation: Fade in/out (simulated by destroy after time)
        toast.after(3000, toast.destroy)

    def create_modern_card(self, parent, title, value, color, icon, pady=5):
        t = self.themes[self.current_theme]
        # Outer frame for shadow/border
        card_border = tk.Frame(parent, bg="#e2e8f0" if self.current_theme == "light" else "#334155", padx=1, pady=1)
        card_border.pack(side="top", fill="x", expand=True, pady=pady)
        
        # Inner card
        card = tk.Frame(card_border, bg=t["card_bg"])
        card.pack(fill="both", expand=True)
        
        # Left color strip
        tk.Frame(card, bg=color, width=4).pack(side="left", fill="y")
        
        # Content
        content = tk.Frame(card, bg=t["card_bg"], padx=15, pady=15)
        content.pack(fill="both", expand=True)
        
        # Icon circle (simulated)
        icon_lbl = tk.Label(content, text=icon, font=("Segoe UI", 18), bg=t["card_bg"], fg=color)
        icon_lbl.pack(side="left", anchor="center")
        
        # Text
        info = tk.Frame(content, bg=t["card_bg"])
        info.pack(side="left", padx=(15, 0))
        tk.Label(info, text=title, font=("Segoe UI", 9, "bold"), fg="#64748b", bg=t["card_bg"]).pack(anchor="w")
        tk.Label(info, text=str(value), font=("Segoe UI", 18, "bold"), fg=t["text"], bg=t["card_bg"]).pack(anchor="w")

    def show_trash(self):
        self.clear_content()
        self.current_view = "trash"
        
        # TITLE with Theme support colors
        ctk.CTkLabel(self.content_area, text="Chiqindi Qutisi (Trash)", font=("Segoe UI", 26, "bold"), text_color=("#c0392b", "#e74c3c")).pack(anchor="w", padx=30, pady=20)
        ctk.CTkLabel(self.content_area, text="O'chirilgan ma'lumotlarni tiklashingiz yoki butunlay o'chirishingiz mumkin", font=("Segoe UI", 12), text_color="gray").pack(anchor="w", padx=35)

        # TABLE CONTAINER
        tree_frame = ctk.CTkFrame(self.content_area)
        tree_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        # TABLE
        self.update_treeview_style()
        self.trash_tree = ttk.Treeview(tree_frame, columns=("m","f","date"), show="headings")
        
        self.trash_tree.heading("m", text="Tashkilot Nomi"); self.trash_tree.column("m", width=300)
        self.trash_tree.heading("f", text="Rahbar"); self.trash_tree.column("f", width=200)
        self.trash_tree.heading("date", text="O'chirilgan vaqt"); self.trash_tree.column("date", width=150)
        
        self.trash_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # LOAD DATA
        for i in self.data_manager.trash:
            self.trash_tree.insert("", "end", values=(i.get("m"), i.get("f"), i.get("deleted_at","-")))

        # ACTIONS
        btn_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(btn_frame, text="♻ Tiklash", fg_color="#27ae60", height=40, font=("Segoe UI", 12, "bold"), command=self.restore_item).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔥 Butunlay O'chirish", fg_color="#c0392b", height=40, hover_color="#a93226", font=("Segoe UI", 12, "bold"), command=self.perm_delete_item).pack(side="left", padx=5)

    def restore_item(self):
        sel = self.trash_tree.selection()
        if not sel: return
        for s in sel:
            v = self.trash_tree.item(s)["values"]
            # Find in trash by name and director (simple match)
            item = next((i for i in self.data_manager.trash if i.get("m") == v[0] and i.get("f") == v[1]), None)
            if item:
                self.data_manager.restore_from_trash(item)
        self.show_trash()
        self.filter_data() # Update main table if it's visible
        messagebox.showinfo("OK", "Ma'lumotlar tiklandi!")

    def perm_delete_item(self):
        sel = self.trash_tree.selection()
        if not sel: return
        if not messagebox.askyesno("Diqqat", "Rostdan ham butunlay o'chirmoqchimisiz? Qaytarib bo'lmaydi!"): return
        
        for s in sel:
            v = self.trash_tree.item(s)["values"]
            item = next((i for i in self.data_manager.trash if i.get("m") == v[0] and i.get("f") == v[1]), None)
            if item:
                self.data_manager.permanent_delete(item)
        self.show_trash()

        self.show_trash()

    def show_settings(self):
        # SECURITY CHECK
        if not self.check_password(): return

        self.clear_content()
        self.current_view = "settings"
        
        ctk.CTkLabel(self.content_area, text="Sozlamalar", font=("Segoe UI", 26, "bold"), text_color=("#2c3e50", "white")).pack(anchor="w", padx=30, pady=20)
        ctk.CTkLabel(self.content_area, text="Tashkilot turlarini (Kategoriyalarni) boshqarish", font=("Segoe UI", 12), text_color="gray").pack(anchor="w", padx=35)
        
        # Add New Category
        add_frame = ctk.CTkFrame(self.content_area)
        add_frame.pack(fill="x", padx=30, pady=20)
        
        self.new_cat_var = tk.StringVar()
        ctk.CTkLabel(add_frame, text="Yangi tur qo'shish:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=15, pady=15)
        ctk.CTkEntry(add_frame, textvariable=self.new_cat_var, width=250, height=35, placeholder_text="Masalan: Hokim Yordamchilari").pack(side="left", padx=5)
        
        def add_cat():
            if not self.check_password(): return # Security
            new_c = self.new_cat_var.get().strip()
            if not new_c: return
            if new_c in self.data_manager.categories:
                self.show_toast("Bu tur allaqachon mavjud!")
                return
            
            self.data_manager.categories.append(new_c)
            self.data_manager.save_categories()
            self.new_cat_var.set("")
            self.show_toast(f"'{new_c}' qo'shildi!")
            refresh_list()
        
        ctk.CTkButton(add_frame, text="+ Qo'shish", command=add_cat, fg_color="#27ae60", width=100, height=35).pack(side="left", padx=10)

        # List of Categories
        list_frame = ctk.CTkFrame(self.content_area)
        list_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(list_frame, text="Mavjud Turlar:", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=10)
        
        scroll = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        def refresh_list():
            for w in scroll.winfo_children(): w.destroy()
            for cat in self.data_manager.categories:
                r = ctk.CTkFrame(scroll, fg_color=("white", "#333"), height=40)
                r.pack(fill="x", pady=2)
                
                ctk.CTkLabel(r, text=cat, font=("Segoe UI", 12)).pack(side="left", padx=15, pady=5)
                
                if cat not in ["Mahalla (MFY)", "Maktab", "Bog'cha (MTT)"]: # Prevent deleting core if needed, or allow all
                    ctk.CTkButton(r, text="🗑", width=30, height=30, fg_color="#c0392b", command=lambda c=cat: delete_cat(c)).pack(side="right", padx=5, pady=5)
        
        def delete_cat(cat):
            if not self.check_password(): return # Security
            if messagebox.askyesno("O'chirish", f"'{cat}' turini o'chirmoqchimisiz?"):
                self.data_manager.categories.remove(cat)
                self.data_manager.save_categories()
                refresh_list()
                self.show_toast("O'chirildi!")

        refresh_list()

    def show_table(self):
        self.clear_content()
        self.current_view = "table"
        
        # Determine colors based on theme
        bg = self.themes[self.current_theme]["content_bg"]
        
        # TOOLBAR
        ctrl = ctk.CTkFrame(self.content_area, fg_color="transparent")
        ctrl.pack(fill="x", padx=20, pady=(20, 10))
        
        # Search Container
        search_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
        search_frame.pack(side="left", fill="x")

        # Filter Type
        self.f_type = ctk.CTkComboBox(search_frame, values=["Nomi", "F.I.SH", "INN", "Izoh"], width=120, height=40, font=("Segoe UI", 12))
        self.f_type.set("Nomi")
        self.f_type.pack(side="left", padx=(0, 10))
        # CTk ComboBox command logic if needed (or just query it)

        # Search Entry
        self.s_var = tk.StringVar(); self.s_var.trace("w", self.filter_data)
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.s_var, width=300, height=40, font=("Segoe UI", 14), placeholder_text="Qidiruv...")
        search_entry.pack(side="left", padx=5)
        
        # Clear Button
        ctk.CTkButton(search_frame, text="✖", width=40, height=40, fg_color="#e74c3c", command=lambda: self.s_var.set("")).pack(side="left", padx=5)

        # Action Buttons Container
        btn_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_frame.pack(side="right")

        # Button Helper
        def add_btn(txt, cmd, col, icon=None):
            ctk.CTkButton(btn_frame, text=txt, command=cmd, fg_color=col, height=40, font=("Segoe UI", 12, "bold"), width=100).pack(side="right", padx=3)

        add_btn("📝 Izoh", self.manual_edit_comment, "#8e44ad")
        add_btn("📱 QR", self.show_qr, "#e67e22")
        add_btn("✈ Telegram", self.send_telegram, "#0088cc")
        add_btn("📊 Excel", self.open_export_menu, "#107c41")
        add_btn("✏ Tahrir", self.edit_item, "#f39c12")
        
        # Add Button (Primary)
        ctk.CTkButton(btn_frame, text="+ Qo'shish", command=self.add_item, fg_color="#27ae60", height=40, font=("Segoe UI", 13, "bold"), width=120).pack(side="right", padx=10)

        # CATEGORY TABS (Dynamic)
        cat_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        cat_frame.pack(fill="x", padx=20, pady=10)
        
        if not hasattr(self, 'cat_var'): self.cat_var = tk.StringVar(value="Barchasi")
        
        # Dynamic tabs from DataManager
        tabs = ["Barchasi"] + self.data_manager.categories
        seg_btn = ctk.CTkSegmentedButton(cat_frame, values=tabs, 
                                         variable=self.cat_var, command=self.filter_data_seg,
                                         font=("Segoe UI", 12, "bold"), height=35)
        seg_btn.pack(side="left", fill="x", expand=True)
        seg_btn.set("Barchasi") # Default

        # TABLE CONTAINER
        tree_frame = ctk.CTkFrame(self.content_area)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # TABLE
        self.update_treeview_style() # Ensure style is refreshed
        self.tree = ttk.Treeview(tree_frame, columns=("s","m","f","t","inn","inn_val","izoh"), show="headings") # fixed columns
        
        # Note: columns logic might need adjustment if logic relies on indices. 
        # Using same columns as before: ("s","m","f","t","inn","izoh") in previous code
        self.tree = ttk.Treeview(tree_frame, columns=("s","m","f","t","inn","izoh"), show="headings")
        
        headers = [("s","Turi", 80), ("m","Tashkilot Nomi", 300), ("f","F.I.SH", 200), 
                   ("t","Tel", 100), ("inn","INN", 100), ("izoh","Izoh (Enter=Tahrir)", 200)]
        
        for col, name, width in headers:
            self.tree.heading(col, text=name, command=lambda c=col: self.sort_treeview(c, False))
            self.tree.column(col, width=width, anchor="center" if col != "m" else "w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Double-1>", self.on_double_click) 
        self.tree.bind("<Return>", self.edit_comment_inline) # Enter key binding

        self.update_table(self.filtered_data) # Load current filtered data

    def filter_data_seg(self, value):
        self.cat_var.set(value)
        self.filter_data()
        
    def manual_edit_comment(self):
        # Button trigger for inline edit
        self.edit_comment_inline(None)

    def edit_comment_inline(self, event):
        # Get selected item
        sel = self.tree.focus()
        if not sel: return
        
        # Ensure item is visible
        self.tree.see(sel)
        self.root.update_idletasks() # Ensure layout is calculated
        
        # Get coordinates of the "izoh" column cell
        try:
            bbox = self.tree.bbox(sel, "izoh")
            if not bbox: return # Column not visible
            x, y, w, h = bbox
        except: return 
        
        # Create Entry widget overlay
        # Frame helps with border visibility if needed, but direct Entry is usually enough
        entry = tk.Entry(self.tree, font=("Arial", self.font_size))
        entry.place(x=x, y=y, width=w, height=h)
        
        # Set current value
        current_val = self.tree.item(sel)["values"][5] # Izoh is @ index 5
        entry.insert(0, str(current_val))
        entry.select_range(0, tk.END)
        entry.focus_force() # Force focus

        def save_edit(event):
            new_text = entry.get()
            # 1. Update UI
            current_values = list(self.tree.item(sel)["values"])
            current_values[5] = new_text
            self.tree.item(sel, values=current_values)
            
            # 2. Update Data Source
            inn = str(current_values[4])
            item = next((i for i in self.data if str(i.get("inn")) == inn), None)
            if item:
                item["izoh"] = new_text
                self.data_manager.save_data()
            
            entry.destroy()
            self.tree.focus_set() # Return focus to tree
            self.tree.focus(sel)  # Ensure item is focused
            
            self.sync_background() # Auto Sync

        def cancel_edit(event):
            entry.destroy()
            self.tree.focus_set() # Return focus to tree

        entry.bind("<Return>", save_edit) # Enter saves
        entry.bind("<Escape>", cancel_edit) # Esc cancels

    def open_cloud_menu(self):
        # Mini menu implementation for sidebar button
        win = tk.Toplevel(self.root)
        win.title("Cloud"); win.geometry("300x150")
        win.configure(bg=self.themes[self.current_theme]["content_bg"]) # Theme fix
        
        tk.Label(win, text="GitHub Cloud Sinxronlash", font=("Arial", 12, "bold"), bg=self.themes[self.current_theme]["content_bg"], fg=self.themes[self.current_theme]["text"]).pack(pady=10)
        tk.Button(win, text="☁ Ma'lumotni Yuklash (Upload)", bg="#27ae60", fg="white", command=self.upload_to_github).pack(fill="x", padx=20, pady=5)
        tk.Button(win, text="☁ Ma'lumotni Olish (Download)", bg="#e67e22", fg="white", command=self.download_from_github).pack(fill="x", padx=20, pady=5)

    def open_export_menu(self):
         # Mini menu implementation
        win = tk.Toplevel(self.root)
        win.title("Export"); win.geometry("300x200")
        win.configure(bg=self.themes[self.current_theme]["content_bg"]) # Theme fix

        tk.Button(win, text="📥 Joriy Jadvalni Excelga Yuklash", bg="#1f618d", fg="white", command=self.export_excel_pro).pack(fill="x", padx=20, pady=5)
        tk.Button(win, text="📊 Google Sheet (Dummy)", bg="#107c41", fg="white", command=self.export_to_gsheet_dummy).pack(fill="x", padx=20, pady=5)
        tk.Button(win, text="🔄 Google Sheet Sync (Real)", bg="#2ecc71", fg="white", command=self.open_gsheet_sync_menu).pack(fill="x", padx=20, pady=5)

    def open_gsheet_sync_menu(self):
        if self.current_role != "admin": # Restriction
            messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN!"); return

        win = tk.Toplevel(self.root)
        win.title("Sozlamalar")
        win.geometry("350x250")
        
        ctk.CTkLabel(win, text="Google Sheets Integratsiyasi", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        # Key File Status
        key_status = "✅ Fayl mavjud" if os.path.exists("service_account.json") else "❌ Fayl yo'q"
        lbl_status = ctk.CTkLabel(win, text=f"Key File: {key_status}", text_color="green" if "mavjud" in key_status else "red")
        lbl_status.pack()
        
        def select_key():
            path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
            if path:
                try:
                    shutil.copy(path, "service_account.json")
                    lbl_status.configure(text="✅ Fayl mavjud", text_color="green")
                    messagebox.showinfo("OK", "Kalit fayl o'rnatildi!")
                except Exception as e: messagebox.showerror("Xato", str(e))
        
        if not os.path.exists("service_account.json"):
            ctk.CTkButton(win, text="🔑 Kalit Faylni Tanlash", command=select_key).pack(pady=10)
        else:
            ctk.CTkLabel(win, text="Avtomatik Sinxronizatsiya: YOQILGAN 🟢", font=("Segoe UI", 14, "bold"), text_color="#2ecc71").pack(pady=20)
            ctk.CTkLabel(win, text="Barcha o'zgarishlar o'zi saqlanadi.", font=("Segoe UI", 12), text_color="gray").pack()
            
            # Small re-auth button
            ctk.CTkButton(win, text="🔑 Kalitni Yangilash", command=select_key, height=24, width=120, fg_color="#7f8c8d").pack(pady=(20, 0))

    def sync_background(self):
        # Auto Sync trigger
        threading.Thread(target=self.do_sync, args=("upload", self.sheet_identifier, True), daemon=True).start()

    def do_sync(self, direction, sheet_name="MahallaBazasi", silent=False):
        if not os.path.exists("service_account.json"):
            if not silent: messagebox.showerror("Xato", "Kalit fayl topilmadi!")
            return
        
        # Save config if manual sync
        if not silent:
            self.sheet_identifier = sheet_name
            self.save_sync_config(sheet_name)
        
        if silent:
            self.lbl_sync.configure(text="☁ Yuklanmoqda...", text_color="#f39c12")
        
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
            client = gspread.authorize(creds)
            
            try: 
                 val = sheet_name.strip()
                 logging.info(f"Connecting to sheet input: {val}")
                 
                 # Extract ID using Regex (Best method)
                 # Matches .../d/THIS_PART/...
                 match = re.search(r"/d/([a-zA-Z0-9-_]+)", val)
                 
                 if match:
                     sheet_id = match.group(1)
                     logging.info(f"Extracted Sheet ID: {sheet_id}")
                     spreadsheet = client.open_by_key(sheet_id)
                 elif val.startswith("http"): 
                      # Fallback for weird URLs
                      spreadsheet = client.open_by_url(val)
                 else: 
                      spreadsheet = client.open(val)
            except Exception as e: 
                logging.error(f"Sheet Open Failed: {e}")
                if direction == "upload" and not val.startswith("http"): # Only create if name provided
                    spreadsheet = client.create(val); client.insert_permission(spreadsheet.id, None, perm_type='anyone', role='reader')
                else: 
                     if silent: self.lbl_sync.configure(text="❌ Sheet topilmadi", text_color="red"); return
                     raise Exception("Sheet topilmadi (Nomini to'g'ri yozing yoki Linkni qo'ying)")

            sheet = spreadsheet.sheet1
            
            if direction == "upload":
                # Upload Logic
                data_to_upload = [["Turi", "Nomi", "Rahbar", "Tel", "INN", "Izoh", "ID"]] # Header + ID
                for i in self.data:
                        data_to_upload.append([
                            i.get("s"), i.get("m"), i.get("f"), i.get("t"), str(i.get("inn")), i.get("izoh", ""), i.get("uuid", "")
                        ])
                
                sheet.clear()
                sheet.update(data_to_upload)
                logging.info("Upload Successful")
                
                if silent:
                     self.lbl_sync.configure(text="✅ Bulutda", text_color="#2ecc71")
                else:
                    messagebox.showinfo("OK", "Ma'lumotlar Google Sheetga yuklandi!")
                    webbrowser.open(f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
                
            elif direction == "download":
                # Download Logic
                raw_data = sheet.get_all_records()
                logging.info(f"Downloaded {len(raw_data)} records")
                new_db = []
                for row in raw_data:
                    new_db.append({
                        "s": row.get("Turi"), "m": row.get("Nomi"), "f": row.get("Rahbar"),
                        "t": row.get("Tel"), "inn": str(row.get("INN")), "izoh": row.get("Izoh")
                    })
                
                self.data = new_db
                self.data_manager.data = self.data
                self.save_data()
                self.filter_data()
                if not silent: messagebox.showinfo("OK", "Ma'lumotlar Google Sheetdan yuklab olindi!")

        except Exception as e: 
            err_msg = str(e)
            logging.error(f"Sync Error: {err_msg}\n{traceback.format_exc()}")
            
            if "operation is not supported" in err_msg or "400" in err_msg:
                 friendly_msg = "XATO: Siz Excel (.xlsx) fayl ulagansiz!\nIltimos, Google Sheetni ochib 'File -> Save as Google Sheets' qiling va yangi linkni ishlating."
                 if not silent: messagebox.showerror("Format Xatosi", friendly_msg)
                 else: print(friendly_msg) # console fallback
            elif silent:
                self.lbl_sync.configure(text="❌ Xato", text_color="red")
            else:
                messagebox.showerror("Xato", f"Google Sheet Xatosi:\n{err_msg}")
    
    def on_double_click(self, event):
        self.edit_item()

    def sort_treeview(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            # Try numeric sort if possible
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))


    def filter_data(self, *args):
        if self.current_view != "table": return
        q = self.s_var.get().lower().strip() # Added strip()
        cat = self.cat_var.get()
        tp = self.f_type.get()
        
        res = []
        res = []
        for i in self.data:
            n = str(i.get("m", "")).lower()
            # Dynamic Filter Logic (Strict + Legacy Support)
            s_val = str(i.get("s", "")).strip()
            
            # 1. Exact Match (Primary for New Categories)
            is_match = (s_val == cat)
            
            # 2. Legacy Support for Renamed Core Categories
            if not is_match:
                if cat == "Mahalla (MFY)" and s_val in ["Mahalla", "MFY"]: is_match = True
                elif cat == "Maktab" and s_val in ["Maktablar"]: is_match = True
                elif cat == "Bog'cha (MTT)" and s_val in ["MTT", "Bog'cha"]: is_match = True
            
            match_cat = (cat == "Barchasi") or is_match
             
            if match_cat:
                target = ""
                if tp == "Nomi": target = n
                elif tp == "F.I.SH": target = str(i.get("f","")).lower()
                elif tp == "INN": target = str(i.get("inn",""))
                elif tp == "Izoh": target = str(i.get("izoh","")).lower()
                
                # Check for substring match
                if q in target: res.append(i)
                
        self.filtered_data = res
        self.update_table(res)

    def update_table(self, d_list):
        for r in self.tree.get_children(): self.tree.delete(r)
        
        # Respecting current sort would be ideal, but simply appending matches user expectations for "Filtered View"
        for i in d_list:
            self.tree.insert("", "end", values=(
                i.get("s","-"), i.get("m","-"), i.get("f","-"), 
                i.get("t","-"), i.get("inn","-"), i.get("izoh", "")
            ))
        
        # Set focus to top item for keyboard nav
        if self.tree.get_children():
            first = self.tree.get_children()[0]
            self.tree.selection_set(first)
            self.tree.focus(first)

    # --- PRO FUNKSIYALAR ---

    def export_excel_pro(self):
        # Exports ONLY the currently filtered data (Smart Export)
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not path: return
        
        try:
            wb = openpyxl.Workbook()
            ws = wb.active; ws.title = f"Tashkilotlar - {self.cat_var.get()}" if hasattr(self, 'cat_var') else "Tashkilotlar"
            ws.append(["Turi", "Nomi", "Rahbar", "Tel", "INN", "Izoh"])
            
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = openpyxl.styles.PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")

            # Uses self.filtered_data which contains exactly what is shown on screen (filtered by search OR category)
            for i in self.filtered_data:
                ws.append([i.get("s"), i.get("m"), i.get("f"), i.get("t"), i.get("inn"), i.get("izoh", "")])
            
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length: max_length = len(str(cell.value))
                    except: pass
                ws.column_dimensions[column].width = max_length + 2

            wb.save(path); messagebox.showinfo("OK", f"Excel fayl saqlandi! ({len(self.filtered_data)} ta tashkilot)")
        except Exception as e: messagebox.showerror("Xato", str(e))

    def upload_to_github(self, auto=False):
        if auto:
            # Auto mode: Sillent upload
            gist_id = ""
            if os.path.exists("gist_config.txt"):
                 with open("gist_config.txt", "r") as f: gist_id = f.read().strip()
            if gist_id:
                try:
                    # Token should be saved securely, but for now we assume it's prompted or stored elsewhere?
                    # The original code only prompted for token. 
                    # If auto is True, we can't prompt. 
                    # For now, let's just skip if no token mechanism exists for auto.
                    pass 
                except: pass
            return

        token = simpledialog.askstring("GitHub Token", "GitHub Tokeningizni kiriting:")
        if not token: return
        
        gist_content = {
            "description": "Pop Tumani Bazasi", "public": False,
            "files": {"mahalla_bazasi.json": {"content": json.dumps(self.data, indent=4, ensure_ascii=False)}}
        }
        try:
            r = requests.post("https://api.github.com/gists", json=gist_content, headers={"Authorization": f"token {token}"})
            if r.status_code == 201:
                with open("gist_config.txt", "w") as f: f.write(r.json()['id'])
                messagebox.showinfo("OK", "Baza Cloudga yuklandi!")
            else: messagebox.showerror("Xato", "Internet yoki Token xatosi!")
        except Exception as e: messagebox.showerror("Xato", str(e))

    def download_from_github(self):
        gist_id = ""
        if os.path.exists("gist_config.txt"):
            with open("gist_config.txt", "r") as f: gist_id = f.read().strip()
        
        if not gist_id:
            gist_id = simpledialog.askstring("Gist ID", "Baza ID raqamini kiriting:")
        if not gist_id: return

        try:
            r = requests.get(f"https://api.github.com/gists/{gist_id}")
            if r.status_code == 200:
                self.data = json.loads(r.json()['files']['mahalla_bazasi.json']['content'])
                self.data_manager.data = self.data # Update manager data
                self.save_data(); self.filter_data()
                messagebox.showinfo("OK", "Baza yangilandi!")
            else: messagebox.showerror("Xato", "Baza topilmadi!")
        except Exception as e: messagebox.showerror("Xato", str(e))

    def export_to_gsheet_dummy(self):
        # Siz yuborgan Google Sheet havolasi
        url = "https://docs.google.com/spreadsheets/d/1l4MVpVGoyWMP_9Px9QG4V3hWLdQf9LlJ/edit?gid=779517247"
        
        # Havolani brauzerda ochish
        webbrowser.open(url)
        messagebox.showinfo("Google Sheet", "Jadval brauzerda ochildi!")

    # --- YORDAMCHI FUNKSIYALAR ---

    def edit_item(self):
        if not self.check_password(): return # Password Protected
        sel = self.tree.focus()
        if sel:
            v = self.tree.item(sel)["values"]
            item = next((i for i in self.data if i.get("inn") == str(v[4])), None)
            if item: self.open_win("Tahrirlash", item)

    def add_item(self): 
        if not self.check_password(): return # Password Protected
        self.open_win("Yangi qo'shish")

    def open_win(self, title, item=None):
        win = ctk.CTkToplevel(self.root)
        win.title(title)
        win.geometry("450x600")
        win.transient(self.root) 
        win.grab_set()
        
        # Center
        x = self.root.winfo_x() + (self.root.winfo_width()//2) - 225
        y = self.root.winfo_y() + (self.root.winfo_height()//2) - 300
        win.geometry(f"+{x}+{y}")
        
        # Header
        ctk.CTkLabel(win, text=title, font=("Segoe UI", 22, "bold"), text_color=("#2c3e50", "#ecf0f1")).pack(pady=(25, 10))
        ctk.CTkLabel(win, text="ma'lumotlarni to'ldiring", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 20))

        # Fields Config
        # Dynamic Options from DataManager
        cat_opts = self.data_manager.categories
        
        form_config = [
            ("s", "Tashkilot Turi", "combo", cat_opts),
            ("m", "Tashkilot Nomi", "entry", None),
            ("f", "Rahbar (F.I.SH)", "entry", None),
            ("t", "Telefon Raqam", "entry", None),
            ("inn", "INN (Soliq to'lovchi)", "entry", None),
            ("izoh", "Qo'shimcha Izoh", "entry", None),
        ]
        
        widgets = {}
        
        widgets = {}
        
        # Scrollable Container for Fields
        container = ctk.CTkScrollableFrame(win, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        for key, lbl, w_type, opts in form_config:
            ctk.CTkLabel(container, text=lbl, font=("Segoe UI", 12, "bold"), anchor="w").pack(fill="x", pady=(5,0))
            
            if w_type == "combo":
                w = ctk.CTkComboBox(container, values=opts, height=35, font=("Segoe UI", 13))
            else:
                w = ctk.CTkEntry(container, height=35, font=("Segoe UI", 13))
                
            w.pack(fill="x", pady=(0, 8))
            widgets[key] = w
            
            # Pre-fill
            if item:
                val = item.get(key, "")
                if w_type == "combo": w.set(val)
                else: w.insert(0, val)
        
        # Bind Input Mask for Phone
        if "t" in widgets:
             # CTkEntry contains a specialized entry, need to bind to internal entry or wrapper. 
             # CTkEntry events are usually passed through.
             widgets["t"].bind("<KeyRelease>", self.format_phone_input)
        
        def save():
            # VALIDATION
            val_inn = widgets["inn"].get()
            val_name = widgets["m"].get()
            
            if not val_name:
                self.show_toast("Xatolik: Tashkilot nomi kiritilmadi!"); return
            if val_inn and not val_inn.isdigit(): 
                 self.show_toast("Xatolik: INN raqam bo'lishi kerak!"); return

            # 1. Collect Data
            d = {}
            for key, _, w_type, _ in form_config:
                d[key] = widgets[key].get()
            
            # 2. Save
            if item: 
                self.data[self.data.index(item)] = d
            else: 
                self.data.append(d)
            
            # 3. Persist
            self.save_data() 
            self.filter_data()
            
            # 5. Close
            win.destroy()
            self.show_toast("Muvaffaqiyatli saqlandi!")
            
            self.sync_background() # Auto Sync
        
        ctk.CTkButton(win, text="SAQLASH", command=save, height=50, font=("Segoe UI", 14, "bold"), fg_color="#27ae60", hover_color="#2ecc71").pack(fill="x", padx=40, pady=20)

    def format_phone_input(self, event):
        # Auto-format: (99) 123-45-67
        entry = event.widget
        if event.keysym == "BackSpace": return # Let user delete freely
        
        text = entry.get()
        digits = "".join(filter(str.isdigit, text))
        
        formatted = digits
        if len(digits) > 9: digits = digits[:9] # Max 9 digits (excluding +998)
        
        if len(digits) > 0:
            formatted = f"({digits[:2]}"
        if len(digits) > 2:
            formatted += f") {digits[2:5]}"
        if len(digits) > 5:
            formatted += f"-{digits[5:7]}"
        if len(digits) > 7:
            formatted += f"-{digits[7:9]}"
            
        entry.delete(0, tk.END)
        entry.insert(0, formatted)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item: 
            self.tree.selection_set(item)
            # Recreate menu to include Delete
            self.context_menu = tk.Menu(self.root, tearoff=0)
            self.context_menu.add_command(label="📞 Tel nusxalash", command=lambda: self.copy_cell(3))
            self.context_menu.add_command(label="🆔 INN nusxalash", command=lambda: self.copy_cell(4))
            self.context_menu.add_command(label="📝 Izohni nusxalash", command=lambda: self.copy_cell(5))
            self.context_menu.add_separator()
            self.context_menu.add_command(label="📋 Qatorni nusxalash", command=self.copy_row)
            self.context_menu.add_separator()
            self.context_menu.add_command(label="🗑 Chiqindiga tashlash", command=self.delete_selected_item, foreground="red")
            
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected_item(self):
        if not self.check_password(): return # Password Protected
        if self.current_role != "admin":
             messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN o'chira oladi!"); return
        
        sel = self.tree.selection()
        if not sel: return
        if not messagebox.askyesno("O'chirish", "Haqiqatan ham bu ma'lumotni o'chirmoqchimisiz? (Keyinroq Trashdan tiklashingiz mumkin)"): return
        
        v = self.tree.item(sel)["values"]
        # Find item securely
        item = next((i for i in self.data if i.get("inn") == str(v[4])), None)
        if item:
            self.data_manager.move_to_trash(item)
            self.filter_data()
            self.sync_background() # Auto Sync
            messagebox.showinfo("O'chirildi", "Ma'lumot Chiqindi qutisiga joylandi.")

    def restore_item(self):
        if not self.check_password(): return # Password Protected
        if self.current_role != "admin":
             messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN tiklay oladi!"); return

        sel = self.trash_tree.selection()
        if not sel: return
        for s in sel:
            v = self.trash_tree.item(s)["values"]
            # Find in trash by name and director (simple match)
            item = next((i for i in self.data_manager.trash if i.get("m") == v[0] and i.get("f") == v[1]), None)
            if item:
                self.data_manager.restore_from_trash(item)
        self.show_trash()
        self.filter_data() # Update main table if it's visible
        self.sync_background() # Auto Sync
        messagebox.showinfo("OK", "Ma'lumotlar tiklandi!")

    def perm_delete_item(self):
        if not self.check_password(): return # Password Protected
        if self.current_role != "admin":
             messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN o'chira oladi!"); return

        sel = self.trash_tree.selection()
        if not sel: return
        if not messagebox.askyesno("Diqqat", "Rostdan ham butunlay o'chirmoqchimisiz? Qaytarib bo'lmaydi!"): return
        
        for s in sel:
            v = self.trash_tree.item(s)["values"]
            item = next((i for i in self.data_manager.trash if i.get("m") == v[0] and i.get("f") == v[1]), None)
            if item:
                self.data_manager.permanent_delete(item)
        self.show_trash()
        self.sync_background() # Auto Sync

    def copy_cell(self, idx):
        try:
            sel = self.tree.item(self.tree.selection()[0])["values"]
            pyperclip.copy(str(sel[idx])); messagebox.showinfo("OK", "Nusxalandi!")
        except: pass

    def copy_row(self):
        try:
            sel = self.tree.item(self.tree.selection()[0])["values"]
            pyperclip.copy("\t".join(map(str, sel))); messagebox.showinfo("OK", "Nusxalandi!")
        except: pass # Xatolik bo'lsa indamaydi
    
    def send_telegram(self):
        try:
            v = self.tree.item(self.tree.focus())["values"]
            izoh = f"\n📝 {v[5]}" if v[5] else ""
            pyperclip.copy(f"🏢 {v[1]}\n👤 {v[2]}\n📞 {v[3]}\n🆔 {v[4]}{izoh}")
            messagebox.showinfo("OK", "Telegramga tayyor!")
        except: pass

    def show_qr(self):
        try:
            sel = self.tree.focus()
            if not sel: return
            v = self.tree.item(sel)["values"]
            
            # Telefon raqamni tozalash
            raw_tel = str(v[3])
            tel = "".join(filter(str.isdigit, raw_tel))
            
            # Normalization
            if len(tel) == 9: 
                tel = "+998" + tel
            elif len(tel) == 12 and tel.startswith("998"):
                tel = "+" + tel
            # Agar boshqa format bo'lsa, o'zgarishsiz qoladi yoki "+" qo'shiladi
            
            # Create QR Data (Raw Number)
            data = tel
            
            qr = qrcode.make(data)
            qr.save("t.png")
            
            # Show Window
            w = tk.Toplevel(self.root)
            w.title("QR Code (Telefon)")
            w.geometry("300x400")
            
            # Load Image
            img = Image.open("t.png")
            img = img.resize((250, 250)) 
            i = ImageTk.PhotoImage(img)
            
            l = tk.Label(w, image=i)
            l.image = i 
            l.pack(pady=20)
            
            tk.Label(w, text=f"{v[1]}", font=("Segoe UI", 12, "bold")).pack()
            tk.Label(w, text=f"{tel}", font=("Segoe UI", 14, "bold"), fg="blue").pack(pady=5)
            tk.Label(w, text="(Skaner qiling va qo'ng'iroq tugmasini bosing)", font=("Segoe UI", 9), fg="gray").pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("QR Xatosi", f"QR Kod yaratishda xatolik:\n{str(e)}")

    def change_font(self, delta): self.font_size += delta; self.update_style()
    def update_style(self):
        self.style.configure("Treeview", font=("Arial", self.font_size), rowheight=self.font_size*3)
        
        if self.current_theme == "dark":
            self.style.configure("Treeview", background="#34495e", foreground="white", fieldbackground="#34495e")
            self.style.configure("Treeview.Heading", font=("Arial", self.font_size, "bold"), background="#2c3e50", foreground="white") # Dark Header
            self.style.map("Treeview", background=[("selected", "#3498db")])
        else:
            self.style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
            self.style.configure("Treeview.Heading", font=("Arial", self.font_size, "bold"), background="#ecf0f1", foreground="black") # Light Header
            self.style.map("Treeview", background=[("selected", "#3498db")])

if __name__ == "__main__":
    root = ctk.CTk()
    app = MahallaDasturi(root)
    root.mainloop()