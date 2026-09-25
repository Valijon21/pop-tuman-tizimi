# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 65 files · ~75,496 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1013 nodes · 2053 edges · 53 communities (40 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 153 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `21f5ff79`
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
- .trigger_manual_auto_backup

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

## Communities (53 total, 13 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Sing, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.12
Nodes (9): Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, Ommaviy tashkilotlarni saqlash va sonini qaytarish., Tashkilotni unikal ID si bo'yicha olish., Tashkilotni INN si bo'yicha olish., Xodimlar tarixini olish (tashkilot yoki mahalla bo'yicha)., So'nggi faoliyat jurnallarini olish. (+1 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (30): QMouseEvent, QPaintEvent, QPoint, tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, TestQtArchitecture, CategoryBarChart (+22 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (42): normalize_text(), Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), get_telegram_bot_service(), Any, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish. (+34 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.15
Nodes (15): clean_inn(), clean_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+7 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 6 - "UI Views Test Suite"
Cohesion: 0.19
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.12
Nodes (9): Connection, Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., SQLite ulanishini olish va WAL rejimini faollashtirish., Chiqindi qutisidagi barcha yozuvlarni olish., Chiqindi qutisini to'liq saqlash., Xodim rotatsiyasi/almashinuvini tarix jadvaliga qo'shish (ko'p qirrali parametrl, Tizimdagi harakatni SQLite jurnaliga qayd etish. (+1 more)

### Community 8 - "settings_view.py"
Cohesion: 0.06
Nodes (22): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, Test TableView search, pill selection, category filters., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Test all dialogs for clean initialization, styles, and button bindings., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling. (+14 more)

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.12
Nodes (10): extract_sheet_id(), URL yoki matndan Google Sheet ID sini ajratib olish., Any, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, SearchService (+2 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.14
Nodes (11): Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Any, QWidget, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish. (+3 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.12
Nodes (8): Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Chiqindi qutisida barcha yangi ustunlar saqlanishini tekshirish., TestSQLiteManager

### Community 21 - "hash_password"
Cohesion: 0.06
Nodes (27): QLabel, QPushButton, Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash., AppsView, copy_file_to_windows_clipboard(), QFrame, QWidget, Yordamchi va Kommunal Dasturlar ekrani. (+19 more)

### Community 22 - "test_services.py"
Cohesion: 0.23
Nodes (10): clean_phone_number(), generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., vCard 3.0 formatida kontakt ma'lumotlarini shakllantirish., Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish. (+2 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.08
Nodes (31): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+23 more)

### Community 24 - "TestImportService"
Cohesion: 0.06
Nodes (27): Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, hex_to_rgba(), Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi). (+19 more)

### Community 25 - "clean_inn"
Cohesion: 0.05
Nodes (43): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+35 more)

### Community 26 - "sanitize_text"
Cohesion: 0.13
Nodes (22): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, get_stylesheet(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha     to'liq va mu (+14 more)

### Community 27 - "MainWindow"
Cohesion: 0.06
Nodes (19): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk). (+11 more)

### Community 28 - "TableView"
Cohesion: 0.10
Nodes (12): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish. (+4 more)

### Community 29 - "settings_view.py"
Cohesion: 0.40
Nodes (3): Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, validate_phone(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish.

### Community 30 - "telegram_bot.py"
Cohesion: 0.15
Nodes (8): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, open_broadcast_dialog(), ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5).

### Community 31 - "hash_password"
Cohesion: 0.21
Nodes (6): QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., Any, QDialog, QRDialog, QR kod tasvirini joriy rejim bo'yicha qayta chizish., Telefon raqami va tashkilot kontakti uchun professional QR-Kod Dialogi.

### Community 32 - "VerificationDialog"
Cohesion: 0.24
Nodes (9): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti, Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini (+1 more)

### Community 33 - ".__init__"
Cohesion: 0.33
Nodes (3): get_utility_path(), Yordamchi dastur fayli yo'lini topish (BASE_DIR yoki PyInstaller MEIPASS)., ui_qt.views.apps_view: Yordamchi va Kommunal Dasturlar (Utilities & Tools) Sahif

### Community 34 - "DataManager"
Cohesion: 0.18
Nodes (6): ImportDialog, open_batch_import_dialog(), Any, QDialog, Excel / CSV ommaviy import dialog oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 35 - "validate_inn"
Cohesion: 0.24
Nodes (12): Client, download_data_from_sheet(), get_gspread_client(), open_spreadsheet(), Any, Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali, ID, URL yoki nom orqali jadvalni ochish., Ma'lumotlar ro'yxatini Google Sheetga yuklash (to'liq 13 ta ustun bilan). (+4 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.13
Nodes (13): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish., Foydalanuvchi talabiga to'liq mos keluvchi verifikatsiya shablon matnini yaratis (+5 more)

### Community 37 - "CabinetDialog"
Cohesion: 0.11
Nodes (13): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., CabinetDialog, copy_cabinet_quick() (+5 more)

### Community 38 - "build_verification_text"
Cohesion: 0.06
Nodes (18): is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., Task 5: Avtomatlashtirilgan fonda davriy zaxira olish (Auto-Backup Scheduler)., Any, QWidget, Tizim sozlamalari ekrani., Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash. (+10 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.27
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Baza jadvallari va indekslarini yaratish., SQLiteManager, tests.test_features_12346: 1, 2, 3, 4, 6-topshiriqlar bo'yicha maxsus sinov test

### Community 40 - "OrgEditDialog"
Cohesion: 0.24
Nodes (9): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+1 more)

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.25
Nodes (4): Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi., TestFeatures12346

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.23
Nodes (6): HistoryView, open_staff_history_dialog(), Any, QDialog, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 47 - "TestDataManager"
Cohesion: 0.33
Nodes (6): QPixmap, create_crisp_pixmap(), Retina / 4K / High-DPI o'lchamli kristall tiniqlikdagi QPixmap yaratish.     Win, pil_to_qpixmap(), Image, PIL Image ob'ektini PyQt5 QPixmap tasviriga xotirada tezkor aylantirish.

### Community 49 - "is_service_account_available"
Cohesion: 0.67
Nodes (3): Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger

### Community 54 - ".trigger_manual_auto_backup"
Cohesion: 0.19
Nodes (9): format_phone(), Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val (+1 more)

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `clean_inn` to `External Services (Excel, QR, GSheets)`, `UI Views Test Suite`, `sync_contracts_data.py`, `pil_to_qpixmap`, `export_organizations_to_excel`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.207) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `extract_sheet_id`, `CabinetDialog`, `sync_contracts_data.py`, `pil_to_qpixmap`, `Services Package Architecture`, `test_services.py`, `clean_inn`, `sanitize_text`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Data Validation & Formatting`, `build_verification_text`, `settings_view.py`, `.test_07_dialogs_instantiation`, `Cloud Sync Verification`, `.add_organization`, `hash_password`, `TestImportService`, `clean_inn`, `sanitize_text`, `TableView`, `telegram_bot.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `TestQtArchitecture` (e.g. with `MainWindow` and `OrganizationTableModel`) actually correct?**
  _`TestQtArchitecture` has 22 INFERRED edges - model-reasoned connections that need verification._