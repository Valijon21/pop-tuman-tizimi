# Graph Report - tashkilotlar INN tizim  (2026-09-23)

## Corpus Check
- 72 files · ~55,729 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 761 nodes · 1458 edges · 54 communities (39 shown, 15 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e48a49b8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- UI App Core & Event Handlers
- Core Configuration & Logging
- Data Validation & Formatting
- External Services (Excel, QR, GSheets)
- Data Persistence & Backup Manager
- import_organizations_from_file
- UI Views Test Suite
- SQLiteManager
- Toast Notification System
- Application Lifecycle & Entry Points
- PyInstaller Windows Build Pipeline
- Automated Test Runner
- Core Architecture Package
- Database Package Architecture
- Services Package Architecture
- UI Package Architecture
- UI Views Package Architecture
- rules/graphify.md
- workflows/graphify.md
- hash_password
- TelegramBotService
- import_organizations_from_file
- TestImportService
- clean_inn
- sanitize_text
- MainWindow
- TableView
- TestQtArchitecture
- SettingsView
- hash_password
- MahallaPassportView
- TrashView
- CabinetDialog
- open_record_dialog
- app.py
- .test_view_imports
- VerificationDialog
- ImportDialog
- OrgEditDialog
- test_views.py
- render_settings
- components/__init__.py
- ui_qt/__init__.py
- ui_qt/views/__init__.py
- build_verification_text
- .filter_data
- DashboardView
- main.py
- .setup_ui
- .open_cabinet
- ClickableCard
- setup_logger

## God Nodes (most connected - your core abstractions)
1. `MahallaDasturi` - 56 edges
2. `MainWindow` - 36 edges
3. `TableView` - 32 edges
4. `DataManager` - 27 edges
5. `SQLiteManager` - 27 edges
6. `TestQtArchitecture` - 27 edges
7. `build_verification_text()` - 22 edges
8. `TelegramBotService` - 21 edges
9. `OrgEditDialog` - 21 edges
10. `DashboardView` - 19 edges

## Surprising Connections (you probably didn't know these)
- `MahallaDasturi` --uses--> `DataManager`  [INFERRED]
  ui/app.py → database/data_manager.py
- `MainWindow` --uses--> `DataManager`  [INFERRED]
  ui_qt/app_window.py → database/data_manager.py
- `BroadcastView` --uses--> `BroadcastService`  [INFERRED]
  ui_qt/views/broadcast_view.py → services/broadcast_service.py
- `MahallaDasturi` --uses--> `SearchService`  [INFERRED]
  ui/app.py → services/search_service.py
- `TableView` --uses--> `SearchService`  [INFERRED]
  ui_qt/views/table_view.py → services/search_service.py

## Import Cycles
- None detected.

## Communities (54 total, 15 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.11
Nodes (6): MahallaDasturi, CTk, Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)., Verifikatsiya so'rovi dialogini ochish., Tezkor verifikatsiya matnini clipboardga nusxalash., Dastur yopilayotganda avtomatik zaxira olish.

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.16
Nodes (14): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+6 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.13
Nodes (16): clean_inn(), clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish. (+8 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.10
Nodes (14): export_organizations_to_excel(), Any, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., normalize_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati. (+6 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.10
Nodes (15): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Tizimdagi harakatlarni qayd etish (JSON + SQLite)., Xodim rotatsiyasi/almashinuvini qayd etish. (+7 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.21
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.06
Nodes (29): Connection, Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan to'liq saqlash/yangilash., Bitta tashkilotni qo'shish yoki yangilash., SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Bitta tashkilotni qo'shish yoki yangilash (Alias)., Ommaviy tashkilotlarni saqlash va sonini qaytarish. (+21 more)

### Community 8 - "Toast Notification System"
Cohesion: 0.28
Nodes (6): CTk, Pop Tuman Tashkilotlari va INN Tizimi Zamonaviy Toast / Banner Bildirishnomalar, Qulay yordamchi funksiya., Oynaning pastki qismida silliq paydo bo'lib yo'qoluvchi bildirishnoma., show_toast(), ToastNotification

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.15
Nodes (12): 1-qadam. Loyihani yuklab olish, 2-qadam. Kerakli kutubxonalarni o'rnatish, 3-qadam. Dasturni ishga tushirish, 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish, 🔑 Kalit Fayllar va Sozlamalar, 📁 Loyiha Tuzilmasi, 📞 Muallif va Ruxsatnoma, 📦 Mustaqil Windows `.exe` Dasturini Yig'ish (+4 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.07
Nodes (47): CTkFrame, Style, apply_treeview_style(), Treeview ranglari va shriftlarini Light/Dark rejimga moslashtirish., copy_cabinet_quick(), open_cabinet_dialog(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinetga Dostup Dialog Oynasi (Cabinet Ac (+39 more)

### Community 21 - "hash_password"
Cohesion: 0.20
Nodes (13): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish., Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali (+5 more)

### Community 22 - "TelegramBotService"
Cohesion: 0.08
Nodes (21): authenticate_user(), hash_password(), Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish., Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash., Parolni SHA-256 xeshga aylantirish., verify_password(), Any, Telegramdan yangi xabarlarni tinglash sikli (Long polling). (+13 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.20
Nodes (9): Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), import_organizations_from_file(), Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, ui_qt.views.import_dialog: Excel va CSV fayllardan ommaviy import qilish dialogi, open_batch_import_dialog(), Any, Pop Tuman Tashkilotlari va INN Tizimi Excel va CSV Ommaviy Import Muloqot Oynasi (+1 more)

### Community 24 - "TestImportService"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 25 - "clean_inn"
Cohesion: 0.40
Nodes (3): Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, validate_phone(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish.

### Community 26 - "sanitize_text"
Cohesion: 0.15
Nodes (11): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, open_broadcast_dialog(), Any, ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5)., open_staff_history_dialog(), Any (+3 more)

### Community 27 - "MainWindow"
Cohesion: 0.07
Nodes (12): QMainWindow, MainWindow, Any, Status bar orqali chiroyli xabar chiqarish., Dastur yopilayotganda avtomatik zaxira nusxa yaratish., Pop Tuman Tizimining Asosiy PyQt5 Oynasi., Any, QWidget (+4 more)

### Community 28 - "TableView"
Cohesion: 0.11
Nodes (12): OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi., Any, QModelIndex, QWidget (+4 more)

### Community 29 - "TestQtArchitecture"
Cohesion: 0.17
Nodes (6): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., TestQtArchitecture, get_stylesheet(), Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Compact Edition) Kichik, Belgilangan mavzu (Dark yoki Light) uchun to'liq QSS stilini qaytaradi.

### Community 30 - "SettingsView"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 31 - "hash_password"
Cohesion: 0.18
Nodes (7): CategoryBarChart, CategoryLegend, QWidget, ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., Donut diagramma yonidagi interaktiv, foizli va rangli tushuntirish paneli (Legen, Toifalar taqsimotini solishtirish uchun zamonaviy gorizontal progress bar diagra, ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5). Senior-

### Community 32 - "MahallaPassportView"
Cohesion: 0.23
Nodes (6): QFrame, MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi.

### Community 33 - "TrashView"
Cohesion: 0.21
Nodes (7): Any, QWidget, ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5). O'chiril, Chiqindi qutisi ekrani., Chiqindi ro'yxatini yuklash., render_trash(), TrashView

### Community 34 - "CabinetDialog"
Cohesion: 0.24
Nodes (5): CabinetDialog, Any, QDialog, Belgilangan tashkilot bo'yicha matnni generatsiya qilish., Kabinetga dostup shablon oynasi.

### Community 35 - "open_record_dialog"
Cohesion: 0.18
Nodes (10): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service, open_mahalla_passport() (+2 more)

### Community 37 - ".test_view_imports"
Cohesion: 0.15
Nodes (8): BroadcastView, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi., HistoryView, QDialog, Kadrlar tarixi dialog oynasi., SQLite dan tarix yozuvlarini yuklash.

### Community 38 - "VerificationDialog"
Cohesion: 0.27
Nodes (4): Any, QDialog, Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 39 - "ImportDialog"
Cohesion: 0.25
Nodes (5): ImportDialog, open_batch_import_dialog(), Any, QDialog, Excel / CSV ommaviy import dialog oynasi.

### Community 40 - "OrgEditDialog"
Cohesion: 0.22
Nodes (10): copy_cabinet_quick(), open_cabinet_dialog(), ui_qt.views.cabinet_dialog: 'Kabinetga dostup' shablonini generatsiya qilish, bi, Oynani ochmasdan tezkor nusxalash., ui_qt.views.table_view: Asosiy tashkilotlar jadvali (Table View) (PyQt5). Senior, O'ng tugma bosilganda kontekst menyu., copy_verification_quick(), open_verification_dialog() (+2 more)

### Community 41 - "test_views.py"
Cohesion: 0.24
Nodes (9): Image, clean_phone_number(), generate_phone_qr_image(), Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish., open_mahalla_passport(), Any, Pop Tuman Tashkilotlari va INN Tizimi Mahalla "Yettiligi" Birlashgan Pasporti (M (+1 more)

### Community 42 - "render_settings"
Cohesion: 0.21
Nodes (6): QMouseEvent, QPaintEvent, QPoint, CategoryDonutChart, PyQt5 QPainter yordamida chiziladigan professional, 60 FPS Donut diagrammasi., data: [(nomi, soni, rang_hex), ...]

### Community 46 - "build_verification_text"
Cohesion: 0.27
Nodes (9): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+1 more)

### Community 47 - ".filter_data"
Cohesion: 0.27
Nodes (3): Sessiya yoki parol kiritish orqali ruxsatni tekshirish., DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish., Google Sheets bilan fonda sinxronlash (Thread-Safe).

### Community 48 - "DashboardView"
Cohesion: 0.24
Nodes (7): DashboardView, Any, QWidget, PyQt5 Zamonaviy, Professional Dashboard Ekrani., Statistika kartalarini, diagrammalarni va jadvalni to'ldirish., QFrame asosidagi ClickableCard vidjeti.         QPushButton cheklovlaridan holi,, render_dashboard()

### Community 49 - "main.py"
Cohesion: 0.24
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, Pop Tuman Tashkilotlari va INN Tizimi Eski ishga tushirish fayli bilan 100% orqa, main(), Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy ishga tushirish fayli - PyQt5, Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy ishga tushirish nuqtasi (Entr, PyQt5 ilovasini ishga tushirish (High-DPI qo'llab-quvvatlash bilan)., run_qt_app()

### Community 50 - ".setup_ui"
Cohesion: 0.22
Nodes (4): Mahalla 'Yettiligi' 360° Pasport oynasini ochish., Excel/CSV ommaviy import dialogini ochish., Kadrlar almashinuvi va rotatsiya tarixi oynasini ochish., Ommaviy xabarnoma (SMS & Telegram) dialogini ochish.

### Community 53 - "setup_logger"
Cohesion: 0.67
Nodes (3): Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger

## Knowledge Gaps
- **12 isolated node(s):** `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)`, `📁 Loyiha Tuzilmasi`, `1-qadam. Loyihani yuklab olish` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `Data Persistence & Backup Manager` to `UI App Core & Event Handlers`, `SQLiteManager`, `Services Package Architecture`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Why does `MahallaDasturi` connect `UI App Core & Event Handlers` to `External Services (Excel, QR, GSheets)`, `Data Persistence & Backup Manager`, `import_organizations_from_file`, `app.py`, `Services Package Architecture`, `.filter_data`, `main.py`, `.setup_ui`, `.open_cabinet`, `hash_password`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `sanitize_text`, `Data Persistence & Backup Manager`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MahallaDasturi` (e.g. with `TestViewImports` and `.test_app_import()`) actually correct?**
  _`MahallaDasturi` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `DataManager` (e.g. with `SQLiteManager` and `TestDataManager`) actually correct?**
  _`DataManager` has 4 INFERRED edges - model-reasoned connections that need verification._