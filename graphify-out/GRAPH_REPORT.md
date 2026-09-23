# Graph Report - tashkilotlar INN tizim  (2026-09-23)

## Corpus Check
- 40 files · ~34,102 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 288 nodes · 495 edges · 21 communities (12 shown, 9 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9c715b6a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- UI App Core & Event Handlers
- Core Configuration & Logging
- Data Validation & Formatting
- External Services (Excel, QR, GSheets)
- Data Persistence & Backup Manager
- Domain Data Models
- UI Views Test Suite
- Dashboard & Chart Analytics
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

## God Nodes (most connected - your core abstractions)
1. `MahallaDasturi` - 49 edges
2. `DataManager` - 21 edges
3. `hash_password()` - 13 edges
4. `TestServices` - 12 edges
5. `render_table()` - 11 edges
6. `render_dashboard()` - 10 edges
7. `validate_inn()` - 9 edges
8. `validate_phone()` - 9 edges
9. `Organization` - 9 edges
10. `SearchService` - 9 edges

## Surprising Connections (you probably didn't know these)
- `MahallaDasturi` --uses--> `DataManager`  [INFERRED]
  ui/app.py → database/data_manager.py
- `MahallaDasturi` --uses--> `SearchService`  [INFERRED]
  ui/app.py → services/search_service.py
- `TestViewImports` --uses--> `MahallaDasturi`  [INFERRED]
  tests/test_views.py → ui/app.py
- `TestDataManager` --uses--> `DataManager`  [INFERRED]
  tests/test_data_manager.py → database/data_manager.py
- `TestModels` --uses--> `Organization`  [INFERRED]
  tests/test_models.py → database/models.py

## Import Cycles
- None detected.

## Communities (21 total, 9 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.09
Nodes (10): MahallaDasturi, Any, CTk, Sessiya yoki parol kiritish orqali ruxsatni tekshirish., Tungi va kunduzgi rejimni almashtirish., Pop Tumani Tashkilotlari va INN Tizimi Asosiy Dasturi (Clean Architecture)., Foydalanuvchiga silliq va xalaqit bermaydigan Toast bildirishnomasi., DRY va KISS: Qidiruv va filtrlashni SearchService orqali bajarish. (+2 more)

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.09
Nodes (25): Client, install_global_exception_handler(), Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, setup_logger(), Logger, Pop Tuman Tashkilotlari va INN Tizimi Eski ishga tushirish fayli bilan 100% orqa (+17 more)

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.09
Nodes (28): clean_inn(), clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, INN (STIR) dan faqat raqamlarni ajratib olish., O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish. (+20 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.08
Nodes (21): Image, export_organizations_to_excel(), Any, Tashkilotlar ro'yxatini zamonaviy formatlangan Excel (.xlsx) fayliga yuklash., clean_phone_number(), generate_phone_qr_image(), Telefon raqami uchun xotirada (RAM) toza QR-kod tasvirini yaratish., Telefon raqamini tozalash va to'g'ri xalqaro formatga keltirish. (+13 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.11
Nodes (13): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, Dependency-Injected), Tizimdagi harakatlarni qayd etish., Yozuvni Chiqindi qutisiga ko'chirish. (+5 more)

### Community 5 - "Domain Data Models"
Cohesion: 0.22
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 6 - "UI Views Test Suite"
Cohesion: 0.13
Nodes (14): CTkFrame, Barcha UI ko'rinishlari (Views) runtime rejimida to'g'ri import bo'lishini teksh, TestViewImports, create_grid_card(), create_modern_card(), draw_donut_chart(), Any, Widget (+6 more)

### Community 7 - "Dashboard & Chart Analytics"
Cohesion: 0.19
Nodes (12): authenticate_user(), hash_password(), Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish., Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash., Parolni SHA-256 xeshga aylantirish., verify_password(), Xavfsizlik va parollarni tekshirish testlari., TestSecurity (+4 more)

### Community 8 - "Toast Notification System"
Cohesion: 0.28
Nodes (6): CTk, Pop Tuman Tashkilotlari va INN Tizimi Zamonaviy Toast / Banner Bildirishnomalar, Qulay yordamchi funksiya., Oynaning pastki qismida silliq paydo bo'lib yo'qoluvchi bildirishnoma., show_toast(), ToastNotification

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.15
Nodes (12): 1-qadam. Loyihani yuklab olish, 2-qadam. Kerakli kutubxonalarni o'rnatish, 3-qadam. Dasturni ishga tushirish, 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish, 🔑 Kalit Fayllar va Sozlamalar, 📁 Loyiha Tuzilmasi, 📞 Muallif va Ruxsatnoma, 📦 Mustaqil Windows `.exe` Dasturini Yig'ish (+4 more)

## Knowledge Gaps
- **12 isolated node(s):** `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)`, `📁 Loyiha Tuzilmasi`, `1-qadam. Loyihani yuklab olish` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MahallaDasturi` connect `UI App Core & Event Handlers` to `Core Configuration & Logging`, `Data Validation & Formatting`, `External Services (Excel, QR, GSheets)`, `Data Persistence & Backup Manager`, `UI Views Test Suite`?**
  _High betweenness centrality (0.271) - this node is a cross-community bridge._
- **Why does `DataManager` connect `Data Persistence & Backup Manager` to `UI App Core & Event Handlers`, `Core Configuration & Logging`?**
  _High betweenness centrality (0.170) - this node is a cross-community bridge._
- **Why does `SearchService` connect `External Services (Excel, QR, GSheets)` to `UI App Core & Event Handlers`, `Core Configuration & Logging`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MahallaDasturi` (e.g. with `TestViewImports` and `.test_app_import()`) actually correct?**
  _`MahallaDasturi` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `DataManager` (e.g. with `TestDataManager` and `MahallaDasturi`) actually correct?**
  _`DataManager` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `Workflow: graphify`, `🚀 Versiya 3.0 (Production-Grade & Clean Architecture)` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `UI App Core & Event Handlers` be split into smaller, more focused modules?**
  _Cohesion score 0.08985507246376812 - nodes in this community are weakly interconnected._