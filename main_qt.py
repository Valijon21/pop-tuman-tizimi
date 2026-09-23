"""
Pop Tuman Tashkilotlari va INN Tizimi (PRO)
Asosiy ishga tushirish fayli - PyQt5 Zamonaviy Interfeysi (Senior Edition)
"""
import sys
import os

# Loyiha papkasini yo'lga qo'shish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from ui_qt.app_window import run_qt_app

if __name__ == "__main__":
    sys.exit(run_qt_app())
