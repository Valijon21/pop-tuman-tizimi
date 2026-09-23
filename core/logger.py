"""
Pop Tuman Tashkilotlari va INN Tizimi
Professional Aylanuvchi Log Tizimi va Global Xatoliklarni Tutuvchi Mexanizm
"""
import os
import sys
import logging
import threading
import traceback
from logging.handlers import RotatingFileHandler
from core.config import BASE_DIR, LOG_FILE

LOGGER_NAME = "PopTumanApp"

def setup_logger(log_filename: str = "app.log") -> logging.Logger:
    """Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)."""
    log_path = os.path.join(BASE_DIR, log_filename)
    app_logger = logging.getLogger(LOGGER_NAME)
    app_logger.setLevel(logging.DEBUG)

    if not app_logger.handlers:
        # 1. Faylga yozuvchi aylanma handler
        rfh = RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024, # 5MB
            backupCount=5,
            encoding="utf-8"
        )
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-8s] [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        rfh.setFormatter(formatter)
        rfh.setLevel(logging.DEBUG)
        app_logger.addHandler(rfh)

        # 2. Konsolga chiqaruvchi handler (agar konsol mavjud bo'lsa)
        try:
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)
            sh.setLevel(logging.INFO)
            app_logger.addHandler(sh)
        except Exception:
            pass

    return app_logger

logger = setup_logger()

def install_global_exception_handler():
    """Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozish."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        err_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.critical(f"Kutilmagan xatolik (Unhandled Exception):\n{err_msg}")

        # Agar GUI yuklangan bo'lsa, xatolik dialogini ko'rsatish
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk._default_root
            if root and root.winfo_exists():
                messagebox.showerror(
                    "Kutilmagan Xatolik",
                    f"Dasturda xatolik yuz berdi:\n{exc_value}\n\nTo'liq tafsilotlar app.log fayliga yozildi."
                )
        except Exception:
            pass

    sys.excepthook = handle_exception

    # Oqimlar (Threads) ichidagi xatoliklarni tutish
    def handle_thread_exception(args):
        err_msg = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
        logger.critical(f"Oqim ichida xatolik (Thread Exception in {args.thread.name}):\n{err_msg}")

    if hasattr(threading, "excepthook"):
        threading.excepthook = handle_thread_exception
