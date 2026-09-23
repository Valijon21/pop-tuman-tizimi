"""
Pop Tuman Tashkilotlari va INN Tizimi (PRO)
Windows Standalone .EXE Yaratish Skripti (PyInstaller Packaging Builder)
"""
import os
import sys
import subprocess
import shutil

# Windows konsolida UTF-8 ni to'g'ri ishlashini ta'minlash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def build():
    print("=" * 60)
    print("📦 POP TUMAN TIZIMI: WINDOWS STANDALONE .EXE YIG'ISH BOSHLANDI")
    print("=" * 60)

    # 1. CustomTkinter papkasini aniqlash
    try:
        import customtkinter
        ctk_dir = os.path.dirname(customtkinter.__file__)
        print(f"[OK] CustomTkinter topildi: {ctk_dir}")
    except ImportError:
        print("[XATO] customtkinter kutubxonasi o'rnatilmagan! (pip install -r requirements.txt)")
        sys.exit(1)

    # 2. PyInstaller mavjudligini tekshirish
    try:
        import PyInstaller
        print(f"[OK] PyInstaller versiyasi: {PyInstaller.__version__}")
    except ImportError:
        print("[OGOHLANTIRISH] PyInstaller o'rnatilmagan! O'rnatilmoqda...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 3. Yig'ish parametrlari
    app_name = "PopTumanTizimi"
    main_script = os.path.join(BASE_DIR, "main.py")
    icon_file = os.path.join(BASE_DIR, "popdata.png")

    # Eski kesh va yig'ilgan fayllarni tozalash (Clean build)
    build_dir = os.path.join(BASE_DIR, "build")
    dist_dir = os.path.join(BASE_DIR, "dist", app_name)
    print("[TOZALASH] Eski kesh va build papkalari tozalanmoqda...")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir, ignore_errors=True)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir, ignore_errors=True)

    # Buyruq argumentlari
    args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",                # Tez ishga tushishi va barqarorlik uchun papka ko'rinishida
        "--windowed",              # Orqada qora terminal oynasi ochilmaydi
        f"--name={app_name}",
        f"--add-data={ctk_dir};customtkinter",
    ]

    if os.path.exists(icon_file):
        args.append(f"--add-data={icon_file};.")

    # Yashirin kutubxonalar (Hidden imports)
    hidden_imports = [
        "PIL._tkinter_finder",
        "gspread",
        "oauth2client",
        "oauth2client.service_account",
        "openpyxl",
        "qrcode",
        "sqlite3",
        "core",
        "core.config",
        "core.logger",
        "core.security",
        "core.validators",
        "database",
        "database.models",
        "database.data_manager",
        "database.sqlite_manager",
        "services",
        "services.qr_service",
        "services.excel_service",
        "services.gsheet_service",
        "services.search_service",
        "services.verification_service",
        "services.telegram_bot",
        "ui",
        "ui.style",
        "ui.toast",
        "ui.app",
        "ui.views",
        "ui.views.dashboard_view",
        "ui.views.table_view",
        "ui.views.trash_view",
        "ui.views.settings_view",
        "ui.views.mahalla_passport_view",
        "ui.views.history_view",
        "ui.views.import_dialog"
    ]
    for h in hidden_imports:
        args.append(f"--hidden-import={h}")

    args.append(main_script)

    print("\n[ISHLAMOQDA] PyInstaller ishga tushirilmoqda...")
    print(f"Buyruq: {' '.join(args)}\n")

    result = subprocess.run(args, cwd=BASE_DIR)

    if result.returncode == 0:
        dist_dir = os.path.join(BASE_DIR, "dist", app_name)
        # Baza va sozlama fayllarini dist papkasiga nusxalash (Stand-alone to'liq ishlashi uchun)
        files_to_copy = [
            "mahalla_tizimi.db",
            "mahalla_bazasi.json",
            "categories.json",
            "settings.json",
            "popdata.png",
            "sync_config.json",
            "service_account.json"
        ]
        for fname in files_to_copy:
            src = os.path.join(BASE_DIR, fname)
            if os.path.exists(src):
                dst = os.path.join(dist_dir, fname)
                shutil.copy2(src, dst)
                print(f"[NUSXALANDI] {fname} -> dist/{app_name}/")

        print("\n" + "=" * 60)
        print(f"✅ MUVAFFAQIYATLI YIG'ILDI!")
        print(f"📁 Dastur joylashgan papka: {dist_dir}")
        print(f"🚀 Ishga tushirish fayli: {os.path.join(dist_dir, app_name + '.exe')}")
        print("=" * 60)
    else:
        print("\n[FAIL] Yig'ishda xatolik yuz berdi!")
        sys.exit(result.returncode)

if __name__ == "__main__":
    build()
