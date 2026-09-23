# Graph Report - tashkilotlar INN tizim  (2026-09-23)

## Corpus Check
- 50 files · ~41,699 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 449 nodes · 806 edges · 23 communities (15 shown, 8 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `86c1f129`
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

## God Nodes (most connected - your core abstractions)
1. `MahallaDasturi` - 55 edges
2. `SQLiteManager` - 27 edges
3. `DataManager` - 24 edges
4. `build_verification_text()` - 17 edges
5. `TestServices` - 14 edges
6. `hash_password()` - 13 edges
7. `open_cabinet_dialog()` - 13 edges
8. `render_dashboard()` - 13 edges
9. `render_table()` - 13 edges
10. `import_organizations_from_file()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `MahallaDasturi` --uses--> `DataManager`  [INFERRED]
  ui/app.py → database/data_manager.py
- `MahallaDasturi` --uses--> `SearchService`  [INFERRED]
  ui/app.py → services/search_service.py
- `TestViewImports` --uses--> `MahallaDasturi`  [INFERRED]
  tests/test_views.py → ui/app.py
- `open_record_dialog()` --calls--> `validate_inn()`  [EXTRACTED]
  ui/views/table_view.py → core/validators.py
- `open_record_dialog()` --calls--> `validate_phone()`  [EXTRACTED]
  ui/views/table_view.py → core/validators.py

## Import Cycles
- None detected.

## Communities (23 total, 8 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.06
Nodes (16): MahallaDasturi, Any, CTk, Sessiya yoki parol kiritish orqali ruxsatni tekshirish., Tungi va kunduzgi rejimni almashtirish., Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)., Foydalanuvchiga silliq va xalaqit bermaydigan Toast bildirishnomasi., DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish. (+8 more)

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.20
Nodes (13): Client, download_data_from_sheet(), extract_sheet_id(), get_gspread_client(), open_spreadsheet(), Any, URL yoki matndan Google Sheet ID sini ajratib olish., Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali (+5 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.05
Nodes (38): clean_inn(), clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish. (+30 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.10
Nodes (14): export_organizations_to_excel(), Any, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., normalize_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati. (+6 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.10
Nodes (15): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Tizimdagi harakatlarni qayd etish (JSON + SQLite)., Xodim rotatsiyasi/almashinuvini qayd etish. (+7 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.12
Nodes (6): Barcha UI ko'rinishlari (Views) runtime rejimida to'g'ri import bo'lishini teksh, TestViewImports, open_staff_history_dialog(), Any, Pop Tuman Tashkilotlari va INN Tizimi Xodimlar Rotatsiyasi va Kadrlar Tarixi Ko', Xodimlar almashinuvi tarixi dialog oynasi.

### Community 6 - "UI Views Test Suite"
Cohesion: 0.15
Nodes (22): CTkFrame, build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., copy_cabinet_quick() (+14 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.06
Nodes (29): Connection, Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan to'liq saqlash/yangilash., Bitta tashkilotni qo'shish yoki yangilash., SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Bitta tashkilotni qo'shish yoki yangilash (Alias)., Ommaviy tashkilotlarni saqlash va sonini qaytarish. (+21 more)

### Community 8 - "Toast Notification System"
Cohesion: 0.28
Nodes (6): CTk, Pop Tuman Tashkilotlari va INN Tizimi Zamonaviy Toast / Banner Bildirishnomalar, Qulay yordamchi funksiya., Oynaning pastki qismida silliq paydo bo'lib yo'qoluvchi bildirishnoma., show_toast(), ToastNotification

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.15
Nodes (12): 1-qadam. Loyihani yuklab olish, 2-qadam. Kerakli kutubxonalarni o'rnatish, 3-qadam. Dasturni ishga tushirish, 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish, 🔑 Kalit Fayllar va Sozlamalar, 📁 Loyiha Tuzilmasi, 📞 Muallif va Ruxsatnoma, 📦 Mustaqil Windows `.exe` Dasturini Yig'ish (+4 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.09
Nodes (39): Image, Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., clean_phone_number(), generate_phone_qr_image(), Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish., Pop Tuman Tashkilotlari va INN Tizimi Telegram Bot Xizmati (Telegram Bot Service, build_verification_text() (+31 more)

### Community 21 - "hash_password"
Cohesion: 0.08
Nodes (29): install_global_exception_handler(), Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, setup_logger(), authenticate_user(), hash_password(), Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish. (+21 more)

### Community 22 - "TelegramBotService"
Cohesion: 0.23
Nodes (6): Any, Telegram Bot orqali tashkilotlar bazasini qidirish va verifikatsiya taqdim etish, Botni fon rejimida ishga tushirish., Foydalanuvchiga xabar yuborish., Telegramdan yangi xabarlarni tinglash sikli (Long polling)., TelegramBotService

## Knowledge Gaps
- **12 isolated node(s):** `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)`, `📁 Loyiha Tuzilmasi`, `1-qadam. Loyihani yuklab olish` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MahallaDasturi` connect `UI App Core & Event Handlers` to `Core Configuration & Logging`, `External Services (Excel, QR, GSheets)`, `Data Persistence & Backup Manager`, `import_organizations_from_file`, `hash_password`?**
  _High betweenness centrality (0.236) - this node is a cross-community bridge._
- **Why does `DataManager` connect `Data Persistence & Backup Manager` to `UI App Core & Event Handlers`, `hash_password`, `SQLiteManager`?**
  _High betweenness centrality (0.230) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `Data Persistence & Backup Manager`, `hash_password`?**
  _High betweenness centrality (0.205) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MahallaDasturi` (e.g. with `TestViewImports` and `.test_app_import()`) actually correct?**
  _`MahallaDasturi` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SQLiteManager` (e.g. with `DataManager` and `TestSQLiteManager`) actually correct?**
  _`SQLiteManager` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `DataManager` (e.g. with `SQLiteManager` and `TestDataManager`) actually correct?**
  _`DataManager` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._