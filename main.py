"""
Pop Tuman Tashkilotlari va INN Tizimi (PRO)
Asosiy ishga tushirish nuqtasi (Entry Point)
"""
import customtkinter as ctk
from ui.app import MahallaDasturi

def main():
    root = ctk.CTk()
    app = MahallaDasturi(root)
    root.mainloop()

if __name__ == "__main__":
    main()
