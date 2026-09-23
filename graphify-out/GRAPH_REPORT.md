# Graph Report - tashkilotlar INN tizim  (2026-09-24)

## Corpus Check
- 58 files · ~61,336 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 755 nodes · 1410 edges · 34 communities (25 shown, 9 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f41c6ba4`
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
- Cloud Sync Verification
- rules/graphify.md
- workflows/graphify.md
- hash_password
- import_organizations_from_file
- TestImportService
- clean_inn
- sanitize_text
- MainWindow
- TableView
- hash_password
- .add_staff_history
- build_verification_text
- sync_contracts_data.py
- components/__init__.py
- ui_qt/__init__.py
- ui_qt/views/__init__.py
- TestDataManager

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 41 edges
2. `TableView` - 39 edges
3. `DataManager` - 38 edges
4. `TestQtArchitecture` - 31 edges
5. `ContractsView` - 29 edges
6. `SQLiteManager` - 27 edges
7. `TelegramBotService` - 26 edges
8. `SettingsView` - 26 edges
9. `OrgEditDialog` - 25 edges
10. `WorkerThread` - 22 edges

## Surprising Connections (you probably didn't know these)
- `TestServices` --uses--> `WorkerThread`  [INFERRED]
  tests/test_services.py → core/threading_utils.py
- `BroadcastView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/broadcast_view.py → core/threading_utils.py
- `TableView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/table_view.py → core/threading_utils.py
- `ContractsSyncService` --uses--> `DataManager`  [INFERRED]
  services/sync_contracts_data.py → database/data_manager.py
- `ExcelSyncService` --uses--> `DataManager`  [INFERRED]
  services/sync_excel_data.py → database/data_manager.py

## Import Cycles
- None detected.

## Communities (34 total, 9 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI qo'llab-quvvatlash bilan)., run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.06
Nodes (21): Orientation, QAbstractTableModel, Any, Foydalanuvchiga HTML formatida xabar yuborish., Barcha obuna bo'lgan mas'ullarga ommaviy xabarnoma tarqatish., Telegramdan yangi xabarlarni tinglash sikli (Long polling)., Telegram Bot orqali tashkilotlar bazasini qidirish, verifikatsiya va ommaviy xab, Bot tokeni kiritilgan va sozlanganligini tekshirish. (+13 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (29): QMouseEvent, QPaintEvent, QPoint, tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., TestQtArchitecture, CategoryBarChart, CategoryDonutChart (+21 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.13
Nodes (13): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish., Foydalanuvchi talabiga to'liq mos keluvchi verifikatsiya shablon matnini yaratis (+5 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.21
Nodes (5): BroadcastView, Any, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi.

### Community 5 - "import_organizations_from_file"
Cohesion: 0.16
Nodes (10): CabinetDialog, copy_cabinet_quick(), open_cabinet_dialog(), Any, QDialog, ui_qt.views.cabinet_dialog: 'Kabinetga dostup' shablonini generatsiya qilish, bi, Tanlangan tashkilot ma'lumotlarini yuklash., Oynani ochmasdan tezkor nusxalash. (+2 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.05
Nodes (39): clean_inn(), clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish. (+31 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.05
Nodes (31): Connection, Any, Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Bitta tashkilotni qo'shish yoki yangilash., Bitta tashkilotni qo'shish yoki yangilash (Alias). (+23 more)

### Community 8 - "Toast Notification System"
Cohesion: 0.19
Nodes (14): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish., Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali (+6 more)

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.06
Nodes (29): Image, BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+21 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.17
Nodes (8): Any, QWidget, ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5). O'chiril, Chiqindi qutisi ekrani., Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish., Chiqindi ro'yxatini yuklash., render_trash(), TrashView

### Community 21 - "hash_password"
Cohesion: 0.16
Nodes (9): build_cabinet_access_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, open_mahalla_passport(), Any (+1 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.15
Nodes (19): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+11 more)

### Community 24 - "TestImportService"
Cohesion: 0.08
Nodes (17): ContractsView, Any, QFrame, QWidget, KPI statistika kartochkasini yaratish., Mavzuni Dark / Light rejimiga moslashtirish., Shartnoma va Ulanishlar Monitoringi Sahifasi., Ctrl+F bosilganda qidiruv maydoniga o'tish. (+9 more)

### Community 25 - "clean_inn"
Cohesion: 0.08
Nodes (19): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+11 more)

### Community 26 - "sanitize_text"
Cohesion: 0.13
Nodes (15): core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, get_stylesheet(), Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Compact Edition) Kichik, Belgilangan mavzu (Dark yoki Light) uchun to'liq QSS stilini qaytaradi., open_broadcast_dialog(), ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5). (+7 more)

### Community 27 - "MainWindow"
Cohesion: 0.10
Nodes (8): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Status bar orqali chiroyli xabar chiqarish., Dastur yopilayotganda avtomatik zaxira nusxa yaratish., Pop Tuman Tizimining Asosiy PyQt5 Oynasi.

### Community 28 - "TableView"
Cohesion: 0.10
Nodes (12): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)., PyQt5 Tashkilotlar Jadvali Ekrani. (+4 more)

### Community 31 - "hash_password"
Cohesion: 0.09
Nodes (15): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, HistoryView, QDialog, Kadrlar tarixi dialog oynasi., SQLite dan tarix yozuvlarini yuklash., MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash. (+7 more)

### Community 35 - ".add_staff_history"
Cohesion: 0.15
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 38 - "build_verification_text"
Cohesion: 0.06
Nodes (19): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., ImportDialog (+11 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.24
Nodes (9): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis., dataulan.xls faylini o'qib, bazadagi tashkilotlarni shartnoma ma'lumotlari bilan (+1 more)

### Community 54 - "TestDataManager"
Cohesion: 0.24
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `clean_inn` to `Core Configuration & Logging`, `.add_staff_history`, `UI Views Test Suite`, `SQLiteManager`, `sync_contracts_data.py`, `hash_password`, `TestDataManager`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.238) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `clean_inn`, `TestDataManager`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Data Validation & Formatting`, `build_verification_text`, `Cloud Sync Verification`, `hash_password`, `TestImportService`, `clean_inn`, `sanitize_text`, `TableView`, `hash_password`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `TestQtArchitecture` (e.g. with `MainWindow` and `OrganizationTableModel`) actually correct?**
  _`TestQtArchitecture` has 18 INFERRED edges - model-reasoned connections that need verification._