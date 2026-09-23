"""
Pop Tuman Tashkilotlari va INN Tizimi (PRO)
Asosiy ishga tushirish nuqtasi (Entry Point)
"""
import sys
import os
import platform
import customtkinter as ctk

from core.logger import logger, install_global_exception_handler
from ui.app import MahallaDasturi

def main():
    # 1. Global xatoliklarni tutuvchini o'rnatish
    install_global_exception_handler()

    # 2. Tizim va dastur ma'lumotlarini loglash
    is_frozen = getattr(sys, "frozen", False)
    logger.info("=" * 60)
    logger.info("🚀 POP TUMAN TASHKILOTLARI VA INN TIZIMI ISHGA TUSHDI")
    logger.info(f"📍 Ishchi katalog: {os.path.abspath(os.getcwd())}")
    logger.info(f"💻 Operatsion tizim: {platform.system()} {platform.release()} ({platform.version()})")
    logger.info(f"🐍 Python: {sys.version.split()[0]} | Frozen (EXE): {is_frozen}")
    logger.info("=" * 60)

    # 3. GUI Dvigatelini tanlash (PyQt5 birinchi darajali, Tkinter zaxira)
    use_tk = "--tk" in sys.argv
    if not use_tk:
        try:
            from ui_qt.app_window import run_qt_app
            logger.info("🚀 PyQt5 zamonaviy GUI dvigateli ishga tushirilmoqda...")
            sys.exit(run_qt_app())
        except ImportError as e:
            logger.warning(f"PyQt5 topilmadi ({e}), CustomTkinter rejimiga o'tilmoqda...")
        except Exception as e:
            logger.error(f"PyQt5 ishga tushirishda xatolik ({e}), CustomTkinter rejimiga o'tilmoqda...", exc_info=True)

    try:
        logger.info("[QADAM 1] Asosiy oyna (root CTk) yaratilmoqda...")
        root = ctk.CTk()

        logger.info("[QADAM 2] MahallaDasturi interfeysi va boshqaruvchilari yuklanmoqda...")
        app = MahallaDasturi(root)

        logger.info("[QADAM 3] Asosiy hodisalar sikli (mainloop) boshlandi.")
        root.mainloop()

        logger.info("🏁 Dastur muvaffaqiyatli yopildi.")
    except Exception as e:
        logger.critical(f"Boshlang'ich yuklashda jiddiy xatolik: {e}", exc_info=True)
        try:
            import tkinter.messagebox as mb
            mb.showerror("Kritik Xatolik", f"Dasturni ishga tushirishda xatolik yuz berdi:\n{e}\n\nTafsilotlar app.log fayliga yozildi.")
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
