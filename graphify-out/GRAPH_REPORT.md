# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 65 files · ~82,631 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1005 nodes · 2020 edges · 60 communities (39 shown, 21 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 135 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8393845d`
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
- settings_view.py
- Application Lifecycle & Entry Points
- PyInstaller Windows Build Pipeline
- Automated Test Runner
- Core Architecture Package
- Database Package Architecture
- Services Package Architecture
- Cloud Sync Verification
- OrganizationTableModel
- Organization
- rules/graphify.md
- workflows/graphify.md
- hash_password
- test_services.py
- import_organizations_from_file
- TestImportService
- clean_inn
- sanitize_text
- MainWindow
- TableView
- settings_view.py
- telegram_bot.py
- hash_password
- VerificationDialog
- .__init__
- DataManager
- validate_inn
- extract_sheet_id
- CabinetDialog
- build_verification_text
- sync_contracts_data.py
- OrgEditDialog
- pil_to_qpixmap
- .test_07_dialogs_instantiation
- components/__init__.py
- ui_qt/__init__.py
- ui_qt/views/__init__.py
- export_organizations_to_excel
- TestDataManager
- Any
- is_service_account_available
- .add_organization
- BroadcastView
- .update_settings_password
- .set_theme
- .trigger_manual_auto_backup
- .add_staff_history
- .test_task5_auto_backup_scheduler
- render_settings
- .on_backup_interval_changed
- .update_edit_password

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 56 edges
2. `TelegramBotService` - 48 edges
3. `DataManager` - 41 edges
4. `TestQtArchitecture` - 40 edges
5. `TableView` - 40 edges
6. `ContractsView` - 36 edges
7. `SettingsView` - 36 edges
8. `WorkerThread` - 31 edges
9. `SQLiteManager` - 30 edges
10. `OrgEditDialog` - 29 edges

## Surprising Connections (you probably didn't know these)
- `TestServices` --uses--> `WorkerThread`  [INFERRED]
  tests/test_services.py → core/threading_utils.py
