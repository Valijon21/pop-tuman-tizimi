# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 66 files · ~104,760 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1065 nodes · 2177 edges · 61 communities (46 shown, 15 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 174 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `787f0827`
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
6. `ContractsView` - 39 edges
7. `SettingsView` - 36 edges
8. `WorkerThread` - 32 edges
9. `OrgEditDialog` - 31 edges
10. `SQLiteManager` - 30 edges

## Surprising Connections (you probably didn't know these)
- `TestServices` --uses--> `WorkerThread`  [INFERRED]
  tests/test_services.py → core/threading_utils.py
- `MainWindow` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/app_window.py → core/threading_utils.py
- `BroadcastView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/broadcast_view.py → core/threading_utils.py
- `CabinetDialog` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/cabinet_dialog.py → core/threading_utils.py
- `SettingsView` --uses--> `WorkerThread`  [INFERRED]
  ui_qt/views/settings_view.py → core/threading_utils.py

## Import Cycles
- None detected.

## Communities (61 total, 15 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Sing, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.15
Nodes (8): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, Test all dialogs for clean initialization, styles, and button bindings., OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.21
Nodes (8): DashboardView, Any, QWidget, PyQt5 Zamonaviy, Professional Dashboard Ekrani., Dashboard'ning barcha vidjetlarini (kartalar, diagrammalar, sarlavhalar), Statistika kartalarini, diagrammalarni va jadvalni to'ldirish., Senior-darajadagi zamonaviy, mukammal balanslangan KPI statistika kartasi., render_dashboard()

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (40): normalize_text(), Kirill yozuvidagi o'zbek matnini lotin yozuviga o'girish., Qidiruv uchun matnni to'liq normallashtirish (tutuq belgilari, kirill-lotin, ora, transliterate_to_latin(), get_role_priority(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Bot tokeni kiritilgan va sozlanganligini tekshirish. (+32 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.15
Nodes (15): clean_inn(), clean_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+7 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.15
Nodes (8): open_cabinet_dialog(), open_qr_dialog(), Any, Ilova oynasida QR dialogini xavfsiz ochish., Any, O'ng tugma bosilganda kontekst menyu., render_table(), open_verification_dialog()

### Community 6 - "UI Views Test Suite"
Cohesion: 0.19
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.13
Nodes (7): PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash., Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, TestQtArchitecture

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test TableView search, pill selection, category filters., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.10
Nodes (19): 1. 🔍 Aqlli Qidiruv va Avto-taklif Tizimi (Smart Search & Auto-complete), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Professional Tartiblangan Jadval), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 4. 📇 Kontakt QR-kod Standartlari (RFC & MeCard), 5. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti (+11 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.12
Nodes (11): extract_sheet_id(), URL yoki matndan Google Sheet ID sini ajratib olish., Any, Auto-complete takliflari uchun barcha unikal nomlar, INN va xodimlar ro'yxati., Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor, aqlli qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Lotin/Kirill transliteratsiya (+3 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.13
Nodes (11): Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Any, QWidget, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish. (+3 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.13
Nodes (11): ItemFlags, Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, Jadval ma'lumotlarini yangilash. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.12
Nodes (8): Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Chiqindi qutisida barcha yangi ustunlar saqlanishini tekshirish., TestSQLiteManager

### Community 21 - "hash_password"
Cohesion: 0.06
Nodes (26): QLabel, QLineEdit, QPushButton, AppsView, copy_file_to_windows_clipboard(), QFrame, QWidget, Yordamchi va Kommunal Dasturlar ekrani. (+18 more)

### Community 22 - "test_services.py"
Cohesion: 0.11
Nodes (16): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti, Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini (+8 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.08
Nodes (31): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+23 more)

### Community 24 - "TestImportService"
Cohesion: 0.05
Nodes (30): QTableWidgetItem, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi)., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish., ContractsView (+22 more)

### Community 25 - "clean_inn"
Cohesion: 0.15
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 26 - "sanitize_text"
Cohesion: 0.09
Nodes (27): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, attach_smart_completer(), ui_qt.components.smart_completer: Zamonaviy va Aqlli Qidiruv Auto-Complete (Takl, Ixtiyoriy QLineEdit maydoniga aqlli qidiruv auto-complete tizimini biriktirish. (+19 more)

### Community 27 - "MainWindow"
Cohesion: 0.07
Nodes (18): QMainWindow, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk)., Sozlamalar sahifasini ochish (773423321v paroli bilan himoyalangan). (+10 more)

### Community 28 - "TableView"
Cohesion: 0.16
Nodes (7): QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish., PyQt5 Tashkilotlar Jadvali Ekrani., TableView

### Community 29 - "settings_view.py"
Cohesion: 0.19
Nodes (9): format_phone(), Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val (+1 more)

### Community 30 - "telegram_bot.py"
Cohesion: 0.20
Nodes (6): MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi., Hozirgi mahalla pasportini rasmiy A4 PDF hujjat ko'rinishida eksport qilish.

### Community 31 - "hash_password"
Cohesion: 0.19
Nodes (6): QMouseEvent, QPaintEvent, QPoint, CategoryDonutChart, data: [(nomi, soni, rang_hex), ...], PyQt5 QPainter yordamida chiziladigan professional, 60 FPS Donut diagrammasi.

### Community 32 - "VerificationDialog"
Cohesion: 0.10
Nodes (11): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, ImportDialog, open_batch_import_dialog(), Any (+3 more)

### Community 34 - "DataManager"
Cohesion: 0.07
Nodes (25): Connection, Any, Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish. (+17 more)

### Community 35 - "validate_inn"
Cohesion: 0.24
Nodes (12): Client, download_data_from_sheet(), get_gspread_client(), open_spreadsheet(), Any, Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali, ID, URL yoki nom orqali jadvalni ochish., Ma'lumotlar ro'yxatini Google Sheetga yuklash (to'liq 13 ta ustun bilan). (+4 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.27
Nodes (9): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+1 more)

### Community 37 - "CabinetDialog"
Cohesion: 0.23
Nodes (5): CabinetDialog, Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Kabinetga dostup shablon oynasi.

### Community 38 - "build_verification_text"
Cohesion: 0.06
Nodes (18): is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., Task 5: Avtomatlashtirilgan fonda davriy zaxira olish (Auto-Backup Scheduler)., Any, QWidget, Tizim sozlamalari ekrani., Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash. (+10 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.16
Nodes (10): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Aqlli tokenli moslash: barcha so'zlar nishon ichida uchrashini tekshiradi. (+2 more)

### Community 40 - "OrgEditDialog"
Cohesion: 0.20
Nodes (15): clean_phone_number(), generate_mecard_data(), generate_mecard_qr_image(), generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Mobil kontakt (MeCard) uchun toza QR-kod tasvirini yaratish. (+7 more)

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.21
Nodes (10): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+2 more)

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.06
Nodes (31): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+23 more)

### Community 48 - "Any"
Cohesion: 0.20
Nodes (8): QPixmap, pil_to_qpixmap(), Image, QDialog, QRDialog, QR kod tasvirini joriy rejim bo'yicha qayta chizish., PIL Image ob'ektini PyQt5 QPixmap tasviriga xotirada tezkor aylantirish., Telefon raqami va tashkilot kontakti uchun professional QR-Kod Dialogi.

### Community 49 - "is_service_account_available"
Cohesion: 0.17
Nodes (7): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, CategoryBarChart, CategoryLegend, QFrame, QWidget, Donut diagramma yonidagi interaktiv, foizli va rangli tushuntirish paneli (Legen, Toifalar taqsimotini solishtirish uchun zamonaviy gorizontal progress bar diagra

### Community 50 - ".add_organization"
Cohesion: 0.21
Nodes (5): Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 52 - ".save_all_organizations"
Cohesion: 0.22
Nodes (7): QCompleter, get_completer_popup_style(), Auto-complete popapining Fluent UI uslubidagi stylesheeti., Senior darajadagi aqlli qidiruv takliflari (Auto-complete) klassi., Mavzuni yangilash (Dark / Light)., Takliflar ro'yxatini tezkor yangilash., SmartSearchCompleter

### Community 53 - ".send_welcome"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 54 - "setup_logger"
Cohesion: 0.67
Nodes (3): Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger

### Community 55 - ".backup_data"
Cohesion: 0.20
Nodes (6): ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, copy_cabinet_quick(), Oynani ochmasdan tezkor nusxalash., ui_qt.views.table_view: Asosiy tashkilotlar jadvali (Table View) (PyQt5). Senior, copy_verification_quick(), Oynani ochmasdan tezkor nusxalash.

### Community 56 - ".get_organization_by_id"
Cohesion: 0.25
Nodes (3): QModelIndex, Jadvalda klaviatura hodisalarini ushlash: Enter, Delete, Ctrl+C., Tanlangan katak(lar) yoki ko'kartirib belgilangan matnlarni buferga nusxalash (C

### Community 57 - ".get_organization_by_inn"
Cohesion: 0.29
Nodes (3): QStyledItemDelegate, IzohDelegate, Izoh ustuni uchun maxsus zamonaviy inline muharrir (QLineEdit).

### Community 58 - ".get_recent_activity"
Cohesion: 0.40
Nodes (3): Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, validate_phone(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish.

## Knowledge Gaps
- **18 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🔍 Aqlli Qidiruv va Avto-taklif Tizimi (Smart Search & Auto-complete)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Professional Tartiblangan Jadval)`, `3. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `export_organizations_to_excel` to `DataManager`, `External Services (Excel, QR, GSheets)`, `UI Views Test Suite`, `sync_contracts_data.py`, `BroadcastView`, `clean_inn`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `VerificationDialog`, `Core Configuration & Logging`, `Data Validation & Formatting`, `UI App Core & Event Handlers`, `build_verification_text`, `SQLiteManager`, `settings_view.py`, `.test_07_dialogs_instantiation`, `export_organizations_to_excel`, `Cloud Sync Verification`, `is_service_account_available`, `hash_password`, `TestImportService`, `sanitize_text`, `broadcast_service.py`, `TableView`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `DataManager`, `CabinetDialog`, `sync_contracts_data.py`, `OrgEditDialog`, `export_organizations_to_excel`, `Services Package Architecture`, `.add_organization`, `test_services.py`, `sanitize_text`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._