# Graph Report - tashkilotlar INN tizim  (2026-09-24)

## Corpus Check
- 61 files · ~68,242 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 884 nodes · 1787 edges · 49 communities (37 shown, 12 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 123 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5aabb65e`
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
- telegram_bot.py
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
- clean_inn

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 48 edges
2. `TelegramBotService` - 43 edges
3. `TableView` - 40 edges
4. `DataManager` - 38 edges
5. `TestQtArchitecture` - 36 edges
6. `ContractsView` - 33 edges
7. `WorkerThread` - 28 edges
8. `OrgEditDialog` - 28 edges
9. `SQLiteManager` - 27 edges
10. `SettingsView` - 27 edges

## Surprising Connections (you probably didn't know these)
- `TestServices` --uses--> `WorkerThread`  [INFERRED]
  tests/test_services.py → core/threading_utils.py
- `BroadcastView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/broadcast_view.py → core/threading_utils.py
- `CabinetDialog` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/cabinet_dialog.py → core/threading_utils.py
- `ImportDialog` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/import_dialog.py → core/threading_utils.py
- `SettingsView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/settings_view.py → core/threading_utils.py

## Import Cycles
- None detected.

## Communities (49 total, 12 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI qo'llab-quvvatlash bilan)., run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.10
Nodes (16): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti, Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini (+8 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (27): QMouseEvent, QPaintEvent, QPoint, tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, TestQtArchitecture, CategoryBarChart (+19 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.07
Nodes (36): normalize_text(), Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Qidiruv so'zi (INN, nom yoki F.I.SH) bo'yicha aniq tashkilotni O(1) topish., Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash. (+28 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.16
Nodes (14): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+6 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.14
Nodes (10): build_cabinet_access_text(), Any, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, CabinetDialog, copy_cabinet_quick(), Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash. (+2 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.16
Nodes (9): Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari. (+1 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.05
Nodes (31): Connection, Any, Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Bitta tashkilotni qo'shish yoki yangilash., Bitta tashkilotni qo'shish yoki yangilash (Alias). (+23 more)

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., Test TableView search, pill selection, category filters., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.19
Nodes (5): Any, Tashkilotlar bo'yicha umumiy statistika hisoblash., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, Qidiruv, QR va Excel xizmatlari testlari., TestServices

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.17
Nodes (8): Any, QWidget, ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5). O'chiril, Chiqindi qutisi ekrani., Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish., Chiqindi ro'yxatini yuklash., render_trash(), TrashView

### Community 16 - "OrganizationTableModel"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.14
Nodes (8): Any, core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, ui_qt.views.verification_dialog: 'Verifikatsiya so'rovi' shablonini generatsiya

### Community 21 - "hash_password"
Cohesion: 0.14
Nodes (12): QPixmap, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., open_qr_dialog(), pil_to_qpixmap(), Any, Image, QDialog, QRDialog (+4 more)

### Community 22 - "test_services.py"
Cohesion: 0.21
Nodes (11): clean_phone_number(), generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., vCard 3.0 formatida kontakt ma'lumotlarini shakllantirish., Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish. (+3 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.15
Nodes (19): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+11 more)

### Community 24 - "TestImportService"
Cohesion: 0.06
Nodes (26): QLabel, Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Forma label yaratish (mavzuga mos rang bilan)., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi). (+18 more)

### Community 25 - "clean_inn"
Cohesion: 0.06
Nodes (33): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+25 more)

### Community 26 - "sanitize_text"
Cohesion: 0.13
Nodes (18): Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., get_stylesheet(), hex_to_rgba(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad (+10 more)

### Community 27 - "MainWindow"
Cohesion: 0.09
Nodes (12): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., QR-kod oynasini ochish., Telegram botni fon rejimida (asinxron) ishga tushirish. (+4 more)

### Community 28 - "TableView"
Cohesion: 0.10
Nodes (13): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish. (+5 more)

### Community 29 - "settings_view.py"
Cohesion: 0.19
Nodes (14): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish., Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali (+6 more)

### Community 31 - "hash_password"
Cohesion: 0.19
Nodes (7): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, HistoryView, open_staff_history_dialog(), Any, QDialog, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 32 - "VerificationDialog"
Cohesion: 0.23
Nodes (5): Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 33 - ".__init__"
Cohesion: 0.16
Nodes (8): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, open_broadcast_dialog(), ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5).

### Community 34 - "DataManager"
Cohesion: 0.16
Nodes (6): ImportDialog, open_batch_import_dialog(), Any, QDialog, ui_qt.views.import_dialog: Excel va CSV fayllardan ommaviy import qilish dialogi, Excel / CSV ommaviy import dialog oynasi.

### Community 35 - "validate_inn"
Cohesion: 0.19
Nodes (7): import_organizations_from_file(), Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 36 - "extract_sheet_id"
Cohesion: 0.25
Nodes (8): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish., Foydalanuvchi talabiga to'liq mos keluvchi verifikatsiya shablon matnini yaratis

### Community 37 - "telegram_bot.py"
Cohesion: 0.24
Nodes (6): Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., SearchService, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service, ui_qt.views.table_view: Asosiy tashkilotlar jadvali (Table View) (PyQt5). Senior

### Community 38 - "build_verification_text"
Cohesion: 0.10
Nodes (10): is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., Any, QWidget, Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash., Tizim sozlamalari ekrani., Telegram botni qo'lda qayta ishga tushirish. (+2 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.23
Nodes (6): QFrame, MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi.

### Community 40 - "OrgEditDialog"
Cohesion: 0.22
Nodes (6): Test all dialogs for clean initialization, styles, and button bindings., OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi.

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.24
Nodes (9): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis., dataulan.xls faylini o'qib, bazadagi tashkilotlarni shartnoma ma'lumotlari bilan (+1 more)

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.22
Nodes (5): O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., Ma'lumotlarni validatsiya qilish va saqlash., Ma'lumotlarni validatsiya qilish va saqlash.

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.50
Nodes (3): export_organizations_to_excel(), Any, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash.

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `clean_inn` to `.__init__`, `External Services (Excel, QR, GSheets)`, `telegram_bot.py`, `UI Views Test Suite`, `SQLiteManager`, `pil_to_qpixmap`, `TestDataManager`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `VerificationDialog`, `Core Configuration & Logging`, `telegram_bot.py`, `import_organizations_from_file`, `Services Package Architecture`, `Organization`, `test_services.py`, `clean_inn`, `sanitize_text`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Data Validation & Formatting`, `DataManager`, `build_verification_text`, `OrgEditDialog`, `settings_view.py`, `Cloud Sync Verification`, `TestImportService`, `clean_inn`, `sanitize_text`, `TableView`, `hash_password`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 7 INFERRED edges - model-reasoned connections that need verification._