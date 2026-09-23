"""
Pop Tuman Tashkilotlari va INN Tizimi
Eski ishga tushirish fayli bilan 100% orqaga moslik (Backward Compatibility Adapter).
"""
import sys
import os

# Loyiha asosiy papkasini sys.path ga qo'shish
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main()