- `MainWindow` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/app_window.py → core/threading_utils.py
- `BroadcastView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/broadcast_view.py → core/threading_utils.py
- `CabinetDialog` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/cabinet_dialog.py → core/threading_utils.py
- `ImportDialog` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/import_dialog.py → core/threading_utils.py

## Import Cycles
- None detected.

## Communities (60 total, 21 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Sing, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.21
Nodes (5): BroadcastView, Any, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi.

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.18
Nodes (7): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, CategoryBarChart, CategoryLegend, QFrame, QWidget, Donut diagramma yonidagi interaktiv, foizli va rangli tushuntirish paneli (Legen, Toifalar taqsimotini solishtirish uchun zamonaviy gorizontal progress bar diagra

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (40): normalize_text(), Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), get_telegram_bot_service(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash. (+32 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.15
Nodes (14): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+6 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.15
Nodes (9): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., import_organizations_from_file(), Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari. (+1 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.21
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.05
Nodes (31): Connection, Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., Bitta tashkilotni qo'shish yoki yangilash. (+23 more)

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test TableView search, pill selection, category filters., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.05
Nodes (34): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+26 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.13
Nodes (11): Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Any, QWidget, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish. (+3 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.14
Nodes (6): PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash., Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, TestQtArchitecture

### Community 21 - "hash_password"
Cohesion: 0.10
Nodes (16): QLabel, AppsView, QFrame, QWidget, UzCrypto (E-IMZO) dasturi uchun karta vidjeti., AnyDesk (Masofaviy Texnik Yordam) dasturi uchun karta vidjeti., Yordamchi va Kommunal Dasturlar ekrani., Yo'riqnoma va tezkor eslatmalar kartasi. (+8 more)

### Community 22 - "test_services.py"
Cohesion: 0.11
Nodes (21): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+13 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.08
Nodes (31): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+23 more)

### Community 24 - "TestImportService"
Cohesion: 0.06
Nodes (24): ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi)., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish., ContractsView, Any (+16 more)

### Community 25 - "clean_inn"
Cohesion: 0.06
Nodes (31): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+23 more)

### Community 26 - "sanitize_text"
Cohesion: 0.12
Nodes (22): core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, get_stylesheet() (+14 more)

### Community 27 - "MainWindow"
Cohesion: 0.07
Nodes (18): QMainWindow, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk)., Sozlamalar sahifasini ochish (773423321v paroli bilan himoyalangan). (+10 more)

### Community 28 - "TableView"
Cohesion: 0.10
Nodes (12): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish. (+4 more)

### Community 29 - "settings_view.py"
Cohesion: 0.29
Nodes (4): O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., Ma'lumotlarni validatsiya qilish va saqlash.

### Community 31 - "hash_password"
Cohesion: 0.14
Nodes (12): QPixmap, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., open_qr_dialog(), pil_to_qpixmap(), Any, Image, QDialog, QRDialog (+4 more)

### Community 32 - "VerificationDialog"
Cohesion: 0.15
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 33 - ".__init__"
Cohesion: 0.10
Nodes (15): get_utility_path(), Yordamchi dastur fayli yo'lini topish (BASE_DIR yoki PyInstaller MEIPASS)., Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Logger, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service (+7 more)

### Community 34 - "DataManager"
Cohesion: 0.17
Nodes (5): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, ImportDialog, QDialog, Excel / CSV ommaviy import dialog oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 35 - "validate_inn"
Cohesion: 0.20
Nodes (13): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish., Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali (+5 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.23
Nodes (5): Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 37 - "CabinetDialog"
Cohesion: 0.13
Nodes (11): build_cabinet_access_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, CabinetDialog, copy_cabinet_quick(), Any, QDialog (+3 more)

### Community 38 - "build_verification_text"
Cohesion: 0.16
Nodes (5): QWidget, Tizim sozlamalari ekrani., Avtomatik zaxira yoqilgan/o'chirilganda sozlamani yangilash., Fonda zaxiralashni hoziroq sinab ko'rish., SettingsView

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.20
Nodes (6): MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi., Hozirgi mahalla pasportini rasmiy A4 PDF hujjat ko'rinishida eksport qilish.

### Community 40 - "OrgEditDialog"
Cohesion: 0.20
Nodes (7): Test all dialogs for clean initialization, styles, and button bindings., OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.23
Nodes (8): DashboardView, Any, QWidget, PyQt5 Zamonaviy, Professional Dashboard Ekrani., Dashboard'ning barcha vidjetlarini (kartalar, diagrammalar, sarlavhalar), Statistika kartalarini, diagrammalarni va jadvalni to'ldirish., Senior-darajadagi zamonaviy, mukammal balanslangan KPI statistika kartasi., render_dashboard()

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.23
Nodes (6): HistoryView, open_staff_history_dialog(), Any, QDialog, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 47 - "TestDataManager"
Cohesion: 0.25
Nodes (6): ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., create_crisp_pixmap(), hex_to_rgba(), Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad, Retina / 4K / High-DPI o'lchamli kristall tiniqlikdagi QPixmap yaratish.     Win, ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5). Senior-

### Community 48 - "Any"
Cohesion: 0.19
Nodes (6): QMouseEvent, QPaintEvent, QPoint, CategoryDonutChart, data: [(nomi, soni, rang_hex), ...], PyQt5 QPainter yordamida chiziladigan professional, 60 FPS Donut diagrammasi.

### Community 49 - "is_service_account_available"
Cohesion: 0.22
Nodes (4): is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., Mavjud sozlamalarni yuklash., Telegram botni qo'lda qayta ishga tushirish.

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `clean_inn` to `VerificationDialog`, `.__init__`, `External Services (Excel, QR, GSheets)`, `UI Views Test Suite`, `SQLiteManager`, `export_organizations_to_excel`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Data Validation & Formatting`, `build_verification_text`, `settings_view.py`, `pil_to_qpixmap`, `.test_07_dialogs_instantiation`, `OrgEditDialog`, `Cloud Sync Verification`, `Organization`, `.add_organization`, `hash_password`, `TestImportService`, `clean_inn`, `sanitize_text`, `TableView`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `.__init__`, `extract_sheet_id`, `CabinetDialog`, `Services Package Architecture`, `clean_inn`, `sanitize_text`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `TestQtArchitecture` (e.g. with `MainWindow` and `OrganizationTableModel`) actually correct?**
  _`TestQtArchitecture` has 22 INFERRED edges - model-reasoned connections that need verification._