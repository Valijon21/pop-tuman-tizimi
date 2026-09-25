# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 65 files · ~102,969 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1031 nodes · 2093 edges · 61 communities (42 shown, 19 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 157 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `70626b5a`
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
- .send_welcome
- setup_logger
- .backup_data
- .get_organization_by_id
- .get_organization_by_inn
- .get_recent_activity
- broadcast_service.py
- .send_help

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
- `CabinetDialog` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/cabinet_dialog.py → core/threading_utils.py
- `SettingsView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/settings_view.py → core/threading_utils.py
- `IzohDelegate` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/table_view.py → core/threading_utils.py

## Import Cycles
- None detected.

## Communities (61 total, 19 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.33
Nodes (5): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.25
Nodes (6): OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.19
Nodes (10): create_crisp_pixmap(), Retina / 4K / High-DPI o'lchamli kristall tiniqlikdagi QPixmap yaratish.     Win, DashboardView, Any, QWidget, PyQt5 Zamonaviy, Professional Dashboard Ekrani., Dashboard'ning barcha vidjetlarini (kartalar, diagrammalar, sarlavhalar), Statistika kartalarini, diagrammalarni va jadvalni to'ldirish. (+2 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.10
Nodes (13): Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash., Botni fon rejimida ishga tushirish., start() metodi uchun qulay alias., HTTP sessiyani yaratish yoki yangilash (Connection pooling, keep-alive va adapte, Tarmoq uzilishi yoki xatolikdan so'ng HTTP sessiyani toza qayta ishga tushirish., Telegram API ga HTTP so'rov yuborish (Sessiya, Keep-Alive va xato holatlarini to, Inline tugma bosilganda Telegram yuklanish animatsiyasini to'xtatish. (+5 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.10
Nodes (21): clean_inn(), clean_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan (+13 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.23
Nodes (10): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis. (+2 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.16
Nodes (8): Tashkilotni Organization dataclass modeli sifatida olish., Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.11
Nodes (14): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, TestQtArchitecture, PasswordPromptDialog, Any, QDialog, Parolni ko'rsatish yoki yashirish. (+6 more)

### Community 8 - "settings_view.py"
Cohesion: 0.07
Nodes (17): Test TableView search, pill selection, category filters., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Test all dialogs for clean initialization, styles, and button bindings., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions. (+9 more)

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.13
Nodes (10): Any, Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, SearchService, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service (+2 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.08
Nodes (16): Task 5: Avtomatlashtirilgan fonda davriy zaxira olish (Auto-Backup Scheduler)., Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi., TestFeatures12346, Any, QWidget (+8 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.11
Nodes (12): ItemFlags, Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP (+4 more)

### Community 17 - "Organization"
Cohesion: 0.12
Nodes (8): Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Chiqindi qutisida barcha yangi ustunlar saqlanishini tekshirish., TestSQLiteManager

### Community 21 - "hash_password"
Cohesion: 0.07
Nodes (22): QLabel, QPushButton, Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash., AppsView, copy_file_to_windows_clipboard(), QFrame, QWidget, Yordamchi va Kommunal Dasturlar ekrani. (+14 more)

### Community 22 - "test_services.py"
Cohesion: 0.14
Nodes (14): get_telegram_bot_service(), Any, TelegramBotService uchun yagona namuna (Singleton) olish., Foydalanuvchiga HTML formatida xabar va ixtiyoriy inline/reply tugmalar yuborish, Mavjud xabar matnini joyida yangilash (In-place dynamic update - qotmasdan tezko, Qidiruv ko'rsatmasi va toifalar bo'yicha saralash inline tugmalari., Tuman bo'yicha jonli tahliliy statistikani ko'rsatish (In-place yangilash bilan), Shartnomalar va buxgalterlar bo'limi ko'rinishi. (+6 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.16
Nodes (18): authenticate_user(), hash_password(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash., Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash.     Br, Muayyan amal ('edit' yoki 'settings') uchun parolni tekshirish.     action='edit (+10 more)

### Community 24 - "TestImportService"
Cohesion: 0.06
Nodes (26): Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi)., Ma'lumotlarni validatsiya qilish va saqlash., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish. (+18 more)

### Community 25 - "clean_inn"
Cohesion: 0.15
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 26 - "sanitize_text"
Cohesion: 0.11
Nodes (27): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Sing, run_qt_app() (+19 more)

### Community 27 - "MainWindow"
Cohesion: 0.06
Nodes (19): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk). (+11 more)

### Community 28 - "TableView"
Cohesion: 0.07
Nodes (16): QStyledItemDelegate, IzohDelegate, Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Izoh ustuni uchun maxsus zamonaviy inline muharrir (QLineEdit)., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash. (+8 more)

### Community 29 - "settings_view.py"
Cohesion: 0.13
Nodes (12): format_phone(), Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., CSV fayldan tashkilotlarni aniqlash va import qilish. (+4 more)

### Community 30 - "telegram_bot.py"
Cohesion: 0.19
Nodes (10): normalize_text(), Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Qidiruv so'zi (INN, nom yoki F.I.SH) bo'yicha aniq tashkilotni O(1) topish., Yangi foydalanuvchini obunachilar ro'yxatiga qo'shish., Xodim yoki tashkilot mas'ulining boshqaruv ustuvorlik darajasi (1-10)., Toifa bo'yicha sahifalangan interaktiv tashkilotlar ro'yxati (Pagination). (+2 more)

### Community 31 - "hash_password"
Cohesion: 0.19
Nodes (6): QMouseEvent, QPaintEvent, QPoint, CategoryDonutChart, data: [(nomi, soni, rang_hex), ...], PyQt5 QPainter yordamida chiziladigan professional, 60 FPS Donut diagrammasi.

### Community 32 - "VerificationDialog"
Cohesion: 0.07
Nodes (15): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, BroadcastView, open_broadcast_dialog(), Any (+7 more)

### Community 33 - ".__init__"
Cohesion: 0.33
Nodes (3): get_utility_path(), Yordamchi dastur fayli yo'lini topish (BASE_DIR yoki PyInstaller MEIPASS)., ui_qt.views.apps_view: Yordamchi va Kommunal Dasturlar (Utilities & Tools) Sahif

### Community 34 - "DataManager"
Cohesion: 0.15
Nodes (7): Connection, Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., SQLite ulanishini olish va WAL rejimini faollashtirish., Xodim rotatsiyasi/almashinuvini tarix jadvaliga qo'shish (ko'p qirrali parametrl, Tizimdagi harakatni SQLite jurnaliga qayd etish., Agar SQLite jadvali bo'sh bo'lsa, JSON fayldan barcha yozuvlarni avtomatik ko'ch, SQLite bazasini vaqt tamg'asi bilan zaxiralash.

### Community 35 - "validate_inn"
Cohesion: 0.13
Nodes (18): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), is_service_account_available(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish. (+10 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.12
Nodes (14): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+6 more)

### Community 37 - "CabinetDialog"
Cohesion: 0.12
Nodes (12): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., CabinetDialog, copy_cabinet_quick(), Any (+4 more)

### Community 38 - "build_verification_text"
Cohesion: 0.09
Nodes (10): QWidget, Tizim sozlamalari ekrani., Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash., Avtomatik zaxira yoqilgan/o'chirilganda sozlamani yangilash., Zaxiralash vaqt oralig'i o'zgarganda., Fonda zaxiralashni hoziroq sinab ko'rish., MainWindow dan chaqiriladigan oxirgi zaxira vaqti ko'rsatkichi. (+2 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.15
Nodes (8): generate_salt(), hash_password_salted(), Xavfsiz tasodifiy salt (tuz) heks-satrini yaratish., PBKDF2-HMAC-SHA256 yordamida parolni avtomatik salt bilan xeshlash., Amallar bo'yicha parollarni (edit va settings) tekshirish., Tahrirlash parolini yangilash (standart: 1234567)., Sozlamalar parolini yangilash (standart: 773423321v)., Eski interfeyslar bilan moslik uchun alias.

### Community 40 - "OrgEditDialog"
Cohesion: 0.06
Nodes (43): QPixmap, BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+35 more)

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.19
Nodes (7): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, HistoryView, open_staff_history_dialog(), Any, QDialog, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.14
Nodes (14): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+6 more)

### Community 47 - "TestDataManager"
Cohesion: 0.22
Nodes (6): ClickableCard, ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., Tugma (QPushButton) cheklovlarisiz, matnlarni siqib qo'ymaydigan     va to'liq d, hex_to_rgba(), Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad, ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5). Senior-

### Community 48 - "Any"
Cohesion: 0.17
Nodes (7): Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, Ommaviy tashkilotlarni saqlash va sonini qaytarish., Chiqindi qutisidagi barcha yozuvlarni olish., Chiqindi qutisini to'liq saqlash., Xodimlar tarixini olish (tashkilot yoki mahalla bo'yicha).

### Community 49 - "is_service_account_available"
Cohesion: 0.21
Nodes (6): CategoryBarChart, CategoryLegend, QFrame, QWidget, Donut diagramma yonidagi interaktiv, foizli va rangli tushuntirish paneli (Legen, Toifalar taqsimotini solishtirish uchun zamonaviy gorizontal progress bar diagra

### Community 50 - ".add_organization"
Cohesion: 0.24
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Baza jadvallari va indekslarini yaratish., SQLiteManager

### Community 54 - "setup_logger"
Cohesion: 0.67
Nodes (3): Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `export_organizations_to_excel` to `External Services (Excel, QR, GSheets)`, `import_organizations_from_file`, `UI Views Test Suite`, `OrgEditDialog`, `pil_to_qpixmap`, `Services Package Architecture`, `Cloud Sync Verification`, `.add_organization`, `BroadcastView`, `.backup_data`, `clean_inn`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `VerificationDialog`, `Core Configuration & Logging`, `Data Validation & Formatting`, `build_verification_text`, `SQLiteManager`, `settings_view.py`, `.test_07_dialogs_instantiation`, `export_organizations_to_excel`, `Cloud Sync Verification`, `hash_password`, `TestImportService`, `sanitize_text`, `TableView`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `extract_sheet_id`, `CabinetDialog`, `OrgEditDialog`, `export_organizations_to_excel`, `Services Package Architecture`, `Cloud Sync Verification`, `.send_welcome`, `test_services.py`, `sanitize_text`, `.send_help`, `telegram_bot.py`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._