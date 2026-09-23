# Graph Report - tashkilotlar INN tizim  (2026-09-23)

## Corpus Check
- 48 files · ~40,784 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 426 nodes · 751 edges · 28 communities (18 shown, 10 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `00640588`
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
- TestSQLiteManager
- Any
- logger.py
- .insert_or_replace_organization
- .save_all_trash

## God Nodes (most connected - your core abstractions)
1. `MahallaDasturi` - 54 edges
2. `SQLiteManager` - 27 edges
3. `DataManager` - 24 edges
4. `build_verification_text()` - 17 edges
5. `hash_password()` - 13 edges
6. `TestServices` - 13 edges
7. `import_organizations_from_file()` - 12 edges
8. `TelegramBotService` - 12 edges
9. `render_table()` - 12 edges
10. `render_dashboard()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `MahallaDasturi` --uses--> `DataManager`  [INFERRED]
  ui/app.py → database/data_manager.py
- `TestSQLiteManager` --uses--> `SQLiteManager`  [INFERRED]
  tests/test_sqlite.py → database/sqlite_manager.py
- `MahallaDasturi` --uses--> `SearchService`  [INFERRED]
  ui/app.py → services/search_service.py
- `TestViewImports` --uses--> `MahallaDasturi`  [INFERRED]
  tests/test_views.py → ui/app.py
- `import_organizations_from_file()` --calls--> `sanitize_text()`  [EXTRACTED]
  services/excel_service.py → core/validators.py

## Import Cycles
- None detected.

## Communities (28 total, 10 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.07
Nodes (15): MahallaDasturi, Any, CTk, Sessiya yoki parol kiritish orqali ruxsatni tekshirish., Tungi va kunduzgi rejimni almashtirish., Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)., Foydalanuvchiga silliq va xalaqit bermaydigan Toast bildirishnomasi., DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish. (+7 more)

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.09
Nodes (25): Client, install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, Pop Tuman Tashkilotlari va INN Tizimi Eski ishga tushirish fayli bilan 100% orqa, main(), Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy ishga tushirish nuqtasi (Entr, download_data_from_sheet(), extract_sheet_id() (+17 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.08
Nodes (27): clean_inn(), clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish. (+19 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.13
Nodes (11): normalize_text(), Any, Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Maydonlar: Nomi, F.I.SH, INN,, Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari). (+3 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.10
Nodes (15): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Tizimdagi harakatlarni qayd etish (JSON + SQLite)., Xodim rotatsiyasi/almashinuvini qayd etish. (+7 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.11
Nodes (14): export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi. (+6 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.13
Nodes (14): CTkFrame, Barcha UI ko'rinishlari (Views) runtime rejimida to'g'ri import bo'lishini teksh, TestViewImports, create_grid_card(), create_modern_card(), draw_donut_chart(), Any, Widget (+6 more)

### Community 7 - "SQLiteManager"
Cohesion: 0.13
Nodes (12): Connection, SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Tashkilotni ID bo'yicha o'chirish., Chiqindi qutisidagi barcha yozuvlarni olish., SQLite ulanishini olish va WAL rejimini faollashtirish., Xodim rotatsiyasi/almashinuvini tarix jadvaliga qo'shish (ko'p qirrali parametrl, Baza jadvallari va indekslarini yaratish., Tizimdagi harakatni SQLite jurnaliga qayd etish. (+4 more)

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
Cohesion: 0.19
Nodes (12): authenticate_user(), hash_password(), Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish., Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash., Parolni SHA-256 xeshga aylantirish., verify_password(), Xavfsizlik va parollarni tekshirish testlari., TestSecurity (+4 more)

### Community 22 - "TelegramBotService"
Cohesion: 0.23
Nodes (6): Any, Telegram Bot orqali tashkilotlar bazasini qidirish va verifikatsiya taqdim etish, Botni fon rejimida ishga tushirish., Foydalanuvchiga xabar yuborish., Telegramdan yangi xabarlarni tinglash sikli (Long polling)., TelegramBotService

### Community 23 - "TestSQLiteManager"
Cohesion: 0.14
Nodes (7): Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., TestSQLiteManager

### Community 24 - "Any"
Cohesion: 0.17
Nodes (7): Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Barcha tashkilotlarni atomik tranzaksiya bilan to'liq saqlash/yangilash., Ommaviy tashkilotlarni saqlash va sonini qaytarish., Tashkilotni unikal ID si bo'yicha olish., Tashkilotni INN si bo'yicha olish., Xodimlar tarixini olish (tashkilot yoki mahalla bo'yicha).

### Community 25 - "logger.py"
Cohesion: 0.24
Nodes (5): Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Logger

## Knowledge Gaps
- **12 isolated node(s):** `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)`, `📁 Loyiha Tuzilmasi`, `1-qadam. Loyihani yuklab olish` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `Data Persistence & Backup Manager` to `UI App Core & Event Handlers`, `logger.py`, `Core Configuration & Logging`, `SQLiteManager`?**
  _High betweenness centrality (0.238) - this node is a cross-community bridge._
- **Why does `MahallaDasturi` connect `UI App Core & Event Handlers` to `Core Configuration & Logging`, `External Services (Excel, QR, GSheets)`, `Data Persistence & Backup Manager`, `import_organizations_from_file`, `UI Views Test Suite`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `SQLiteManager` to `Data Persistence & Backup Manager`, `TestSQLiteManager`, `Any`, `logger.py`, `.insert_or_replace_organization`, `.save_all_trash`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MahallaDasturi` (e.g. with `TestViewImports` and `.test_app_import()`) actually correct?**
  _`MahallaDasturi` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SQLiteManager` (e.g. with `DataManager` and `TestSQLiteManager`) actually correct?**
  _`SQLiteManager` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `DataManager` (e.g. with `SQLiteManager` and `TestDataManager`) actually correct?**
  _`DataManager` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._