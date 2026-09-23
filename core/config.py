import os
import sys

# Papka va fayl yo'llari (PyInstaller EXE yoki Python skriptiga moslashuvchan)
if getattr(sys, "frozen", False):
    # Standalone EXE rejimida .exe fayli joylashgan asosiy papka
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    # Python skripti rejimida loyiha ildiz papkasi
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# .env muhit faylini mustaqil o'qish (tashqi kutubxonalarsiz)
def _load_env():
    env_file = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

_load_env()

DB_FILE = os.path.join(BASE_DIR, "mahalla_bazasi.json")
SQLITE_DB_FILE = os.path.join(BASE_DIR, "mahalla_tizimi.db")
TRASH_FILE = os.path.join(BASE_DIR, "trash.json")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
LOG_FILE = os.path.join(BASE_DIR, "activity_log.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
SYNC_CONFIG_FILE = os.path.join(BASE_DIR, "sync_config.json")
CATEGORIES_FILE = os.path.join(BASE_DIR, "categories.json")
SERVICE_ACCOUNT_FILE = (
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    or os.getenv("SERVICE_ACCOUNT_FILE")
    or os.path.join(BASE_DIR, "service_account.json")
)
ICON_PATH = os.path.join(BASE_DIR, "popdata.png")

# Oyna parametrlari
APP_TITLE = "Pop Tumani Smart Boshqaruv Tizimi (PRO)"
DEFAULT_WINDOW_SIZE = "1350x800"
MIN_WINDOW_SIZE = (1050, 650)
AUTH_TIMEOUT = 20 * 60 # 20 daqiqa sessiya

# Standart kategoriyalar
DEFAULT_CATEGORIES = ["Mahalla (MFY)", "Maktab", "Bog'cha (MTT)", "Boshqa"]

# Diagramma va statistika ranglari
CHART_COLORS = ["#10b981", "#f59e0b", "#8b5cf6", "#3b82f6", "#e11d48", "#14b8a6", "#f97316", "#6366f1"]

# Mavzular palitrasi (Modern Slate & Ko'k)
THEMES = {
    "light": {
        "bg": "#f8fafc",
        "fg": "#334155",
        "content_bg": "#f1f5f9",
        "sidebar": "#1e293b",
        "sidebar_text": "#e2e8f0",
        "card_bg": "white",
        "text": "#1e293b",
        "accent": "#3b82f6"
    },
    "dark": {
        "bg": "#0f172a",
        "fg": "#e2e8f0",
        "content_bg": "#1e293b",
        "sidebar": "#020617",
        "sidebar_text": "#94a3b8",
        "card_bg": "#1e293b",
        "text": "#f8fafc",
        "accent": "#60a5fa"
    }
}
