# Graph Report - tashkilotlar INN tizim  (2026-09-23)

## Corpus Check
- 71 files · ~54,062 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 726 nodes · 1379 edges · 46 communities (34 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e026e7c9`
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
- SettingsView
- hash_password
- MahallaPassportView
- TrashView
- CabinetDialog
- open_record_dialog
- app.py
- .test_view_imports
- VerificationDialog
- ImportDialog
- OrgEditDialog
- test_views.py
- render_settings
- components/__init__.py
- ui_qt/__init__.py
- ui_qt/views/__init__.py

## God Nodes (most connected - your core abstractions)
1. `MahallaDasturi` - 56 edges
2. `MainWindow` - 36 edges
3. `TableView` - 32 edges
4. `DataManager` - 27 edges
5. `SQLiteManager` - 27 edges
6. `build_verification_text()` - 22 edges
7. `TelegramBotService` - 21 edges
8. `TestQtArchitecture` - 21 edges
9. `OrgEditDialog` - 20 edges
10. `SettingsView` - 19 edges

## Surprising Connections (you probably didn't know these)
- `MahallaDasturi` --uses--> `DataManager`  [INFERRED]
  ui/app.py → database/data_manager.py
- `MainWindow` --uses--> `DataManager`  [INFERRED]
  ui_qt/app_window.py → database/data_manager.py
- `MahallaDasturi` --uses--> `SearchService`  [INFERRED]
  ui/app.py → services/search_service.py
- `TableView` --uses--> `SearchService`  [INFERRED]
  ui_qt/views/table_view.py → services/search_service.py
- `TestServices` --uses--> `TelegramBotService`  [INFERRED]
  tests/test_services.py → services/telegram_bot.py

## Import Cycles
- None detected.

## Communities (46 total, 12 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.06
Nodes (17): MahallaDasturi, Any, CTk, Sessiya yoki parol kiritish orqali ruxsatni tekshirish., Tungi va kunduzgi rejimni almashtirish., Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)., Foydalanuvchiga silliq va xalaqit bermaydigan Toast bildirishnomasi., DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish. (+9 more)

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.11
Nodes (18): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+10 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.19
Nodes (11): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text() (+3 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.13
Nodes (11): normalize_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari). (+3 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.10
Nodes (15): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Tizimdagi harakatlarni qayd etish (JSON + SQLite)., Xodim rotatsiyasi/almashinuvini qayd etish. (+7 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.21
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.05
Nodes (30): Connection, Any, Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan to'liq saqlash/yangilash., Bitta tashkilotni qo'shish yoki yangilash., SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Bitta tashkilotni qo'shish yoki yangilash (Alias). (+22 more)

### Community 8 - "Toast Notification System"
Cohesion: 0.28
Nodes (6): CTk, Pop Tuman Tashkilotlari va INN Tizimi Zamonaviy Toast / Banner Bildirishnomalar, Qulay yordamchi funksiya., Oynaning pastki qismida silliq paydo bo'lib yo'qoluvchi bildirishnoma., show_toast(), ToastNotification

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.15
Nodes (12): 1-qadam. Loyihani yuklab olish, 2-qadam. Kerakli kutubxonalarni o'rnatish, 3-qadam. Dasturni ishga tushirish, 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish, 🔑 Kalit Fayllar va Sozlamalar, 📁 Loyiha Tuzilmasi, 📞 Muallif va Ruxsatnoma, 📦 Mustaqil Windows `.exe` Dasturini Yig'ish (+4 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.06
Nodes (59): CTkFrame, Image, build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish. (+51 more)

### Community 21 - "hash_password"
Cohesion: 0.20
Nodes (13): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish., Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali (+5 more)

### Community 22 - "TelegramBotService"
Cohesion: 0.06
Nodes (20): Orientation, QAbstractTableModel, Any, Telegramdan yangi xabarlarni tinglash sikli (Long polling)., Telegram Bot orqali tashkilotlar bazasini qidirish, verifikatsiya va ommaviy xab, Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash., Yangi foydalanuvchini obunachilar ro'yxatiga qo'shish., Botni fon rejimida ishga tushirish. (+12 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.15
Nodes (10): export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., ui_qt.views.import_dialog: Excel va CSV fayllardan ommaviy import qilish dialogi, open_batch_import_dialog(), Any (+2 more)

### Community 24 - "TestImportService"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 25 - "clean_inn"
Cohesion: 0.22
Nodes (6): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., ui_qt.views.org_edit_dialog: Tashkilot qo'shish va tahrirlash dialogi. Maydonlar

### Community 26 - "sanitize_text"
Cohesion: 0.07
Nodes (29): install_global_exception_handler(), Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, setup_logger(), Logger, Pop Tuman Tashkilotlari va INN Tizimi Eski ishga tushirish fayli bilan 100% orqa, main() (+21 more)

### Community 27 - "MainWindow"
Cohesion: 0.09
Nodes (12): QMainWindow, MainWindow, Any, Status bar orqali chiroyli xabar chiqarish., Dastur yopilayotganda avtomatik zaxira nusxa yaratish., Pop Tuman Tizimining Asosiy PyQt5 Oynasi., DashboardView, Any (+4 more)

### Community 28 - "TableView"
Cohesion: 0.15
Nodes (8): Any, QModelIndex, QWidget, Ma'lumotlarni SearchService orqali qidirish va modelga uzatish., PyQt5 Tashkilotlar Jadvali Ekrani., O'ng tugma bosilganda kontekst menyu., render_table(), TableView

### Community 29 - "TestQtArchitecture"
Cohesion: 0.15
Nodes (10): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., TestQtArchitecture, get_stylesheet(), Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Fluent & Material Design QSS), Belgilangan mavzu (Dark yoki Light) uchun to'liq QSS stilini qaytaradi., copy_cabinet_quick(), Oynani ochmasdan tezkor nusxalash. (+2 more)

### Community 30 - "SettingsView"
Cohesion: 0.16
Nodes (6): Any, QWidget, Mavjud sozlamalarni yuklash., Tizim sozlamalari ekrani., render_settings(), SettingsView

### Community 31 - "hash_password"
Cohesion: 0.25
Nodes (8): authenticate_user(), hash_password(), Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish., Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash., Parolni SHA-256 xeshga aylantirish., verify_password(), Xavfsizlik va parollarni tekshirish testlari., TestSecurity

### Community 32 - "MahallaPassportView"
Cohesion: 0.24
Nodes (5): MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi.

### Community 33 - "TrashView"
Cohesion: 0.21
Nodes (7): Any, QWidget, ui_qt.views.trash_view: Chiqindi qutisi (Recycle Bin) sahifasi (PyQt5). O'chiril, Chiqindi qutisi ekrani., Chiqindi ro'yxatini yuklash., render_trash(), TrashView

### Community 34 - "CabinetDialog"
Cohesion: 0.24
Nodes (5): CabinetDialog, Any, QDialog, Kabinetga dostup shablon oynasi., Belgilangan tashkilot bo'yicha matnni generatsiya qilish.

### Community 35 - "open_record_dialog"
Cohesion: 0.24
Nodes (7): Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin, validate_jshshir(), validate_passport_series(), Ma'lumotlarni validatsiya qilish va saqlash., open_record_dialog(), Tashkilot qo'shish yoki tahrirlash dialogi.

### Community 36 - "app.py"
Cohesion: 0.24
Nodes (7): Style, apply_treeview_style(), Treeview ranglari va shriftlarini Light/Dark rejimga moslashtirish., Any, Widget, Chiqindi qutisi (Trash) sahifasini ko'rsatish., render_trash()

### Community 37 - ".test_view_imports"
Cohesion: 0.29
Nodes (4): HistoryView, QDialog, Kadrlar tarixi dialog oynasi., SQLite dan tarix yozuvlarini yuklash.

### Community 38 - "VerificationDialog"
Cohesion: 0.27
Nodes (4): Any, QDialog, Verifikatsiya so'rovi shablon oynasi., VerificationDialog

### Community 39 - "ImportDialog"
Cohesion: 0.25
Nodes (5): ImportDialog, open_batch_import_dialog(), Any, QDialog, Excel / CSV ommaviy import dialog oynasi.

### Community 40 - "OrgEditDialog"
Cohesion: 0.32
Nodes (5): OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi.

### Community 41 - "test_views.py"
Cohesion: 0.33
Nodes (4): open_staff_history_dialog(), Any, Pop Tuman Tashkilotlari va INN Tizimi Xodimlar Rotatsiyasi va Kadrlar Tarixi Ko', Xodimlar almashinuvi tarixi dialog oynasi.

### Community 42 - "render_settings"
Cohesion: 0.50
Nodes (4): Any, Widget, Sozlamalar (Settings) sahifasini ko'rsatish., render_settings()

## Knowledge Gaps
- **12 isolated node(s):** `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)`, `📁 Loyiha Tuzilmasi`, `1-qadam. Loyihani yuklab olish` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `Data Persistence & Backup Manager` to `UI App Core & Event Handlers`, `app.py`, `SQLiteManager`, `sanitize_text`, `MainWindow`, `hash_password`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Why does `MahallaDasturi` connect `UI App Core & Event Handlers` to `External Services (Excel, QR, GSheets)`, `Data Persistence & Backup Manager`, `app.py`, `import_organizations_from_file`, `test_views.py`, `hash_password`, `import_organizations_from_file`, `sanitize_text`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `Data Persistence & Backup Manager`, `hash_password`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MahallaDasturi` (e.g. with `TestViewImports` and `.test_app_import()`) actually correct?**
  _`MahallaDasturi` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TableView` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`TableView` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `DataManager` (e.g. with `SQLiteManager` and `TestDataManager`) actually correct?**
  _`DataManager` has 4 INFERRED edges - model-reasoned connections that need verification._