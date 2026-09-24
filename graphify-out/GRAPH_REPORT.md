# Graph Report - tashkilotlar INN tizim  (2026-09-24)

## Corpus Check
- 63 files · ~70,677 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 918 nodes · 1859 edges · 65 communities (48 shown, 17 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `48570ca1`
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
- Any
- QLabel
- BroadcastView
- SQLiteManager
- Any
- .save_data
- .__init__
- ._create_kpi_card
- .add_organization
- .insert_or_replace_organization
- pil_to_qpixmap
- extract_sheet_id
- open_mahalla_passport
- .get_organization_by_id
- .get_organization_by_inn
- .get_recent_activity

## God Nodes (most connected - your core abstractions)
1. `TelegramBotService` - 48 edges
2. `MainWindow` - 48 edges
3. `DataManager` - 41 edges
4. `TableView` - 40 edges
5. `TestQtArchitecture` - 36 edges
6. `ContractsView` - 36 edges
7. `SQLiteManager` - 30 edges
8. `WorkerThread` - 28 edges
9. `OrgEditDialog` - 28 edges
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

## Communities (65 total, 17 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI va Yagona Nusxa / Single Instance himo, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.24
Nodes (9): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti, Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini (+1 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (24): QMouseEvent, QPaintEvent, QPoint, Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, CategoryBarChart, CategoryDonutChart, CategoryLegend, ClickableCard (+16 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (42): normalize_text(), Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), get_telegram_bot_service(), Any, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish. (+34 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.15
Nodes (14): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+6 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.22
Nodes (6): CabinetDialog, open_cabinet_dialog(), Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Kabinetga dostup shablon oynasi.

### Community 6 - "UI Views Test Suite"
Cohesion: 0.16
Nodes (9): Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari. (+1 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.12
Nodes (8): Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Chiqindi qutisida barcha yangi ustunlar saqlanishini tekshirish., TestSQLiteManager

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., Test TableView search, pill selection, category filters., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.15
Nodes (8): Any, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, SearchService, Qidiruv, QR va Excel xizmatlari testlari., TestServices

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.13
Nodes (11): Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Any, QWidget, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish. (+3 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.14
Nodes (12): Any, core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, copy_cabinet_quick(), ui_qt.views.cabinet_dialog: 'Kabinetga dostup' shablonini generatsiya qilish, bi (+4 more)

### Community 21 - "hash_password"
Cohesion: 0.19
Nodes (7): QFrame, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., Any, QDialog, QRDialog, QR kod tasvirini joriy rejim bo'yicha qayta chizish., Telefon raqami va tashkilot kontakti uchun professional QR-Kod Dialogi.

### Community 22 - "test_services.py"
Cohesion: 0.24
Nodes (8): generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., vCard 3.0 formatida kontakt ma'lumotlarini shakllantirish., Raqamli tashrif qog'ozi (vCard) uchun xotirada toza QR-kod tasvirini yaratish., QR-kod rasmini PNG fayl qilib saqlash.

### Community 23 - "import_organizations_from_file"
Cohesion: 0.14
Nodes (19): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+11 more)

### Community 24 - "TestImportService"
Cohesion: 0.10
Nodes (15): ContractsView, QWidget, Mavzuni Dark / Light rejimiga moslashtirish., Shartnoma va Ulanishlar Monitoringi Sahifasi., Ctrl+F bosilganda qidiruv maydoniga o'tish., 250ms Debounce bilan qidiruv., Jadvalda klaviatura hodisalari: Enter (tahrir)., Bazada mavjud bo'lgan shartnoma ma'lumotlarini yuklash. (+7 more)

### Community 25 - "clean_inn"
Cohesion: 0.16
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 26 - "sanitize_text"
Cohesion: 0.13
Nodes (17): Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., get_stylesheet(), hex_to_rgba(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Hex rang kodini (#rrggbb) to'g'ri Qt CSS rgba(r, g, b, alpha) formatiga o'tkazad, Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha     to'liq va mu, ui_qt.views.contract_add_dialog: Shartnoma va Ulanish ma'lumotini qo'shish/tahri (+9 more)

### Community 27 - "MainWindow"
Cohesion: 0.09
Nodes (12): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., QR-kod oynasini ochish., Telegram botni fon rejimida (asinxron) ishga tushirish. (+4 more)

### Community 28 - "TableView"
Cohesion: 0.10
Nodes (12): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Jadvalda klaviatura hodisalarini ushlash: Enter (tahrir), Delete (o'chirish)., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish. (+4 more)

### Community 29 - "settings_view.py"
Cohesion: 0.16
Nodes (16): Client, Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger, download_data_from_sheet(), get_gspread_client(), open_spreadsheet() (+8 more)

### Community 30 - "telegram_bot.py"
Cohesion: 0.25
Nodes (6): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish.

### Community 31 - "hash_password"
Cohesion: 0.33
Nodes (4): HistoryView, QDialog, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 32 - "VerificationDialog"
Cohesion: 0.19
Nodes (6): Test all dialogs for clean initialization, styles, and button bindings., Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 33 - ".__init__"
Cohesion: 0.20
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, open_broadcast_dialog(), ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5)., ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5). O'chiril

### Community 34 - "DataManager"
Cohesion: 0.20
Nodes (5): ImportDialog, open_batch_import_dialog(), Any, QDialog, Excel / CSV ommaviy import dialog oynasi.

### Community 35 - "validate_inn"
Cohesion: 0.12
Nodes (12): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., CSV fayldan tashkilotlarni aniqlash va import qilish. (+4 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.24
Nodes (9): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+1 more)

### Community 37 - "telegram_bot.py"
Cohesion: 0.14
Nodes (8): DataManager, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Xodim rotatsiyasi/almashinuvini qayd etish., Ma'lumotlar bazasining zaxira nusxasini yaratish (oxirgi 10 ta nusxa)., Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi., TestFeatures12346

### Community 38 - "build_verification_text"
Cohesion: 0.10
Nodes (10): is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish., Any, QWidget, Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Mavjud sozlamalarni yuklash., Tizim sozlamalari ekrani., Telegram botni qo'lda qayta ishga tushirish. (+2 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.20
Nodes (6): MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi., Hozirgi mahalla pasportini rasmiy A4 PDF hujjat ko'rinishida eksport qilish.

### Community 40 - "OrgEditDialog"
Cohesion: 0.12
Nodes (11): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, TestQtArchitecture, OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash. (+3 more)

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.23
Nodes (10): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis. (+2 more)

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.29
Nodes (4): O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., Ma'lumotlarni validatsiya qilish va saqlash.

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.19
Nodes (12): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+4 more)

### Community 48 - "clean_inn"
Cohesion: 0.15
Nodes (7): Connection, Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., SQLite ulanishini olish va WAL rejimini faollashtirish., Xodim rotatsiyasi/almashinuvini tarix jadvaliga qo'shish (ko'p qirrali parametrl, Tizimdagi harakatni SQLite jurnaliga qayd etish., Agar SQLite jadvali bo'sh bo'lsa, JSON fayldan barcha yozuvlarni avtomatik ko'ch, SQLite bazasini vaqt tamg'asi bilan zaxiralash.

### Community 49 - "Any"
Cohesion: 0.17
Nodes (7): Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, Ommaviy tashkilotlarni saqlash va sonini qaytarish., Chiqindi qutisidagi barcha yozuvlarni olish., Chiqindi qutisini to'liq saqlash., Xodimlar tarixini olish (tashkilot yoki mahalla bo'yicha).

### Community 50 - "QLabel"
Cohesion: 0.21
Nodes (8): QLabel, Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Forma label yaratish (mavzuga mos rang bilan)., Mavjud ma'lumotlarni formaga yuklash (tahrirlash rejimi).

### Community 51 - "BroadcastView"
Cohesion: 0.21
Nodes (5): BroadcastView, Any, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi.

### Community 52 - "SQLiteManager"
Cohesion: 0.24
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Baza jadvallari va indekslarini yaratish., SQLiteManager

### Community 53 - "Any"
Cohesion: 0.25
Nodes (5): Any, Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Tashkilotni Organization dataclass modeli sifatida olish., Xodimlar rotatsiyasi tarixini olish.

### Community 54 - ".save_data"
Cohesion: 0.29
Nodes (3): Yozuvni Chiqindi qutisiga ko'chirish., Chiqindi qutisidan asosiy bazaga tiklash., Chiqindi qutisidan butunlay o'chirish.

### Community 56 - "._create_kpi_card"
Cohesion: 0.29
Nodes (3): Any, Senior-darajadagi muvozanatli 2x2 KPI statistika kartochkasi., O'ng tugma kontekst menyusi.

### Community 57 - ".add_organization"
Cohesion: 0.40
Nodes (3): Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi)., Mavjud tashkilot ma'lumotlarini yangilash (dict yoki Organization modeli qabul q, Tizimdagi harakatlarni qayd etish (JSON + SQLite).

### Community 59 - "pil_to_qpixmap"
Cohesion: 0.50
Nodes (4): QPixmap, pil_to_qpixmap(), Image, PIL Image ob'ektini PyQt5 QPixmap tasviriga xotirada tezkor aylantirish.

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `telegram_bot.py` to `.__init__`, `External Services (Excel, QR, GSheets)`, `UI Views Test Suite`, `pil_to_qpixmap`, `export_organizations_to_excel`, `TestDataManager`, `import_organizations_from_file`, `Any`, `.save_data`, `.__init__`, `SQLiteManager`, `.add_organization`, `MainWindow`, `clean_inn`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `VerificationDialog`, `telegram_bot.py`, `import_organizations_from_file`, `export_organizations_to_excel`, `Services Package Architecture`, `Organization`, `test_services.py`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `.get_recent_activity`, `telegram_bot.py`, `SQLiteManager`, `export_organizations_to_excel`, `clean_inn`, `Any`, `import_organizations_from_file`, `.__init__`, `.insert_or_replace_organization`, `.get_organization_by_id`, `.get_organization_by_inn`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._