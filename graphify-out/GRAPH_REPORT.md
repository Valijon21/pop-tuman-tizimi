# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 64 files · ~88,183 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 971 nodes · 1969 edges · 68 communities (44 shown, 24 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 136 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `44f5bfd8`
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
- .open_edit_dialog
- .on_auto_backup_toggled
- .update_last_backup_display
- .insert_or_replace_organization
- export_organizations_to_excel
- .closeEvent
- setup_logger
- .test_task5_auto_backup_scheduler
- render_settings
- .on_backup_interval_changed
- .update_edit_password
- .focus_search

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 54 edges
2. `TelegramBotService` - 48 edges
3. `DataManager` - 41 edges
4. `TableView` - 40 edges
5. `TestQtArchitecture` - 38 edges
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

## Communities (68 total, 24 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.16
Nodes (13): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, get_telegram_bot_service(), TelegramBotService uchun yagona namuna (Singleton) olish. (+5 more)

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.11
Nodes (15): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti, Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini (+7 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.13
Nodes (11): CategoryBarChart, CategoryLegend, ClickableCard, QWidget, ui_qt.components.widgets: Yuqori sifatli (Senior-Grade) maxsus Qt komponentlari., Tugma (QPushButton) cheklovlarisiz, matnlarni siqib qo'ymaydigan     va to'liq d, Donut diagramma yonidagi interaktiv, foizli va rangli tushuntirish paneli (Legen, Toifalar taqsimotini solishtirish uchun zamonaviy gorizontal progress bar diagra (+3 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (38): normalize_text(), Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)., get_role_priority(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash., Qidiruv so'zi (INN, nom yoki F.I.SH) bo'yicha aniq tashkilotni O(1) topish. (+30 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.16
Nodes (13): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+5 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.17
Nodes (8): import_organizations_from_file(), Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService, ui_qt.views.import_dialog: Excel va CSV fayllardan ommaviy import qilish dialogi

### Community 6 - "UI Views Test Suite"
Cohesion: 0.13
Nodes (9): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Ma'lumotlar ombori boshqaruvi va atomik saqlash testlari (Isolated)., TestDataManager, Organization ma'lumotlar modeli testlari. (+1 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.12
Nodes (13): Connection, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish., Chiqindi elementini ID si bo'yicha SQLite bazasidan butunlay o'chirish., SQLite ulanishini olish va WAL rejimini faollashtirish., Chiqindi qutisini to'liq saqlash., Baza jadvallari va indekslarini yaratish., Xodim rotatsiyasi/almashinuvini tarix jadvaliga qo'shish (ko'p qirrali parametrl (+5 more)

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., Test TableView search, pill selection, category filters., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.16
Nodes (8): Any, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, SearchService, Qidiruv, QR va Excel xizmatlari testlari., TestServices

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.14
Nodes (11): Any, QWidget, ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5). O'chiril, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish. (+3 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.12
Nodes (11): Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel, Any, QModelIndex, ui_qt.components.table_model: Yuqori unumdorlikka ega QAbstractTableModel. 60 FP, Tanlangan qator bo'yicha tashkilot obyektini olish. (+3 more)

### Community 17 - "Organization"
Cohesion: 0.14
Nodes (11): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, TestQtArchitecture, PasswordPromptDialog, Any, QDialog, Parolni ko'rsatish yoki yashirish. (+3 more)

### Community 21 - "hash_password"
Cohesion: 0.13
Nodes (12): copy_cabinet_quick(), open_cabinet_dialog(), Oynani ochmasdan tezkor nusxalash., open_qr_dialog(), Ilova oynasida QR dialogini xavfsiz ochish., Any, ui_qt.views.table_view: Asosiy tashkilotlar jadvali (Table View) (PyQt5). Senior, O'ng tugma bosilganda kontekst menyu. (+4 more)

### Community 22 - "test_services.py"
Cohesion: 0.14
Nodes (17): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+9 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.07
Nodes (38): Client, authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish. (+30 more)

### Community 24 - "TestImportService"
Cohesion: 0.05
Nodes (29): QLabel, Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Forma label yaratish (mavzuga mos rang bilan). (+21 more)

### Community 25 - "clean_inn"
Cohesion: 0.05
Nodes (43): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+35 more)

### Community 26 - "sanitize_text"
Cohesion: 0.15
Nodes (13): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, get_stylesheet(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha     to'liq va mu, ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5). (+5 more)

### Community 27 - "MainWindow"
Cohesion: 0.07
Nodes (17): QMainWindow, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Sozlamalar sahifasini ochish (773423321v paroli bilan himoyalangan)., Yangi tashkilot qo'shish (1234567 paroli bilan himoyalangan). (+9 more)

### Community 28 - "TableView"
Cohesion: 0.18
Nodes (6): QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish., PyQt5 Tashkilotlar Jadvali Ekrani., TableView

### Community 29 - "settings_view.py"
Cohesion: 0.25
Nodes (5): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish.

### Community 30 - "telegram_bot.py"
Cohesion: 0.17
Nodes (7): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread, is_service_account_available(), Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish.

### Community 31 - "hash_password"
Cohesion: 0.15
Nodes (10): QPixmap, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., pil_to_qpixmap(), Any, Image, QDialog, QRDialog, QR kod tasvirini joriy rejim bo'yicha qayta chizish. (+2 more)

### Community 32 - "VerificationDialog"
Cohesion: 0.27
Nodes (9): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+1 more)

### Community 34 - "DataManager"
Cohesion: 0.17
Nodes (5): Test all dialogs for clean initialization, styles, and button bindings., ImportDialog, QDialog, Excel / CSV ommaviy import dialog oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 35 - "validate_inn"
Cohesion: 0.25
Nodes (4): Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., Task 3: Telegram bot sessiya boshqaruvi va avto-yangilanishi., TestFeatures12346

### Community 36 - "extract_sheet_id"
Cohesion: 0.21
Nodes (5): Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 37 - "CabinetDialog"
Cohesion: 0.21
Nodes (5): CabinetDialog, Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Kabinetga dostup shablon oynasi.

### Community 38 - "build_verification_text"
Cohesion: 0.20
Nodes (4): QWidget, Tizim sozlamalari ekrani., MainWindow dan chaqiriladigan oxirgi zaxira vaqti ko'rsatkichi., SettingsView

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.19
Nodes (7): QFrame, MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi., Hozirgi mahalla pasportini rasmiy A4 PDF hujjat ko'rinishida eksport qilish.

### Community 40 - "OrgEditDialog"
Cohesion: 0.18
Nodes (7): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.19
Nodes (9): Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, DashboardView, Any, QWidget, PyQt5 Zamonaviy, Professional Dashboard Ekrani., Dashboard'ning barcha vidjetlarini (kartalar, diagrammalar, sarlavhalar), Statistika kartalarini, diagrammalarni va jadvalni to'ldirish., Senior-darajadagi zamonaviy, mukammal balanslangan KPI statistika kartasi. (+1 more)

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.20
Nodes (7): HistoryView, open_staff_history_dialog(), Any, QDialog, ui_qt.views.history_view: Kadrlar almashinuvi va rotatsiyasi tarixi dialogi (PyQ, SQLite dan tarix yozuvlarini yuklash., Kadrlar tarixi dialog oynasi.

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.12
Nodes (8): Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Chiqindi qutisida barcha yangi ustunlar saqlanishini tekshirish., TestSQLiteManager

### Community 47 - "TestDataManager"
Cohesion: 0.14
Nodes (8): Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (buzilm, Ommaviy tashkilotlarni saqlash va sonini qaytarish., Tashkilotni unikal ID si bo'yicha olish., Tashkilotni INN si bo'yicha olish., Chiqindi qutisidagi barcha yozuvlarni olish., So'nggi faoliyat jurnallarini olish.

### Community 48 - "Any"
Cohesion: 0.19
Nodes (6): QMouseEvent, QPaintEvent, QPoint, CategoryDonutChart, data: [(nomi, soni, rang_hex), ...], PyQt5 QPainter yordamida chiziladigan professional, 60 FPS Donut diagrammasi.

### Community 51 - "BroadcastView"
Cohesion: 0.20
Nodes (8): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service

### Community 55 - ".add_staff_history"
Cohesion: 0.33
Nodes (4): generate_phone_qr_image(), Image, Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., QR-kod rasmini PNG fayl qilib saqlash.

### Community 58 - ".update_last_backup_display"
Cohesion: 0.40
Nodes (3): Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, validate_passport_series(), Ma'lumotlarni validatsiya qilish va saqlash.

### Community 60 - "export_organizations_to_excel"
Cohesion: 0.50
Nodes (3): export_organizations_to_excel(), Any, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash.

### Community 62 - "setup_logger"
Cohesion: 0.67
Nodes (3): Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Logger

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `clean_inn` to `UI App Core & Event Handlers`, `.__init__`, `External Services (Excel, QR, GSheets)`, `validate_inn`, `UI Views Test Suite`, `SQLiteManager`, `BroadcastView`, `MainWindow`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `UI App Core & Event Handlers`, `.__init__`, `VerificationDialog`, `validate_inn`, `extract_sheet_id`, `CabinetDialog`, `Services Package Architecture`, `BroadcastView`, `clean_inn`, `sanitize_text`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `UI App Core & Event Handlers`, `Core Configuration & Logging`, `build_verification_text`, `settings_view.py`, `pil_to_qpixmap`, `.test_07_dialogs_instantiation`, `OrgEditDialog`, `Cloud Sync Verification`, `Organization`, `.add_organization`, `TestImportService`, `clean_inn`, `sanitize_text`, `TableView`, `.closeEvent`, `telegram_bot.py`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `DataManager` (e.g. with `Organization` and `SQLiteManager`) actually correct?**
  _`DataManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 7 INFERRED edges - model-reasoned connections that need verification._