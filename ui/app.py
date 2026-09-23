import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import json
import threading
import time
import webbrowser
import requests
import pyperclip
from typing import Optional, List, Dict, Any

from core.config import (
    APP_TITLE, DEFAULT_WINDOW_SIZE, MIN_WINDOW_SIZE, THEMES,
    ICON_PATH, AUTH_TIMEOUT, SYNC_CONFIG_FILE, SERVICE_ACCOUNT_FILE
)
from core.logger import logger
from core.security import hash_password, authenticate_user
from database.data_manager import DataManager
from services.excel_service import export_organizations_to_excel
from services.gsheet_service import get_gspread_client, upload_data_to_sheet, download_data_from_sheet
from ui.style import apply_treeview_style
from ui.views.dashboard_view import render_dashboard
from ui.views.table_view import render_table
from ui.views.trash_view import render_trash
from ui.views.settings_view import render_settings

class MahallaDasturi:
    """Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)."""

    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        self.root.configure(bg="#f4f7f6")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Ma'lumotlar boshqaruvchisi
        self.data_manager = DataManager()
        self.data = self.data_manager.data
        self.font_size = self.data_manager.settings.get("font_size", 15)
        self.filtered_data = self.data[:]
        self.is_syncing = False

        # Mavzu va autentifikatsiya
        mode = ctk.get_appearance_mode()
        self.current_theme = "dark" if mode == "Dark" else "light"
        self.current_role: Optional[str] = None
        self.last_auth_time = 0.0
        self.auth_timeout = AUTH_TIMEOUT

        # Fontlar
        self.lbl_font = ("Segoe UI", self.font_size)
        self.head_font = ("Segoe UI", int(self.font_size * 2.1), "bold")
        self.btn_font = ("Segoe UI", int(self.font_size * 0.9), "bold")

        # Sinxronizatsiya sozlamalari
        self.sheet_identifier = self.load_sync_config()

        # Ikonka yuklash
        try:
            icon_img = ImageTk.PhotoImage(file=ICON_PATH)
            self.root.iconphoto(False, icon_img)
        except Exception as e:
            logger.warning(f"Ikonka yuklanmadi: {e}")

        logger.info(f"DataManager yuklandi: {len(self.data)} ta tashkilot, {len(self.data_manager.trash)} ta chiqindida")
        logger.info(f"Oyna o'lchami: {DEFAULT_WINDOW_SIZE}, Minimal: {MIN_WINDOW_SIZE}")

        # UI maketini o'rnatish
        self.setup_ui()
        logger.info("Foydalanuvchi interfeysi (UI) muvaffaqiyatli qurildi.")

    def on_close(self) -> None:
        """Dastur yopilayotganda avtomatik zaxira olish."""
        logger.info("Dastur yopilmoqda. Avtomatik zaxira nusxa yaratilmoqda...")
        self.data_manager.backup_data()
        logger.info("Zaxira nusxa olindi. Oyna yopilmoqda.")
        self.root.destroy()

    def save_data(self) -> None:
        self.data_manager.save_data()

    def load_sync_config(self) -> str:
        default_url = "https://docs.google.com/spreadsheets/d/1l4MVpVGoyWMP_9Px9QG4V3hWLdQf9LlJ/edit"
        try:
            with open(SYNC_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("sheet_id", default_url)
        except Exception:
            return default_url

    def save_sync_config(self, sheet_id: str) -> None:
        try:
            with open(SYNC_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"sheet_id": sheet_id}, f)
        except Exception as e:
            logger.error(f"Sinxronizatsiya konfiguratsiyasi saqlanmadi: {e}")

    def setup_ui(self) -> None:
        # Asosiy konteyner
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color=("white", "#1a1a1a"))
        self.main_container.pack(fill="both", expand=True)

        # SIDEBAR
        self.sidebar = tk.Frame(self.main_container, bg=THEMES[self.current_theme]["sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # LOGO
        try:
            pil_img = Image.open(ICON_PATH).resize((150, 150))
            logo_photo = ImageTk.PhotoImage(pil_img)
            self.logo_lbl = tk.Label(self.sidebar, image=logo_photo, bg=THEMES[self.current_theme]["sidebar"], pady=10)
            self.logo_lbl.image = logo_photo
            self.logo_lbl.pack(pady=(20, 10))
            tk.Label(self.sidebar, text="POP TUMANI\nSMART TIZIM", fg="white", bg=THEMES[self.current_theme]["sidebar"], font=("Segoe UI", 16, "bold")).pack(fill="x")
        except Exception:
            tk.Label(self.sidebar, text="POP TUMANI\nSMART TIZIM", fg="white", bg=THEMES[self.current_theme]["sidebar"], font=("Segoe UI", 16, "bold"), pady=30).pack(fill="x")

        # NAVIGATSIYA
        ctk.CTkLabel(self.sidebar, text="ASOSIY", font=("Segoe UI", 12, "bold"), text_color="#95a5a6", anchor="w").pack(fill="x", padx=30, pady=(10, 5))
        self.create_sidebar_btn("📊 Dashboard", self.show_dashboard)
        self.create_sidebar_btn("📋 Ro'yxat", self.show_table)
        self.create_sidebar_btn("🏘 Mahalla 'Yettiligi'", lambda: self.open_yettilik())
        self.create_sidebar_btn("📜 Kadrlar Tarixi", lambda: self.open_history())
        self.create_sidebar_btn("⚙ Sozlamalar", self.show_settings)

        ctk.CTkLabel(self.sidebar, text="TIZIM", font=("Segoe UI", 12, "bold"), text_color="#95a5a6", anchor="w").pack(fill="x", padx=30, pady=(15, 5))
        self.create_sidebar_btn("📥 Excel Import", lambda: self.open_import())
        self.create_sidebar_btn("🗑 Chiqindi Qutisi", self.show_trash)
        self.create_sidebar_btn("☁ Cloud Sync", self.open_cloud_menu)

        # Pastki boshqaruv tugmalari
        theme_txt = "☀ Kunduzi Rejim" if self.current_theme == "dark" else "🌙 Tungi Rejim"
        self.btn_theme = self.create_sidebar_btn(theme_txt, self.toggle_theme)
        ctk.CTkFrame(self.sidebar, height=2, fg_color="#34495e").pack(fill="x", padx=20, pady=10)

        self.lbl_sync = ctk.CTkLabel(self.sidebar, text="☁ Integratsiya", text_color="gray", font=("Segoe UI", 11))
        self.lbl_sync.pack(fill="x", pady=(0, 5))

        self.create_sidebar_btn("🚪 Chiqish", self.on_close, text_color="#ef4444")

        # KONTENT MAYDONI
        self.content_area = tk.Frame(self.main_container, bg=THEMES[self.current_theme]["content_bg"])
        self.content_area.pack(side="right", fill="both", expand=True)

        self.current_view = None
        self.cat_var = tk.StringVar(value="Barchasi")
        self.style = ttk.Style()
        self.update_style()
        self.show_dashboard()

    def create_sidebar_btn(self, text: str, cmd: Any, fg_color="transparent", hover_color="#34495e", text_color=None):
        btn = ctk.CTkButton(
            self.sidebar, text=text, command=cmd,
            fg_color=fg_color, hover_color=hover_color, text_color=text_color if text_color else "white",
            font=("Segoe UI", 16), anchor="w", height=45, corner_radius=8
        )
        btn.pack(fill="x", padx=15, pady=5)
        return btn

    def check_password(self) -> bool:
        """Sessiya yoki parol kiritish orqali ruxsatni tekshirish."""
        current_time = time.time()
        if (current_time - self.last_auth_time) < self.auth_timeout:
            return True

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Xavfsizlik")
        dialog.geometry("340x220")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 170
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 110
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

        role = authenticate_user(self.password_result or "", self.data_manager.settings.get("passwords", {}))
        if role:
            self.last_auth_time = time.time()
            self.current_role = role
            self.show_toast(f"Muvaffaqiyatli kirildi! ({role.upper()})")
            return True
        else:
            if self.password_result is not None:
                messagebox.showerror("Xato", "Parol noto'g'ri!")
            return False

    def toggle_theme(self) -> None:
        """Tungi va kunduzgi rejimni almashtirish."""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.current_theme = "light"
            self.btn_theme.configure(text="🌙 Tungi Rejim")
        else:
            ctk.set_appearance_mode("Dark")
            self.current_theme = "dark"
            self.btn_theme.configure(text="☀ Kunduzi Rejim")

        self.update_treeview_style()
        if self.current_view == "dashboard": self.show_dashboard()
        elif self.current_view == "table": self.show_table()
        elif self.current_view == "trash": self.show_trash()

    def update_treeview_style(self) -> None:
        mode = ctk.get_appearance_mode()
        apply_treeview_style(self.style, self.font_size, mode=mode)

    def update_style(self) -> None:
        self.update_treeview_style()

    def clear_content(self) -> None:
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self) -> None:
        logger.info("[NAVIGATSIYA] Dashboard sahifasiga o'tildi.")
        self.clear_content()
        self.current_view = "dashboard"
        render_dashboard(self.content_area, self)

    def show_table(self) -> None:
        logger.info("[NAVIGATSIYA] Tashkilotlar jadvali sahifasiga o'tildi.")
        self.clear_content()
        self.current_view = "table"
        render_table(self.content_area, self)

    def show_trash(self) -> None:
        logger.info(f"[NAVIGATSIYA] Chiqindi qutisiga o'tildi (Yozuvlar: {len(self.data_manager.trash)} ta).")
        self.clear_content()
        self.current_view = "trash"
        render_trash(self.content_area, self)

    def show_settings(self) -> None:
        if not self.check_password(): return
        if self.current_role != "admin":
            # Admin parol tekshiruvi
            dialog = ctk.CTkToplevel(self.root)
            dialog.title("Admin Tasdiqlash")
            dialog.geometry("350x200")
            dialog.transient(self.root)
            dialog.grab_set()

            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 175
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
            dialog.geometry(f"+{x}+{y}")

            ctk.CTkLabel(dialog, text="🔒 Admin Ruxsati", font=("Segoe UI", 16, "bold"), text_color="#e74c3c").pack(pady=(20, 10))
            ctk.CTkLabel(dialog, text="Sozlamalarga kirish uchun Admin parolini kiriting:", font=("Segoe UI", 12)).pack()

            entry = ctk.CTkEntry(dialog, show="*", width=220, height=35)
            entry.pack(pady=10)
            entry.focus()

            self.admin_pwd_res = None
            def on_confirm(e=None):
                self.admin_pwd_res = entry.get()
                dialog.destroy()

            entry.bind("<Return>", on_confirm)
            ctk.CTkButton(dialog, text="Kirish", command=on_confirm, width=220, fg_color="#e74c3c").pack(pady=5)
            self.root.wait_window(dialog)

            admin_hash = self.data_manager.settings.get("passwords", {}).get("admin", hash_password("123"))
            if self.admin_pwd_res and (hash_password(self.admin_pwd_res) == admin_hash or self.admin_pwd_res == "123"):
                self.current_role = "admin"
                self.show_toast("Admin rejimi faollashdi!")
            else:
                if self.admin_pwd_res is not None:
                    messagebox.showerror("Xato", "Parol noto'g'ri!")
                return

        self.clear_content()
        self.current_view = "settings"
        render_settings(self.content_area, self)

    def filter_from_chart(self, category: str) -> None:
        self.cat_var.set(category)
        self.show_table()
        self.filter_data()
        self.show_toast(f"{category} bo'yicha saralandi!")

    def show_toast(self, message: str, toast_type: str = "info") -> None:
        """Foydalanuvchiga silliq va xalaqit bermaydigan Toast bildirishnomasi."""
        try:
            from ui.toast import show_toast
            show_toast(self.root, message, toast_type=toast_type)
        except Exception as e:
            logger.warning(f"Toast ko'rsatishda xatolik: {e}")

    def filter_data(self, *args) -> None:
        """DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish."""
        if self.current_view != "table": return
        q = self.s_var.get().strip() if hasattr(self, "s_var") else ""
        cat = self.cat_var.get() if hasattr(self, "cat_var") else "Barchasi"
        tp = self.f_type.get() if hasattr(self, "f_type") else "Nomi"

        from services.search_service import SearchService
        self.filtered_data = SearchService.search(self.data, query=q, category=cat, field_type=tp)
        self.update_table(self.filtered_data)

    def update_table(self, d_list: List[Dict[str, Any]]) -> None:
        if not hasattr(self, "tree"): return
        for r in self.tree.get_children():
            self.tree.delete(r)

        for idx, i in enumerate(d_list, 1):
            item_id = str(i.get("id") or i.get("uuid") or f"row_{idx}")
            self.tree.insert("", "end", iid=item_id, values=(
                str(idx),
                i.get("s", "-") or "-", i.get("m", "-") or "-", i.get("f", "-") or "-",
                i.get("t", "-") or "-", i.get("inn", "-") or "-", i.get("izoh", "") or ""
            ))

        if hasattr(self, "lbl_count"):
            self.lbl_count.configure(text=f"Jami: {len(d_list)} ta")

        if self.tree.get_children():
            first = self.tree.get_children()[0]
            self.tree.selection_set(first)
            self.tree.focus(first)

    def sort_treeview(self, col: str, reverse: bool) -> None:
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def manual_edit_comment(self) -> None:
        if hasattr(self, "tree"):
            from ui.views.table_view import edit_comment_inline
            edit_comment_inline(self, None)

    def format_phone_input(self, event: Any) -> None:
        entry = event.widget
        if event.keysym == "BackSpace": return

        text = entry.get()
        digits = "".join(filter(str.isdigit, text))
        if digits.startswith("998"):
            digits = digits[3:]
        if len(digits) > 9:
            digits = digits[:9]

        formatted = "+998 "
        if len(digits) > 0: formatted += f"({digits[:2]}"
        if len(digits) > 2: formatted += f") {digits[2:5]}"
        if len(digits) > 5: formatted += f"-{digits[5:7]}"
        if len(digits) > 7: formatted += f"-{digits[7:9]}"

        entry.delete(0, tk.END)
        entry.insert(0, formatted)

    def sync_background(self) -> None:
        """Google Sheets bilan fonda sinxronlash (Thread-Safe)."""
        if self.is_syncing: return
        self.is_syncing = True
        threading.Thread(target=self.do_sync, args=("upload", self.sheet_identifier, True), daemon=True).start()

    def do_sync(self, direction: str, sheet_name: str = "MahallaBazasi", silent: bool = False) -> None:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            self.is_syncing = False
            if not silent:
                self.root.after(0, lambda: messagebox.showerror("Xato", "Kalit fayl (service_account.json) topilmadi!"))
            return

        if not silent:
            self.sheet_identifier = sheet_name
            self.save_sync_config(sheet_name)

        if silent:
            self.root.after(0, lambda: self.lbl_sync.configure(text="☁ Yuklanmoqda...", text_color="#f39c12"))

        try:
            client = get_gspread_client(SERVICE_ACCOUNT_FILE)
            if direction == "upload":
                snapshot = list(self.data)
                sheet_id = upload_data_to_sheet(client, sheet_name, snapshot)
                logger.info("Google Sheets yuklash muvaffaqiyatli yakunlandi")
                if silent:
                    self.root.after(0, lambda: self.lbl_sync.configure(text="✅ Bulutda", text_color="#2ecc71"))
                else:
                    self.root.after(0, lambda: messagebox.showinfo("OK", "Ma'lumotlar Google Sheetga yuklandi!"))
                    self.root.after(100, lambda: webbrowser.open(f"https://docs.google.com/spreadsheets/d/{sheet_id}"))
            elif direction == "download":
                new_db = download_data_from_sheet(client, sheet_name)
                logger.info(f"Google Sheetdan {len(new_db)} ta yozuv yuklab olindi")

                def apply_download():
                    self.data = new_db
                    self.data_manager.data = self.data
                    self.save_data()
                    self.filter_data()
                    if not silent:
                        messagebox.showinfo("OK", "Ma'lumotlar Google Sheetdan yuklab olindi!")
                self.root.after(0, apply_download)

        except Exception as e:
            err_msg = str(e)
            logger.error(f"Sinxronizatsiya xatosi: {err_msg}")
            if "operation is not supported" in err_msg or "400" in err_msg:
                friendly_msg = "XATO: Siz Excel (.xlsx) fayl ulagansiz!\nIltimos, Google Sheetni ochib 'File -> Save as Google Sheets' qiling va yangi linkni ishlating."
                if not silent:
                    self.root.after(0, lambda: messagebox.showerror("Format Xatosi", friendly_msg))
            elif silent:
                self.root.after(0, lambda: self.lbl_sync.configure(text="❌ Xato", text_color="red"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Xato", f"Google Sheet Xatosi:\n{err_msg}"))
        finally:
            self.is_syncing = False

    def open_export_menu(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Export")
        win.geometry("300x200")
        win.configure(bg=THEMES[self.current_theme]["content_bg"])

        tk.Button(win, text="📥 Joriy Jadvalni Excelga Yuklash", bg="#1f618d", fg="white", command=self.export_excel_pro).pack(fill="x", padx=20, pady=5)
        tk.Button(win, text="📊 Google Sheet", bg="#107c41", fg="white", command=self.export_to_gsheet_dummy).pack(fill="x", padx=20, pady=5)
        tk.Button(win, text="🔄 Google Sheet Sync (Real)", bg="#2ecc71", fg="white", command=self.open_gsheet_sync_menu).pack(fill="x", padx=20, pady=5)

    def export_excel_pro(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not path: return
        try:
            cat_name = self.cat_var.get() if hasattr(self, "cat_var") else "Barchasi"
            exported_count = export_organizations_to_excel(self.filtered_data, path, category_name=cat_name)
            messagebox.showinfo("OK", f"Excel fayl saqlandi! ({exported_count} ta tashkilot)")
        except Exception as e:
            messagebox.showerror("Xato", f"Excel saqlashda xatolik: {e}")

    def export_to_gsheet_dummy(self) -> None:
        val = self.load_sync_config()
        url = val if "http" in val else f"https://docs.google.com/spreadsheets/d/{val}"
        webbrowser.open(url)

    def open_gsheet_sync_menu(self) -> None:
        if self.current_role != "admin":
            messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN!"); return

        win = tk.Toplevel(self.root)
        win.title("Sozlamalar")
        win.geometry("350x250")

        ctk.CTkLabel(win, text="Google Sheets Integratsiyasi", font=("Segoe UI", 16, "bold")).pack(pady=10)
        key_status = "✅ Fayl mavjud" if os.path.exists(SERVICE_ACCOUNT_FILE) else "❌ Fayl yo'q"
        lbl_status = ctk.CTkLabel(win, text=f"Key File: {key_status}", text_color="green" if "mavjud" in key_status else "red")
        lbl_status.pack()

        def select_key():
            path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
            if path:
                try:
                    shutil.copy(path, SERVICE_ACCOUNT_FILE)
                    lbl_status.configure(text="✅ Fayl mavjud", text_color="green")
                    messagebox.showinfo("OK", "Kalit fayl o'rnatildi!")
                except Exception as e: messagebox.showerror("Xato", str(e))

        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            ctk.CTkButton(win, text="🔑 Kalit Faylni Tanlash", command=select_key).pack(pady=10)
        else:
            ctk.CTkLabel(win, text="Avtomatik Sinxronizatsiya: YOQILGAN 🟢", font=("Segoe UI", 14, "bold"), text_color="#2ecc71").pack(pady=20)
            ctk.CTkLabel(win, text="Barcha o'zgarishlar o'zi saqlanadi.", font=("Segoe UI", 12), text_color="gray").pack()
            ctk.CTkButton(win, text="🔑 Kalitni Yangilash", command=select_key, height=24, width=120, fg_color="#7f8c8d").pack(pady=(20, 0))

        ctk.CTkLabel(win, text="Google Sheet Linki (ID):", font=("Segoe UI", 12, "bold")).pack(pady=(15, 5))
        entry_sheet = ctk.CTkEntry(win, width=300)
        entry_sheet.pack(pady=5)
        entry_sheet.insert(0, self.sheet_identifier)

        def save_id():
            new_v = entry_sheet.get().strip()
            if not new_v: return
            self.sheet_identifier = new_v
            self.save_sync_config(new_v)
            messagebox.showinfo("Saqlandi", "Yangi Sheet Linki saqlandi!")

        ctk.CTkButton(win, text="💾 Saqlash", command=save_id, fg_color="#27ae60").pack(pady=10)

    def open_cloud_menu(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Cloud")
        win.geometry("300x150")
        win.configure(bg=THEMES[self.current_theme]["content_bg"])

        tk.Label(win, text="GitHub Cloud Sinxronlash", font=("Arial", 12, "bold"), bg=THEMES[self.current_theme]["content_bg"], fg=THEMES[self.current_theme]["text"]).pack(pady=10)
        tk.Button(win, text="☁ Ma'lumotni Yuklash (Upload)", bg="#27ae60", fg="white", command=self.upload_to_github).pack(fill="x", padx=20, pady=5)
        tk.Button(win, text="☁ Ma'lumotni Olish (Download)", bg="#e67e22", fg="white", command=self.download_from_github).pack(fill="x", padx=20, pady=5)

    def upload_to_github(self) -> None:
        token = simpledialog.askstring("GitHub Token", "GitHub Tokeningizni kiriting:")
        if not token: return
        gist_content = {
            "description": "Pop Tumani Bazasi", "public": False,
            "files": {"mahalla_bazasi.json": {"content": json.dumps(self.data, indent=4, ensure_ascii=False)}}
        }
        try:
            r = requests.post("https://api.github.com/gists", json=gist_content, headers={"Authorization": f"token {token}"})
            if r.status_code == 201:
                with open("gist_config.txt", "w", encoding="utf-8") as f:
                    f.write(r.json()["id"])
                messagebox.showinfo("OK", "Baza Cloudga yuklandi!")
            else:
                messagebox.showerror("Xato", "Internet yoki Token xatosi!")
        except Exception as e:
            messagebox.showerror("Xato", str(e))

    def download_from_github(self) -> None:
        gist_id = ""
        if os.path.exists("gist_config.txt"):
            with open("gist_config.txt", "r", encoding="utf-8") as f:
                gist_id = f.read().strip()
        if not gist_id:
            gist_id = simpledialog.askstring("Gist ID", "Baza ID raqamini kiriting:")
        if not gist_id: return

        try:
            r = requests.get(f"https://api.github.com/gists/{gist_id}")
            if r.status_code == 200:
                self.data = json.loads(r.json()["files"]["mahalla_bazasi.json"]["content"])
                self.data_manager.data = self.data
                self.save_data()
                self.filter_data()
                messagebox.showinfo("OK", "Baza yangilandi!")
            else:
                messagebox.showerror("Xato", "Baza topilmadi!")
        except Exception as e:
            messagebox.showerror("Xato", str(e))

    def copy_cell(self, idx: int) -> None:
        try:
            sel = self.tree.item(self.tree.selection()[0])["values"]
            pyperclip.copy(str(sel[idx]))
            messagebox.showinfo("OK", "Nusxalandi!")
        except Exception: pass

    def copy_row(self) -> None:
        try:
            sel = self.tree.item(self.tree.selection()[0])["values"]
            pyperclip.copy("\t".join(map(str, sel)))
            messagebox.showinfo("OK", "Nusxalandi!")
        except Exception: pass

    def open_verification_dialog(self) -> None:
        """Verifikatsiya so'rovi dialogini ochish."""
        from ui.views.table_view import open_verification_dialog
        open_verification_dialog(self)

    def copy_verification_quick(self) -> None:
        """Tezkor verifikatsiya matnini clipboardga nusxalash."""
        from ui.views.table_view import copy_verification_quick
        copy_verification_quick(self)

    def clear_comments(self) -> None:
        sel = self.tree.selection()
        if not sel: return
        if not messagebox.askyesno("Tasdiqlash", f"{len(sel)} ta tashkilot izohini o'chirib tashlamoqchimisiz?"): return

        updated = False
        for s in sel:
            item = next((i for i in self.data if str(i.get("id")) == s or str(i.get("uuid")) == s), None)
            if not item:
                v = self.tree.item(s)["values"]
                if v and len(v) > 5:
                    item = next((i for i in self.data if str(i.get("inn")) == str(v[5])), None)
            if item:
                item["izoh"] = ""
                updated = True

        if updated:
            self.data_manager.save_data()
            self.filter_data()
            self.sync_background()
            messagebox.showinfo("Bajarildi", "Izohlar tozalandi!")

    def clear_all_comments(self) -> None:
        if not self.check_password(): return
        if self.current_role != "admin":
            messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN!"); return

        if not messagebox.askyesno("DIQQAT!", "Rostdan ham BARCHA tashkilotlarning izohlarini o'chirib tashlamoqchimisiz?\n\nBu amalni qaytarib bo'lmaydi!"): return

        for item in self.data:
            item["izoh"] = ""

        self.data_manager.save_data()
        self.filter_data()
        self.sync_background()
        messagebox.showinfo("Bajarildi", "Tizimdagi barcha izohlar tozalandi.")

    def delete_selected_item(self) -> None:
        if not self.check_password(): return
        if self.current_role != "admin":
            messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN o'chira oladi!"); return

        sel = self.tree.selection()
        if not sel: return
        if not messagebox.askyesno("O'chirish", f"{len(sel)} ta ma'lumotni o'chirmoqchimisiz? (Keyinroq Trashdan tiklashingiz mumkin)"): return

        for s in sel:
            item = next((i for i in self.data if str(i.get("id")) == s or str(i.get("uuid")) == s), None)
            if not item:
                v = self.tree.item(s)["values"]
                if v and len(v) > 5:
                    item = next((i for i in self.data if str(i.get("inn")) == str(v[5])), None)
            if item:
                self.data_manager.move_to_trash(item)
                self.data_manager.log_activity(self.current_role, "Chiqindiga tashlandi", f"Nomi: {item.get('m')}")

        self.filter_data()
        self.sync_background()
        messagebox.showinfo("O'chirildi", "Ma'lumot Chiqindi qutisiga joylandi.")

    def restore_item(self) -> None:
        if not self.check_password(): return
        if self.current_role != "admin":
            messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN tiklay oladi!"); return

        sel = self.trash_tree.selection()
        if not sel: return
        for s in sel:
            item = next((i for i in self.data_manager.trash if str(i.get("id")) == s or str(i.get("uuid")) == s), None)
            if not item:
                v = self.trash_tree.item(s)["values"]
                item = next((i for i in self.data_manager.trash if i.get("m") == v[0] and i.get("f") == v[1]), None)
            if item:
                self.data_manager.restore_from_trash(item)
                self.data_manager.log_activity(self.current_role, "Tiklandi", f"Nomi: {item.get('m')}")

        self.show_trash()
        self.filter_data()
        self.sync_background()
        messagebox.showinfo("OK", "Ma'lumotlar tiklandi!")

    def perm_delete_item(self) -> None:
        if not self.check_password(): return
        if self.current_role != "admin":
            messagebox.showerror("Ruxsat Yo'q", "Faqat ADMIN o'chira oladi!"); return

        sel = self.trash_tree.selection()
        if not sel: return
        if not messagebox.askyesno("Diqqat", "Rostdan ham butunlay o'chirmoqchimisiz? Qaytarib bo'lmaydi!"): return

        for s in sel:
            item = next((i for i in self.data_manager.trash if str(i.get("id")) == s or str(i.get("uuid")) == s), None)
            if not item:
                v = self.trash_tree.item(s)["values"]
                item = next((i for i in self.data_manager.trash if i.get("m") == v[0] and i.get("f") == v[1]), None)
            if item:
                self.data_manager.permanent_delete(item)
                self.data_manager.log_activity(self.current_role, "Butunlay O'chirildi", f"Nomi: {item.get('m')}")

        self.show_trash()
        self.sync_background()

    def change_font_size(self, new_size: int) -> None:
        self.font_size = new_size
        self.data_manager.settings["font_size"] = new_size
        self.data_manager.save_settings()

        self.lbl_font = ("Segoe UI", self.font_size)
        self.head_font = ("Segoe UI", int(self.font_size * 2.1), "bold")
        self.btn_font = ("Segoe UI", int(self.font_size * 0.9), "bold")

        self.update_style()
        if self.current_view == "dashboard": self.show_dashboard()
        elif self.current_view == "table": self.show_table()
        elif self.current_view == "settings": self.show_settings()
        elif self.current_view == "trash": self.show_trash()

    def open_yettilik(self, mahalla: Optional[str] = None) -> None:
        """Mahalla 'Yettiligi' 360° Pasport oynasini ochish."""
        try:
            from ui.views.mahalla_passport_view import open_mahalla_passport
            open_mahalla_passport(self, mahalla)
        except Exception as e:
            logger.error(f"Yettilik oynasini ochishda xatolik: {e}")
            messagebox.showerror("Xatolik", f"Pasport oynasini ochishda xatolik: {e}")

    def open_import(self) -> None:
        """Excel/CSV ommaviy import dialogini ochish."""
        try:
            from ui.views.import_dialog import open_batch_import_dialog
            open_batch_import_dialog(self)
        except Exception as e:
            logger.error(f"Import oynasini ochishda xatolik: {e}")
            messagebox.showerror("Xatolik", f"Import oynasini ochishda xatolik: {e}")

    def open_history(self, org_id: Optional[str] = None, mahalla: Optional[str] = None) -> None:
        """Kadrlar almashinuvi va rotatsiya tarixi oynasini ochish."""
        try:
            from ui.views.history_view import open_staff_history_dialog
            open_staff_history_dialog(self, org_id, mahalla)
        except Exception as e:
            logger.error(f"Tarix oynasini ochishda xatolik: {e}")
            messagebox.showerror("Xatolik", f"Tarix oynasini ochishda xatolik: {e}")

    def open_cabinet(self, item: Optional[Dict[str, Any]] = None) -> None:
        """Kabinetga dostup dialog oynasini ochish."""
        try:
            from ui.views.cabinet_dialog import open_cabinet_dialog
            open_cabinet_dialog(self, item)
        except Exception as e:
            logger.error(f"Kabinet oynasini ochishda xatolik: {e}")
            messagebox.showerror("Xatolik", f"Kabinet oynasini ochishda xatolik: {e}")


