# Graph Report - tashkilotlar INN tizim  (2026-09-23)

## Corpus Check
- 74 files · ~68,830 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 850 nodes · 1635 edges · 44 communities (28 shown, 16 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `50ca2b04`
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
- UI Package Architecture
- UI Views Package Architecture
- rules/graphify.md
- workflows/graphify.md
- hash_password
- TelegramBotService
- import_organizations_from_file
- TestImportService
- clean_inn
- sanitize_text
- MainWindow
- TableView
- TestQtArchitecture
- test_views.py
- hash_password
- MahallaPassportView
- TrashView
- CabinetDialog
- .add_staff_history
- app.py
- sync_contracts_data.py
- components/__init__.py
- ui_qt/__init__.py
- ui_qt/views/__init__.py
- TestImportService
- validate_inn
- TestDataManager

## God Nodes (most connected - your core abstractions)
1. `MahallaDasturi` - 56 edges
2. `MainWindow` - 41 edges
3. `TableView` - 34 edges
4. `DataManager` - 33 edges
5. `TestQtArchitecture` - 31 edges
6. `SQLiteManager` - 27 edges
7. `TelegramBotService` - 27 edges
8. `ContractsView` - 24 edges
9. `build_verification_text()` - 22 edges
10. `OrgEditDialog` - 22 edges

## Surprising Connections (you probably didn't know these)
- `ContractsSyncService` --uses--> `DataManager`  [INFERRED]
  services/sync_contracts_data.py → database/data_manager.py
- `ExcelSyncService` --uses--> `DataManager`  [INFERRED]
  services/sync_excel_data.py → database/data_manager.py
- `TestDataManager` --uses--> `DataManager`  [INFERRED]
  tests/test_data_manager.py → database/data_manager.py
- `MahallaDasturi` --uses--> `DataManager`  [INFERRED]
  ui/app.py → database/data_manager.py
- `MainWindow` --uses--> `DataManager`  [INFERRED]
  ui_qt/app_window.py → database/data_manager.py

## Import Cycles
- None detected.

## Communities (44 total, 16 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.11
Nodes (6): MahallaDasturi, CTk, Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)., Verifikatsiya so'rovi dialogini ochish., Tezkor verifikatsiya matnini clipboardga nusxalash., Dastur yopilayotganda avtomatik zaxira olish.

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.16
Nodes (14): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+6 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (29): QMouseEvent, QPaintEvent, QPoint, tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., TestQtArchitecture, CategoryBarChart, CategoryDonutChart (+21 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.13
Nodes (11): normalize_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari). (+3 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.16
Nodes (11): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Tizimdagi harakatlarni qayd etish (JSON + SQLite)., Xodimlar rotatsiyasi tarixini olish. (+3 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.18
Nodes (12): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin, validate_jshshir() (+4 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.05
Nodes (30): Connection, Any, Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan to'liq saqlash/yangilash., SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Bitta tashkilotni qo'shish yoki yangilash., Bitta tashkilotni qo'shish yoki yangilash (Alias). (+22 more)

### Community 8 - "Toast Notification System"
Cohesion: 0.28
Nodes (6): CTk, Pop Tuman Tashkilotlari va INN Tizimi Zamonaviy Toast / Banner Bildirishnomalar, Qulay yordamchi funksiya., Oynaning pastki qismida silliq paydo bo'lib yo'qoluvchi bildirishnoma., show_toast(), ToastNotification

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.11
Nodes (18): 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition), 1. Repozitoriyni klonlash, 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi), 2. Virtual muhit yaratish va kutubxonalarni o'rnatish, 3. Dasturni ishga tushirish, 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti, 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati), 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi (+10 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.06
Nodes (58): CTkFrame, Image, build_cabinet_access_text(), get_cabinet_portal_url(), Any, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar. (+50 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.15
Nodes (7): Any, QWidget, Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Tizim sozlamalari ekrani., Mavjud sozlamalarni yuklash., render_settings(), SettingsView

### Community 22 - "TelegramBotService"
Cohesion: 0.05
Nodes (25): Orientation, QAbstractTableModel, Any, Telegramdan yangi xabarlarni tinglash sikli (Long polling)., Telegram Bot orqali tashkilotlar bazasini qidirish, verifikatsiya va ommaviy xab, Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash., Yangi foydalanuvchini obunachilar ro'yxatiga qo'shish., Botni fon rejimida ishga tushirish. (+17 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.07
Nodes (33): Client, authenticate_user(), hash_password(), Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish., Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash., Parolni SHA-256 xeshga aylantirish., verify_password(), download_data_from_sheet() (+25 more)

### Community 24 - "TestImportService"
Cohesion: 0.11
Nodes (13): ContractsView, Any, QFrame, QWidget, KPI statistika kartochkasini yaratish., Mavzuni Dark / Light rejimiga moslashtirish., Shartnoma va Ulanishlar Monitoringi Sahifasi., Bazada mavjud bo'lgan shartnoma ma'lumotlarini yuklash. (+5 more)

### Community 25 - "clean_inn"
Cohesion: 0.15
Nodes (16): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, services.sync_excel_data: Excel (data.xlsx) faylidagi ma'lumotlarni bazaga (SQLi, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash. (+8 more)

### Community 26 - "sanitize_text"
Cohesion: 0.05
Nodes (42): install_global_exception_handler(), Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, setup_logger(), Logger, Pop Tuman Tashkilotlari va INN Tizimi Eski ishga tushirish fayli bilan 100% orqa, main() (+34 more)

### Community 27 - "MainWindow"
Cohesion: 0.07
Nodes (16): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Status bar orqali chiroyli xabar chiqarish., Dastur yopilayotganda avtomatik zaxira nusxa yaratish., Pop Tuman Tizimining Asosiy PyQt5 Oynasi. (+8 more)

### Community 28 - "TableView"
Cohesion: 0.13
Nodes (9): Any, QModelIndex, QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish., PyQt5 Tashkilotlar Jadvali Ekrani., O'ng tugma bosilganda kontekst menyu., render_table() (+1 more)

### Community 29 - "TestQtArchitecture"
Cohesion: 0.27
Nodes (3): Sessiya yoki parol kiritish orqali ruxsatni tekshirish., DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish., Google Sheets bilan fonda sinxronlash (Thread-Safe).

### Community 30 - "test_views.py"
Cohesion: 0.25
Nodes (5): Kadrlar almashinuvi va rotatsiya tarixi oynasini ochish., open_staff_history_dialog(), Any, Pop Tuman Tashkilotlari va INN Tizimi Xodimlar Rotatsiyasi va Kadrlar Tarixi Ko', Xodimlar almashinuvi tarixi dialog oynasi.

### Community 31 - "hash_password"
Cohesion: 0.06
Nodes (22): Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, BroadcastView, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi., HistoryView, QDialog, Kadrlar tarixi dialog oynasi. (+14 more)

### Community 32 - "MahallaPassportView"
Cohesion: 0.29
Nodes (3): Mahalla 'Yettiligi' 360° Pasport oynasini ochish., Excel/CSV ommaviy import dialogini ochish., Ommaviy xabarnoma (SMS & Telegram) dialogini ochish.

### Community 33 - "TrashView"
Cohesion: 0.15
Nodes (10): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., Tashkilot ma'lumotlar modeli va validatsiyasi. (+2 more)

### Community 36 - "app.py"
Cohesion: 0.14
Nodes (11): Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., open_batch_import_dialog() (+3 more)

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.23
Nodes (10): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis. (+2 more)

### Community 47 - "TestImportService"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 50 - "validate_inn"
Cohesion: 0.24
Nodes (7): Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), validate_passport_series(), Ma'lumotlarni validatsiya qilish va saqlash., open_record_dialog(), Tashkilot qo'shish yoki tahrirlash dialogi.

## Knowledge Gaps
- **17 isolated node(s):** `graphify`, `Workflow: graphify`, `1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)`, `2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)`, `3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `Data Persistence & Backup Manager` to `UI App Core & Event Handlers`, `.add_staff_history`, `SQLiteManager`, `sync_contracts_data.py`, `TestDataManager`, `import_organizations_from_file`, `clean_inn`, `sanitize_text`, `MainWindow`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `MahallaDasturi` connect `UI App Core & Event Handlers` to `MahallaPassportView`, `CabinetDialog`, `External Services (Excel, QR, GSheets)`, `Data Persistence & Backup Manager`, `import_organizations_from_file`, `app.py`, `hash_password`, `import_organizations_from_file`, `sanitize_text`, `TestQtArchitecture`, `test_views.py`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `Data Persistence & Backup Manager`, `import_organizations_from_file`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MahallaDasturi` (e.g. with `TestViewImports` and `.test_app_import()`) actually correct?**
  _`MahallaDasturi` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `DataManager` (e.g. with `SQLiteManager` and `ContractsSyncService`) actually correct?**
  _`DataManager` has 6 INFERRED edges - model-reasoned connections that need verification._