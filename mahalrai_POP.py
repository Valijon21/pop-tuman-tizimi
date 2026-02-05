
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
from openpyxl.styles import Font
from PIL import ImageTk, Image

# Fayl sozlamalari
DB_FILE = "mahalla_bazasi.json"

class MahallaDasturi:
    def __init__(self, root):
        self.root = root
        self.root.title("Pop Tumani Smart Boshqaruv Tizimi (PRO)")
        self.root.geometry("1350x800")
        self.root.configure(bg="#f4f7f6")
        self.font_size = 11
        self.data = self.load_data()
        self.filtered_data = self.data[:]
        self.setup_ui()

    def load_data(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def setup_ui(self):
        # HEADER
        header = tk.Frame(self.root, bg="#2c3e50", height=70)
        header.pack(fill="x")
        tk.Label(header, text="TASHKILOTLAR PRO TIZIMI", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=20)
        
        # CLOUD TUGMALARI
        cloud_frame = tk.Frame(header, bg="#2c3e50")
        cloud_frame.pack(side="right", padx=20)
        tk.Button(cloud_frame, text="☁ Yuklash", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=self.upload_to_github).pack(side="left", padx=5)
        tk.Button(cloud_frame, text="☁ Olish", bg="#e67e22", fg="white", font=("Arial", 9, "bold"), command=self.download_from_github).pack(side="left", padx=5)

        # SHRIFT
        font_frame = tk.Frame(header, bg="#2c3e50")
        font_frame.pack(side="right", padx=10)
        tk.Button(font_frame, text="A+", command=lambda: self.change_font(2)).pack(side="left", padx=2)
        tk.Button(font_frame, text="A-", command=lambda: self.change_font(-2)).pack(side="left", padx=2)

        # KATEGORIYALAR
        cat_frame = tk.Frame(self.root, bg="#f4f7f6", pady=5)
        cat_frame.pack(fill="x", padx=20)
        self.cat_var = tk.StringVar(value="Barchasi")
        for cat in ["Barchasi", "Mahallalar", "Maktablar", "Bog'chalar"]:
            tk.Radiobutton(cat_frame, text=cat, variable=self.cat_var, value=cat, indicatoron=0, 
                           width=15, command=self.filter_data, bg="#d1d8e0", selectcolor="#3498db", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        # QIDIRUV VA TUGMALAR
        ctrl = tk.Frame(self.root, bg="#f4f7f6", pady=10)
        ctrl.pack(fill="x", padx=20)
        
        self.f_type = ttk.Combobox(ctrl, values=["Nomi", "F.I.SH", "INN", "Izoh"], state="readonly", width=10, font=("Arial", 11))
        self.f_type.current(0); self.f_type.pack(side="left", padx=5)
        
        self.s_var = tk.StringVar(); self.s_var.trace("w", self.filter_data)
        tk.Entry(ctrl, textvariable=self.s_var, width=20, font=("Arial", 13)).pack(side="left", padx=5)
        tk.Button(ctrl, text="✖", command=lambda: self.s_var.set("")).pack(side="left")

        # ASOSIY TUGMALAR
        tk.Button(ctrl, font=("Arial", 10,"bold"), text="📊 G-Sheet", bg="#107c41", fg="white", command=self.export_to_gsheet_dummy).pack(side="right", padx=5)
        tk.Button(ctrl, font=("Arial", 10,"bold"), text="📥 Excel", bg="#1f618d", fg="white", command=self.export_excel_pro).pack(side="right", padx=5)
        tk.Button(ctrl, font=("Arial", 10,"bold"), text="✈ Telegram", bg="#0088cc", fg="white", command=self.send_telegram).pack(side="right", padx=5)
        tk.Button(ctrl, font=("Arial", 10,"bold"), text="📱 QR", bg="#e67e22", fg="white", command=self.show_qr).pack(side="right", padx=5)
        tk.Button(ctrl, font=("Arial", 10,"bold"), text="✎ Tahrir", bg="#f39c12", fg="white", command=self.edit_item).pack(side="right", padx=5)
        tk.Button(ctrl, font=("Arial", 10,"bold"), text="+ Qo'shish", bg="#27ae60", fg="white", command=self.add_item).pack(side="right", padx=5)

        # JADVAL
        self.style = ttk.Style(); self.update_style()
        self.tree = ttk.Treeview(self.root, columns=("s","m","f","t","inn","izoh"), show="headings")
        
        headers = [("s","Turi", 80), ("m","Tashkilot Nomi", 300), ("f","F.I.SH", 200), 
                   ("t","Tel", 100), ("inn","INN", 100), ("izoh","Izoh", 150)]
        
        for col, name, width in headers:
            self.tree.heading(col, text=name)
            self.tree.column(col, width=width, anchor="center" if col != "m" else "w")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # O'NG TUGMA MENYUSI
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="📞 Tel nusxalash", command=lambda: self.copy_cell(3))
        self.context_menu.add_command(label="🆔 INN nusxalash", command=lambda: self.copy_cell(4))
        self.context_menu.add_command(label="📝 Izohni nusxalash", command=lambda: self.copy_cell(5))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Qatorni nusxalash", command=self.copy_row)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.update_table(self.data)

    def filter_data(self, *args):
        q, cat, tp = self.s_var.get().lower(), self.cat_var.get(), self.f_type.get()
        res = []
        for i in self.data:
            n = str(i.get("m", "")).lower()
            match_cat = (cat=="Barchasi") or (cat=="Mahallalar" and "mfy" in n) or \
                        (cat=="Maktablar" and "maktab" in n) or (cat=="Bog'chalar" and "mtt" in n)
            if match_cat:
                target = ""
                if tp == "Nomi": target = n
                elif tp == "F.I.SH": target = str(i.get("f","")).lower()
                elif tp == "INN": target = str(i.get("inn",""))
                elif tp == "Izoh": target = str(i.get("izoh","")).lower()
                
                if q in target: res.append(i)
        self.filtered_data = res
        self.update_table(res)

    def update_table(self, d_list):
        for r in self.tree.get_children(): self.tree.delete(r)
        for i in d_list:
            self.tree.insert("", "end", values=(
                i.get("s","-"), i.get("m","-"), i.get("f","-"), 
                i.get("t","-"), i.get("inn","-"), i.get("izoh", "")
            ))

    # --- PRO FUNKSIYALAR ---

    def export_excel_pro(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not path: return
        
        try:
            wb = openpyxl.Workbook()
            ws = wb.active; ws.title = "Tashkilotlar"
            ws.append(["Turi", "Nomi", "Rahbar", "Tel", "INN", "Izoh"])
            
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = openpyxl.styles.PatternFill(start_color="2c3e50", end_color="2c3e50", fill_type="solid")

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

            wb.save(path); messagebox.showinfo("OK", "Excel fayl saqlandi!")
        except Exception as e: messagebox.showerror("Xato", str(e))

    def upload_to_github(self):
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
        sel = self.tree.focus()
        if sel:
            v = self.tree.item(sel)["values"]
            item = next((i for i in self.data if i.get("inn") == str(v[4])), None)
            if item: self.open_win("Tahrirlash", item)

    def add_item(self): self.open_win("Yangi qo'shish")

    def open_win(self, title, item=None):
        win = tk.Toplevel(self.root); win.title(title); win.geometry("400x500"); win.grab_set()
        flds = [("Turi","s"),("Nomi","m"),("Rahbar","f"),("Tel","t"),("INN","inn"), ("Izoh","izoh")]
        ents = {}
        for l, k in flds:
            tk.Label(win, text=l, font=("Arial", 10, "bold")).pack(pady=(5,0))
            e = tk.Entry(win, width=35, font=("Arial", 11)); e.pack(pady=2); ents[k] = e
            if item: e.insert(0, item.get(k, ""))
        
        def save():
            d = {k: ents[k].get() for _, k in flds}
            if item: self.data[self.data.index(item)] = d
            else: self.data.append(d)
            self.save_data(); self.filter_data(); win.destroy()
        tk.Button(win, text="SAQLASH", bg="#2c3e50", fg="white", font=("Arial", 12, "bold"), command=save).pack(pady=20)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item: self.tree.selection_set(item); self.context_menu.post(event.x_root, event.y_root)

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
            v = self.tree.item(self.tree.focus())["values"]
            qr = qrcode.make(f"BEGIN:VCARD\nFN:{v[2]}\nTEL:{v[3]}\nNOTE:{v[5]}\nEND:VCARD")
            qr.save("t.png"); w = tk.Toplevel(self.root); i = ImageTk.PhotoImage(Image.open("t.png")); l = tk.Label(w, image=i); l.image=i; l.pack()
        except: pass

    def change_font(self, delta): self.font_size += delta; self.update_style()
    def update_style(self):
        self.style.configure("Treeview", font=("Arial", self.font_size), rowheight=self.font_size*3)
        self.style.configure("Treeview.Heading", font=("Arial", self.font_size, "bold"))

if __name__ == "__main__":
    root = tk.Tk(); app = MahallaDasturi(root); root.mainloop()