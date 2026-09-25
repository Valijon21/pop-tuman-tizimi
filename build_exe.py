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

    # 1. PyQt5 mavjudligini tekshirish
    try:
        import PyQt5
        print("[OK] Asosiy GUI dvigateli: PyQt5 topildi")
    except ImportError:
        print("[OGOHLANTIRISH] PyQt5 topilmadi! (pip install PyQt5)")

    # 2. PyInstaller mavjudligini tekshirish
    try:
        import PyInstaller
        print(f"[OK] PyInstaller versiyasi: {PyInstaller.__version__}")
    except ImportError:
        print("[OGOHLANTIRISH] PyInstaller o'rnatilmagan! O'rnatilmoqda...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 3. Yig'ish parametrlari
    app_name = "PopTumanTizimi"
    main_script = os.path.join(BASE_DIR, "main_qt.py")
    icon_file = os.path.join(BASE_DIR, "popdata.png")
    ico_file = os.path.join(BASE_DIR, "popdata.ico")
    logo_file = os.path.join(BASE_DIR, "popdata_logo.png")

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
    ]

    if os.path.exists(ico_file):
        args.append(f"--icon={ico_file}")
    elif os.path.exists(icon_file):
        args.append(f"--icon={icon_file}")

    if os.path.exists(icon_file):
        args.append(f"--add-data={icon_file};.")
    if os.path.exists(ico_file):
        args.append(f"--add-data={ico_file};.")
    if os.path.exists(logo_file):
        args.append(f"--add-data={logo_file};.")

    # Yashirin kutubxonalar (Hidden imports)
    hidden_imports = [
        "gspread",
        "oauth2client",
        "oauth2client.service_account",
        "openpyxl",
        "xlrd",
        "qrcode",
        "sqlite3",
        "core",
        "core.config",
        "core.logger",
        "core.security",
        "core.validators",
        "core.threading_utils",
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
        "services.cabinet_service",
        "services.broadcast_service",
        "services.telegram_bot",
        "PyQt5",
        "PyQt5.QtCore",
        "PyQt5.QtWidgets",
        "PyQt5.QtGui",
        "ui_qt",
        "ui_qt.styles",
        "ui_qt.app_window",
        "ui_qt.components",
        "ui_qt.components.table_model",
        "ui_qt.components.widgets",
        "ui_qt.views",
        "ui_qt.views.dashboard_view",
        "ui_qt.views.table_view",
        "ui_qt.views.contracts_view",
        "ui_qt.views.trash_view",
        "ui_qt.views.settings_view",
        "ui_qt.views.mahalla_passport_view",
        "ui_qt.views.cabinet_dialog",
        "ui_qt.views.verification_dialog",
        "ui_qt.views.broadcast_view",
        "ui_qt.views.history_view",
        "ui_qt.views.import_dialog",
        "ui_qt.views.org_edit_dialog",
        "ui_qt.views.qr_dialog",
        "ui_qt.views.contract_add_dialog",
        "ui_qt.views.password_dialog"
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
            "popdata.ico",
            "popdata_logo.png",
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
