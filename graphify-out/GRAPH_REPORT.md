# Graph Report - tashkilotlar INN tizim  (2026-09-24)

## Corpus Check
- 63 files · ~71,408 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 935 nodes · 1890 edges · 48 communities (38 shown, 10 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 131 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3d63d037`
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
- BroadcastView

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 53 edges
2. `TelegramBotService` - 48 edges
3. `DataManager` - 41 edges
4. `TableView` - 40 edges
5. `TestQtArchitecture` - 36 edges
6. `ContractsView` - 36 edges
7. `SettingsView` - 34 edges
8. `WorkerThread` - 31 edges
9. `SQLiteManager` - 30 edges
10. `OrgEditDialog` - 28 edges

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

## Communities (48 total, 10 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI va Yagona Nusxa / Single Instance himo, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.20
Nodes (11): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti, Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini (+3 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.05
Nodes (28): QMouseEvent, QPaintEvent, QPoint, tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, TestQtArchitecture (+20 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (38): normalize_text(), Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash., Qidiruv so'zi (INN, nom yoki F.I.SH) bo'yicha aniq tashkilotni O(1) topish. (+30 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.16
Nodes (13): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+5 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.20
Nodes (9): Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, open_cabinet_dialog(), ui_qt.views.cabinet_dialog: 'Kabinetga dostup' shablonini generatsiya qilish, bi, ui_qt.views.contracts_view: Shartnoma va Ulanishlar Monitoringi Ekrani (PyQt5)., ui_qt.views.mahalla_passport_view: Mahalla 'Yettiligi' 360° Pasport oynasi (PyQt, open_qr_dialog(), ui_qt.views.qr_dialog: Telefon raqami va tashkilot ma'lumotlari uchun zamonaviy, Ilova oynasida QR dialogini xavfsiz ochish. (+1 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.21
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.05
Nodes (31): Connection, Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., Bitta tashkilotni qo'shish yoki yangilash. (+23 more)

### Community 8 - "settings_view.py"
Cohesion: 0.05
Nodes (24): QPixmap, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Test all dialogs for clean initialization, styles, and button bindings., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling. (+16 more)

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.15
Nodes (7): extract_sheet_id(), URL yoki matndan Google Sheet ID sini ajratib olish., Any, Tashkilotlar bo'yicha umumiy statistika hisoblash., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, Qidiruv, QR va Excel xizmatlari testlari., TestServices

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.08
Nodes (16): Task 5: Avtomatlashtirilgan fonda davriy zaxira olish (Auto-Backup Scheduler)., Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi., TestFeatures12346, Any, QWidget (+8 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.20
Nodes (5): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread

### Community 21 - "hash_password"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 22 - "test_services.py"
Cohesion: 0.23
Nodes (10): clean_phone_number(), generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., vCard 3.0 formatida kontakt ma'lumotlarini shakllantirish., Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish. (+2 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.15
Nodes (19): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+11 more)

### Community 24 - "TestImportService"
Cohesion: 0.06
Nodes (26): QLabel, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Forma label yaratish (mavzuga mos rang bilan)., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi)., Ma'lumotlarni validatsiya qilish va saqlash. (+18 more)

### Community 25 - "clean_inn"
Cohesion: 0.06
Nodes (33): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+25 more)

### Community 26 - "sanitize_text"
Cohesion: 0.17
Nodes (13): core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, get_stylesheet(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha     to'liq va mu, open_broadcast_dialog(), ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5). (+5 more)

### Community 27 - "MainWindow"
Cohesion: 0.07
Nodes (15): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., QR-kod oynasini ochish., Telegram botni fon rejimida (asinxron) ishga tushirish. (+7 more)

### Community 28 - "TableView"
Cohesion: 0.10
Nodes (12): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish. (+4 more)

### Community 29 - "settings_view.py"
Cohesion: 0.24
Nodes (12): Client, download_data_from_sheet(), get_gspread_client(), open_spreadsheet(), Any, Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali, ID, URL yoki nom orqali jadvalni ochish., Ma'lumotlar ro'yxatini Google Sheetga yuklash (to'liq 13 ta ustun bilan). (+4 more)

### Community 30 - "telegram_bot.py"
Cohesion: 0.29
Nodes (5): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish.

### Community 31 - "hash_password"
Cohesion: 0.29
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., SearchService, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service

### Community 32 - "VerificationDialog"
Cohesion: 0.40
Nodes (4): ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., hex_to_rgba(), Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad, ui_qt.views.dashboard_view: Asosiy boshqaruv paneli (Dashboard) (PyQt5). Senior-

### Community 33 - ".__init__"
Cohesion: 0.14
Nodes (9): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Logger, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, tests.test_features_12346: 1, 2, 3, 4, 6-topshiriqlar bo'yicha maxsus sinov test (+1 more)

### Community 34 - "DataManager"
Cohesion: 0.18
Nodes (5): ImportDialog, open_batch_import_dialog(), Any, QDialog, Excel / CSV ommaviy import dialog oynasi.

### Community 35 - "validate_inn"
Cohesion: 0.19
Nodes (9): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val (+1 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.11
Nodes (17): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+9 more)

### Community 38 - "build_verification_text"
Cohesion: 0.07
Nodes (14): is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., Any, QWidget, Tizim sozlamalari ekrani., Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash., Avtomatik zaxira yoqilgan/o'chirilganda sozlamani yangilash. (+6 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.15
Nodes (9): QFrame, MahallaPassportView, open_mahalla_passport(), Any, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi. (+1 more)

### Community 40 - "OrgEditDialog"
Cohesion: 0.32
Nodes (5): OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi.

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.24
Nodes (9): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis., dataulan.xls faylini o'qib, bazadagi tashkilotlarni shartnoma ma'lumotlari bilan (+1 more)

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.29
Nodes (4): O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., Ma'lumotlarni validatsiya qilish va saqlash.

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.24
Nodes (9): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+1 more)

### Community 51 - "BroadcastView"
Cohesion: 0.10
Nodes (12): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, BroadcastView, Any, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi., HistoryView, open_staff_history_dialog() (+4 more)

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `clean_inn` to `.__init__`, `External Services (Excel, QR, GSheets)`, `UI Views Test Suite`, `SQLiteManager`, `pil_to_qpixmap`, `TestDataManager`, `Cloud Sync Verification`, `sanitize_text`, `MainWindow`, `hash_password`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `Core Configuration & Logging`, `.__init__`, `extract_sheet_id`, `import_organizations_from_file`, `settings_view.py`, `Services Package Architecture`, `Cloud Sync Verification`, `test_services.py`, `clean_inn`, `sanitize_text`, `hash_password`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Data Validation & Formatting`, `DataManager`, `build_verification_text`, `sync_contracts_data.py`, `settings_view.py`, `OrgEditDialog`, `Cloud Sync Verification`, `Organization`, `BroadcastView`, `TestImportService`, `clean_inn`, `sanitize_text`, `TableView`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._