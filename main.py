"""
Pop Tuman Tashkilotlari va INN Tizimi (PRO)
Asosiy kirish nuqtasi (Entry Point Adapter).
Dasturni yagona zamonaviy PyQt5 interfeysi (main_qt.py) orqali ishga tushiradi.
"""
import sys
import os

# Loyiha papkasini yo'lga qo'shish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from main_qt import main

if __name__ == "__main__":
    sys.exit(main())
