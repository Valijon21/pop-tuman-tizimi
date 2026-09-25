"""
Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise)
Asosiy ishga tushirish fayli - PyQt5 Zamonaviy Interfeysi (Senior Edition)
"""
import sys
import os
import platform

# Loyiha papkasini yo'lga qo'shish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core.logger import logger, install_global_exception_handler
from ui_qt.app_window import run_qt_app

def main() -> int:
    """Asosiy ilovani ishga tushirish (Entry Point)."""
    # 1. Global xatoliklarni tutuvchini o'rnatish
    install_global_exception_handler()

    # Windows taskbar uchun ilova identifikatorini o'rnatish
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("poptuman.tashkilot.inn.v4")
        except Exception:
            pass

    # 2. Tizim va dastur ma'lumotlarini loglash
    is_frozen = getattr(sys, "frozen", False)
    logger.info("=" * 60)
    logger.info("🚀 POP TUMAN TASHKILOTLARI VA INN TIZIMI (PyQt5 Modern Fluent UI)")
    logger.info(f"📍 Ishchi katalog: {os.path.abspath(os.getcwd())}")
    logger.info(f"💻 Operatsion tizim: {platform.system()} {platform.release()} ({platform.version()})")
    logger.info(f"🐍 Python: {sys.version.split()[0]} | Frozen (EXE): {is_frozen}")
    logger.info("=" * 60)

    # 3. PyQt5 asosiy interfeysini ishga tushirish
    return run_qt_app()

if __name__ == "__main__":
    sys.exit(main())
