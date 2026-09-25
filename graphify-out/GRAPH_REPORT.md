# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 65 files · ~102,455 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1027 nodes · 2078 edges · 53 communities (42 shown, 11 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 157 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c36b32c6`
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
- .save_all_organizations

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 56 edges
2. `TelegramBotService` - 48 edges
3. `TableView` - 42 edges
4. `DataManager` - 41 edges
5. `TestQtArchitecture` - 40 edges
6. `ContractsView` - 36 edges
7. `SettingsView` - 36 edges
8. `WorkerThread` - 32 edges
9. `SQLiteManager` - 30 edges
10. `OrgEditDialog` - 30 edges

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

## Communities (53 total, 11 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Sing, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.14
Nodes (9): PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, TestQtArchitecture, OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi. (+1 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (23): QMouseEvent, QPaintEvent, QPoint, Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, CategoryBarChart, CategoryDonutChart, CategoryLegend, ClickableCard (+15 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (40): normalize_text(), Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), get_telegram_bot_service(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash. (+32 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.05
Nodes (42): clean_inn(), clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish. (+34 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.23
Nodes (10): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis. (+2 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.13
Nodes (9): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Ma'lumotlar ombori boshqaruvi va atomik saqlash testlari (Isolated)., TestDataManager, Organization ma'lumotlar modeli testlari. (+1 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.21
Nodes (7): PasswordPromptDialog, Any, QDialog, Parolni ko'rsatish yoki yashirish., Amal ('edit' yoki 'settings') uchun parolni so'rash.     Agar joriy sessiyada av, Amallarni (tahrirlash yoki sozlamalar) himoyalash uchun zamonaviy modal dialog., request_password()

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test TableView search, pill selection, category filters., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.16
Nodes (6): Any, Tashkilotlar bo'yicha umumiy statistika hisoblash., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, Qidiruv, QR va Excel xizmatlari testlari., TestServices

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.16
Nodes (10): Any, QWidget, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish., Chiqindi ro'yxatini yuklash (Yuqori unumdorlik: updatesEnabled(False) va blockSi (+2 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.11
Nodes (12): ItemFlags, Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP (+4 more)

### Community 17 - "Organization"
Cohesion: 0.05
Nodes (31): Connection, Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., Bitta tashkilotni qo'shish yoki yangilash. (+23 more)

### Community 21 - "hash_password"
Cohesion: 0.06
Nodes (26): QLabel, QPushButton, Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash., AppsView, copy_file_to_windows_clipboard(), QFrame, QWidget, Yordamchi va Kommunal Dasturlar ekrani. (+18 more)

### Community 22 - "test_services.py"
Cohesion: 0.24
Nodes (8): generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., vCard 3.0 formatida kontakt ma'lumotlarini shakllantirish., Raqamli tashrif qog'ozi (vCard) uchun xotirada toza QR-kod tasvirini yaratish., QR-kod rasmini PNG fayl qilib saqlash.

### Community 23 - "import_organizations_from_file"
Cohesion: 0.11
Nodes (24): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+16 more)

### Community 24 - "TestImportService"
Cohesion: 0.05
Nodes (28): Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Forma label yaratish (mavzuga mos rang bilan)., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi). (+20 more)

### Community 25 - "clean_inn"
Cohesion: 0.16
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 26 - "sanitize_text"
Cohesion: 0.10
Nodes (23): core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, get_stylesheet(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha     to'liq va mu, open_broadcast_dialog() (+15 more)

### Community 27 - "MainWindow"
Cohesion: 0.06
Nodes (19): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk). (+11 more)

### Community 28 - "TableView"
Cohesion: 0.07
Nodes (16): QStyledItemDelegate, IzohDelegate, Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Izoh ustuni uchun maxsus zamonaviy inline muharrir (QLineEdit)., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash. (+8 more)

### Community 29 - "settings_view.py"
Cohesion: 0.24
Nodes (6): open_verification_dialog(), Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 30 - "telegram_bot.py"
Cohesion: 0.20
Nodes (5): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread

### Community 31 - "hash_password"
Cohesion: 0.15
Nodes (10): QPixmap, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., pil_to_qpixmap(), Any, Image, QDialog, QRDialog, QR kod tasvirini joriy rejim bo'yicha qayta chizish. (+2 more)

### Community 32 - "VerificationDialog"
Cohesion: 0.22
Nodes (5): BroadcastView, Any, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi.

### Community 33 - ".__init__"
Cohesion: 0.12
Nodes (12): get_utility_path(), Yordamchi dastur fayli yo'lini topish (BASE_DIR yoki PyInstaller MEIPASS)., Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Logger, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service (+4 more)

### Community 34 - "DataManager"
Cohesion: 0.17
Nodes (5): Test all dialogs for clean initialization, styles, and button bindings., ImportDialog, QDialog, Excel / CSV ommaviy import dialog oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 35 - "validate_inn"
Cohesion: 0.15
Nodes (16): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), is_service_account_available(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish. (+8 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.25
Nodes (8): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish., Foydalanuvchi talabiga to'liq mos keluvchi verifikatsiya shablon matnini yaratis

### Community 37 - "CabinetDialog"
Cohesion: 0.13
Nodes (13): build_cabinet_access_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, CabinetDialog, copy_cabinet_quick(), open_cabinet_dialog(), Any (+5 more)

### Community 38 - "build_verification_text"
Cohesion: 0.07
Nodes (16): Task 5: Avtomatlashtirilgan fonda davriy zaxira olish (Auto-Backup Scheduler)., Any, QWidget, Tizim sozlamalari ekrani., Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash., Avtomatik zaxira yoqilgan/o'chirilganda sozlamani yangilash., Zaxiralash vaqt oralig'i o'zgarganda. (+8 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.25
Nodes (5): Any, Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Tashkilotni Organization dataclass modeli sifatida olish., Xodimlar rotatsiyasi tarixini olish.

### Community 40 - "OrgEditDialog"
Cohesion: 0.17
Nodes (12): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+4 more)

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.14
Nodes (8): DataManager, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Xodim rotatsiyasi/almashinuvini qayd etish., Ma'lumotlar bazasining zaxira nusxasini yaratish (oxirgi 10 ta JSON va 30 ta SQL, Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi., TestFeatures12346

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.33
Nodes (4): HistoryView, QDialog, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.29
Nodes (3): Yozuvni Chiqindi qutisiga ko'chirish., Chiqindi qutisidan asosiy bazaga tiklash., Chiqindi qutisidan butunlay o'chirish.

### Community 47 - "TestDataManager"
Cohesion: 0.29
Nodes (6): ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., create_crisp_pixmap(), hex_to_rgba(), Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad, Retina / 4K / High-DPI o'lchamli kristall tiniqlikdagi QPixmap yaratish.     Win, ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5). Senior-

### Community 49 - "is_service_account_available"
Cohesion: 0.40
Nodes (3): Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi)., Mavjud tashkilot ma'lumotlarini yangilash (dict yoki Organization modeli qabul q, Tizimdagi harakatlarni qayd etish (JSON + SQLite).

### Community 50 - ".add_organization"
Cohesion: 0.40
Nodes (4): Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., SearchService, ui_qt.views.table_view: Asosiy tashkilotlar jadvali (Table View) (PyQt5). Senior

### Community 51 - "BroadcastView"
Cohesion: 0.40
Nodes (3): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, copy_verification_quick(), Oynani ochmasdan tezkor nusxalash.

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `pil_to_qpixmap` to `.__init__`, `External Services (Excel, QR, GSheets)`, `import_organizations_from_file`, `UI Views Test Suite`, `sync_contracts_data.py`, `export_organizations_to_excel`, `Any`, `is_service_account_available`, `Organization`, `clean_inn`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.195) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Core Configuration & Logging`, `Data Validation & Formatting`, `build_verification_text`, `SQLiteManager`, `settings_view.py`, `pil_to_qpixmap`, `Cloud Sync Verification`, `BroadcastView`, `hash_password`, `TestImportService`, `sanitize_text`, `TableView`, `telegram_bot.py`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `.__init__`, `CabinetDialog`, `pil_to_qpixmap`, `Services Package Architecture`, `.add_organization`, `test_services.py`, `sanitize_text`, `settings_view.py`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._