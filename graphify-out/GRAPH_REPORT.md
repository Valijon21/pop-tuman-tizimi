# Graph Report - tashkilotlar INN tizim  (2026-09-25)

## Corpus Check
- 69 files · ~107,266 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1152 nodes · 2369 edges · 73 communities (55 shown, 18 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 205 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `63348d60`
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
- .open_column_manager
- .insert_or_replace_organization
- .on_table_double_clicked
- .load_data
- extract_sheet_id
- .load_settings
- .update_settings_password
- .apply_column_widths
- .test_task5_auto_backup_scheduler
- render_settings
- .on_backup_interval_changed
- .update_edit_password

## God Nodes (most connected - your core abstractions)
1. `MainWindow` - 56 edges
2. `TableView` - 52 edges
3. `ContractsView` - 49 edges
4. `TelegramBotService` - 48 edges
5. `DataManager` - 46 edges
6. `TestQtArchitecture` - 40 edges
7. `SQLiteManager` - 38 edges
8. `SettingsView` - 36 edges
9. `OrgEditDialog` - 35 edges
10. `WorkerThread` - 32 edges

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

## Communities (73 total, 18 thin omitted)

### Community 0 - "UI App Core & Event Handlers"
Cohesion: 0.27
Nodes (8): install_global_exception_handler(), Barcha kutilmagan xatoliklarni (Unhandled Exceptions) avtomatik log faylga yozis, main(), Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise) Asosiy ishga tushiri, Asosiy ilovani ishga tushirish (Entry Point)., Pop Tuman Tashkilotlari va INN Tizimi (PRO) Asosiy kirish nuqtasi (Entry Point A, PyQt5 ilovasini ishga tushirish (High-DPI, AppUserModelID va Yagona Nusxa / Sing, run_qt_app()

### Community 1 - "Core Configuration & Logging"
Cohesion: 0.15
Nodes (8): OrgEditDialog yangi tashkilot rejimida toifani to'g'ri qabul qilishi., Barcha dialoglar Light rejimida to'g'ri ochilishi va stillari o'rnatilishini tek, OrgEditDialog, Any, QDialog, Mavjud ma'lumotlarni formaga yuklash., Tashkilot ma'lumotlarini qo'shish yoki tahrirlash oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 2 - "Data Validation & Formatting"
Cohesion: 0.06
Nodes (28): QMouseEvent, QPaintEvent, QPoint, Dashboard statistika kartalari balandligi, ikonka o'lchamlari va ranglari to'g'r, CategoryBarChart, CategoryDonutChart, CategoryLegend, ClickableCard (+20 more)

### Community 3 - "External Services (Excel, QR, GSheets)"
Cohesion: 0.06
Nodes (41): normalize_text(), Qidiruv uchun matnni to'liq normallashtirish (tutuq belgilari, kirill-lotin, ora, get_role_priority(), get_telegram_bot_service(), Any, Mahalla yettiligi xodimlarini professional, toza ko'rinishda chiqarish., Bot tokeni kiritilgan va sozlanganligini tekshirish., Oldin saqlangan obunachilar (chat_id) ro'yxatini yuklash. (+33 more)

### Community 4 - "Data Persistence & Backup Manager"
Cohesion: 0.16
Nodes (14): clean_phone(), format_phone(), Pop Tuman Tashkilotlari va INN Tizimi Ma'lumotlarni tekshirish va tozalash (Val, Biometrik pasport / ID karta seriyasini tekshirish (masalan: AB1234567, AA765432, Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish., Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish., Telefon raqamini tekshirish.          Qaytaradi: (to'g'riligi: bool, formatlan, O'zbekiston JSHSHIR (PINFL - 14 ta raqam) ni tekshirish.     Birinchi raqam jin (+6 more)

### Community 5 - "import_organizations_from_file"
Cohesion: 0.08
Nodes (19): Pop Tuman Tashkilotlari va INN Tizimi Tezkor Qidiruv va Filtrlash Xizmati (Sear, Kirill yozuvidagi o'zbek matnini lotin yozuviga o'girish., transliterate_to_latin(), tests/test_custom_columns.py: Dinamik ustunlar qo'shish va boshqarish bo'yicha b, ColumnManagerDialog komponenti to'g'ri ishlashi., Dinamik ustunlar va ularning saqlanishi bo'yicha to'liq testlar., SQLiteManager da yangi ustun ochish va ma'lumotlarni xatosiz saqlash., TestCustomColumns (+11 more)

### Community 6 - "UI Views Test Suite"
Cohesion: 0.21
Nodes (7): Organization, Any, Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish., Obyektni lug'atga aylantirish., Tashkilot ma'lumotlar modeli va validatsiyasi., Organization ma'lumotlar modeli testlari., TestModels

### Community 7 - "SQLiteManager"
Cohesion: 0.17
Nodes (8): ContractAddDialog yangi tashkilot rejimida toifani to'g'ri qabul qilishi., Shartnoma qo'shish/tahrirlash dialogi yaratilishi va ma'lumot yuklanishini teksh, ContractAddDialog, Any, QDialog, Shartnoma va ulanish ma'lumotlarini qo'shish yoki tahrirlash oynasi., Mavjud ma'lumotlarni formaga yuklash (tahrirlash yoki oldindan to'ldirish rejimi, Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 8 - "settings_view.py"
Cohesion: 0.12
Nodes (8): Test TableView search, pill selection, category filters., Test ContractsView loading, KPI cards and filters., Test TrashView and SettingsView loading., Verify stylesheet generator with dark/light and various font sizes., Test switching across all tabs in MainWindow., Test toggling between dark/light and dynamic font scaling., Test Dashboard buttons, KPI cards, charts, and table interactions., TestUIUXDeep

### Community 9 - "Application Lifecycle & Entry Points"
Cohesion: 0.09
Nodes (21): 1. Repozitoriyni klonlash, 🏢 1. Toifalar Qatorida Tezkor Tashkilot va Toifa Qo'shish (Quick Add Engine), 2. Bog'liqliklarni o'rnatish, ⚙️ 2. Professional Dinamik Ustunlar Menejeri (Column Manager), 🔍 3. Aqlli Qidiruv va Mos Nomlar Taklifi (Smart Search Engine), 3. Dasturni ishga tushirish, 🏘 4. Mahalla "Yettiligi" 360° Raqamli Pasporti, 📑 4. Shartnoma va Ulanishlar Monitoringi (+13 more)

### Community 14 - "Services Package Architecture"
Cohesion: 0.13
Nodes (9): Any, Auto-complete takliflari uchun barcha unikal nomlar, INN va xodimlar ro'yxati., Tashkilotlar bo'yicha umumiy statistika hisoblash., Tashkilotlar bazasida tezkor, aqlli qidiruv va filtrlash xizmati., Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)., Ko'p maydonli aqlli qidiruv va filtrlash.         Lotin/Kirill transliteratsiya, SearchService, Qidiruv, QR va Excel xizmatlari testlari. (+1 more)

### Community 15 - "Cloud Sync Verification"
Cohesion: 0.13
Nodes (11): Task 6: ContractsView va TrashView da signal boshqaruvi va unumdorlik., Any, QWidget, Tanlangan yozuvlarni bir martalik atomik tranzaksiyada bazaga qayta tiklash., Chiqindi qutisi ekrani., Tanlangan yozuvlarni bir martalik to'plamli operatsiyada butunlay o'chirish., Chiqindi qutisini ommaviy atomik operatsiya bilan to'liq tozalash (disk va SQLit, Chiqindi qutisi sahifasini tanlangan mavzuga moslashtirish. (+3 more)

### Community 16 - "OrganizationTableModel"
Cohesion: 0.08
Nodes (17): ItemFlags, Orientation, QAbstractTableModel, SortOrder, OrganizationTableModel ga dinamik ustunlar qo'shish va o'qish., OrganizationTableModel da maxsus ustun katagini inline tahrirlash., Maxsus ustunlar bo'yicha to'g'ri saralash., OrganizationTableModel (+9 more)

### Community 17 - "Organization"
Cohesion: 0.12
Nodes (8): Kadrlar rotatsiyasi tarixi audit yozuvini tekshirish., Zaxira nusxa yaratish funksiyasini tekshirish., Jadvallar to'g'ri yaratilganligini tekshirish., Ommaviy yozuv qo'shish va barchasini olish testi., Yozuvni kiritish, yangilash va o'chirish., SQLite Manager ACID va Ma'lumotlar Bazasi Testlari., Chiqindi qutisida barcha yangi ustunlar saqlanishini tekshirish., TestSQLiteManager

### Community 21 - "hash_password"
Cohesion: 0.06
Nodes (28): QLabel, QLineEdit, QPushButton, Yordamchi dasturlar (AppsView) sahifasi va tugmalarini sinash., AppsView, copy_file_to_windows_clipboard(), QFrame, QWidget (+20 more)

### Community 22 - "test_services.py"
Cohesion: 0.23
Nodes (10): BroadcastService, calculate_sms_segments(), extract_clean_phone_list(), filter_audience_recipients(), Any, Pop Tuman Tashkilotlari va INN Tizimi Ommaviy Xabarnoma va Bildirishnoma Xizmati, Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi., Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllanti (+2 more)

### Community 23 - "import_organizations_from_file"
Cohesion: 0.11
Nodes (24): authenticate_user(), generate_salt(), hash_password(), hash_password_salted(), is_rate_limited(), core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli. PBKDF, Muvaffaqiyatsiz urinishni qayd etish., Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash. (+16 more)

### Community 24 - "TestImportService"
Cohesion: 0.16
Nodes (7): ContractsView da toifalar qatorida Tashkilot qo'shish va Toifa tugmalari mavjudl, ContractsView, Ctrl+F bosilganda qidiruv maydoniga o'tish., Ustun bosib saralangandan so'ng № ustunini 1, 2, 3... qilib qayta raqamlash., Shartnoma va Ulanishlar Monitoringi Sahifasi., O'ng tugma kontekst menyusi., Shartnoma ma'lumotlarini Excelga eksport qilish.

### Community 25 - "clean_inn"
Cohesion: 0.14
Nodes (15): clean_mahalla_key(), ExcelSyncService, format_fio(), format_phone(), Any, Excel faylidagi ma'lumotlarni bazaga xavfsiz kiritish klassi., Excel dagi mahalla nomini bazadagi aniq Lotincha MFY nomiga bog'lash., Excel faylidan barcha xodimlarni o'qib, bazani xavfsiz yangilash.         Dublik (+7 more)

### Community 26 - "sanitize_text"
Cohesion: 0.15
Nodes (15): core.threading_utils: Asinxron fon oqimlari (QThread) va vazifalar boshqaruvi. U, ui_qt.app_window: Pop Tumani Tashkilotlari va INN Tizimi Asosiy PyQt5 Oynasi (Cl, create_crisp_pixmap(), ui_qt.styles: Pop Tuman Tizimi - PyQt5 Zamonaviy Dizayn Tizimi (Senior Enterpris, Retina / 4K / High-DPI o'lchamli kristall tiniqlikdagi QPixmap yaratish.     Win, ui_qt.views.broadcast_view: Ommaviy Xabarnoma (SMS & Telegram) dialogi (PyQt5)., copy_cabinet_quick(), open_cabinet_dialog() (+7 more)

### Community 27 - "MainWindow"
Cohesion: 0.06
Nodes (21): QMainWindow, Menyular orasida navigatsiya kechikishsiz va dirty bayrog'i orqali ishlashini te, MainWindow, Any, Dialog ochuvchi sidebar tugmalari uchun: checked holatni to'g'ri boshqarish., Sozlamalardan shrift o'lchami o'zgarganda darhol butun tizimda qo'llash., Belgilangan amal ('edit' yoki 'settings') uchun xavfsizlik parolini tekshirish., Yordamchi va kommunal dasturlar sahifasini ochish (UzCrypto, AnyDesk). (+13 more)

### Community 28 - "TableView"
Cohesion: 0.13
Nodes (9): Any, QModelIndex, Ctrl+F bosilganda qidiruv maydoniga fokus va matnni belgilash., Jadvalda klaviatura hodisalarini ushlash: Enter, Delete, Ctrl+C., Tanlangan katak(lar) yoki ko'kartirib belgilangan matnlarni buferga nusxalash (C, O'ng tugma bosilganda kontekst menyu., PyQt5 Tashkilotlar Jadvali Ekrani., render_table() (+1 more)

### Community 29 - "settings_view.py"
Cohesion: 0.19
Nodes (6): BroadcastView, open_broadcast_dialog(), Any, QDialog, Auditoriya filtri bo'yicha qabul qiluvchilar ro'yxatini chiqarish., Ommaviy xabarnoma dialog oynasi.

### Community 30 - "telegram_bot.py"
Cohesion: 0.24
Nodes (5): MahallaPassportView, QDialog, Tizimdagi barcha mahallalarni to'plash., Tanlangan mahalla uchun 7 ta kartani to'ldirish., Mahalla Yettiligi 360 Pasport Oynasi.

### Community 31 - "hash_password"
Cohesion: 0.16
Nodes (6): QWidget, Jadval sahifasidagi barcha inline stillarni mavzuga moslashtirish., Kategoriya tugmalarini va qo'shish tugmalarini dinamik barpo etish., Yangi toifa qo'shish dialogi., 250ms Debounce bilan qidiruv: tez yozishda UI qotmasligini ta'minlaydi., Ma'lumotlarni SearchService orqali qidirish va modelga uzatish.

### Community 32 - "VerificationDialog"
Cohesion: 0.17
Nodes (5): Test all dialogs for clean initialization, styles, and button bindings., ImportDialog, QDialog, Excel / CSV ommaviy import dialog oynasi., Oynani ochishdan oldin tahrirlash paroli (1234567) ruxsatini tekshirish.

### Community 33 - ".__init__"
Cohesion: 0.23
Nodes (10): ContractsSyncService, format_phone_clean(), parse_int_safe(), Any, services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodim, Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish., Raqamni xavfsiz butun songa o'tkazish., Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis. (+2 more)

### Community 34 - "DataManager"
Cohesion: 0.07
Nodes (25): Connection, Any, Barcha faol tashkilotlarni ro'yxat ko'rinishida olish., Jadval ustunlari ro'yxatini olish., SQLite bilan xavfsiz va tranzaksiyaviy ishlash menejeri., Jadvalga yangi ustunni xavfsiz qo'shish (organizations va trash jadvallariga)., Barcha tashkilotlarni atomik tranzaksiya bilan xavfsiz saqlash/yangilash (dinami, Tashkilotni ID si bo'yicha SQLite bazasidan butunlay o'chirish. (+17 more)

### Community 35 - "validate_inn"
Cohesion: 0.26
Nodes (11): Client, download_data_from_sheet(), get_gspread_client(), open_spreadsheet(), Any, Google Sheets klientini yaratish (zamonaviy google-auth yoki oauth2client orqali, ID, URL yoki nom orqali jadvalni ochish., Ma'lumotlar ro'yxatini Google Sheetga yuklash (to'liq 13 ta ustun bilan). (+3 more)

### Community 36 - "extract_sheet_id"
Cohesion: 0.24
Nodes (9): Services moduli: Tashqi integratsiyalar, eksport va yordamchi xizmatlar., build_verification_text(), extract_identifiers_from_text(), format_role(), Any, Pop Tuman Tashkilotlari va INN Tizimi Verifikatsiya Xizmati (Verification Servic, Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB123, Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish. (+1 more)

### Community 37 - "CabinetDialog"
Cohesion: 0.24
Nodes (5): CabinetDialog, Any, QDialog, Tanlangan tashkilot ma'lumotlarini yuklash., Kabinetga dostup shablon oynasi.

### Community 38 - "build_verification_text"
Cohesion: 0.12
Nodes (7): QWidget, Tizim sozlamalari ekrani., Sozlamalar sahifasidagi inline stillarni mavzuga moslashtirish., Avtomatik zaxira yoqilgan/o'chirilganda sozlamani yangilash., Fonda zaxiralashni hoziroq sinab ko'rish., MainWindow dan chaqiriladigan oxirgi zaxira vaqti ko'rsatkichi., SettingsView

### Community 39 - "sync_contracts_data.py"
Cohesion: 0.22
Nodes (7): build_cabinet_access_text(), get_cabinet_portal_url(), Any, Pop Tuman Tashkilotlari va INN Tizimi Kabinet Xizmati (Cabinet Access Service) X, Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon mat, Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish., ui_qt.views.mahalla_passport_view: Mahalla 'Yettiligi' 360° Pasport oynasi (PyQt

### Community 40 - "OrgEditDialog"
Cohesion: 0.20
Nodes (15): clean_phone_number(), generate_mecard_data(), generate_mecard_qr_image(), generate_phone_qr_image(), generate_vcard_data(), generate_vcard_qr_image(), Image, Mobil kontakt (MeCard) uchun toza QR-kod tasvirini yaratish. (+7 more)

### Community 41 - "pil_to_qpixmap"
Cohesion: 0.19
Nodes (10): export_mahalla_passport_pdf(), export_organizations_pdf(), _image_to_base64_src(), Any, services.pdf_service: Pop Tuman Tashkilotlari va Mahalla Yettiligi A4 PDF Ekspor, PIL tasvirni HTML <img> uchun base64 URI ga aylantirish., Tashkilotlar ro'yxatini A4 formatidagi rasmiy PDF hisobot ko'rinishida eksport q, Mahalla 'Yettiligi' 360° Pasportini A4 formatidagi rasmiy PDF hujjat ko'rinishid (+2 more)

### Community 42 - ".test_07_dialogs_instantiation"
Cohesion: 0.40
Nodes (4): attach_smart_completer(), ui_qt.components.smart_completer: Zamonaviy va Aqlli Qidiruv Auto-Complete (Takl, Ixtiyoriy QLineEdit maydoniga aqlli qidiruv auto-complete tizimini biriktirish., ui_qt.views.history_view: Kadrlar almashinuvi va rotatsiyasi tarixi dialogi (PyQ

### Community 46 - "export_organizations_to_excel"
Cohesion: 0.10
Nodes (18): DataManager, Any, Zaxira nusxalar papkasi mavjudligini ta'minlash., Fayldan xavfsiz o'qish (buzilgan taqdirda zaxiradan tiklash)., Atomik saqlash: ma'lumot avval .tmp ga to'liq yozilib, keyin xavfsiz almashtiril, Ma'lumotlar omborini xavfsiz boshqarish (Persistence layer, SQLite + JSON dual-s, Baza ma'lumotlarini (SQLite yoki JSON) qayta yuklash., Yangi tashkilot qo'shish (dict yoki Organization modeli qabul qiladi). (+10 more)

### Community 47 - "TestDataManager"
Cohesion: 0.15
Nodes (5): MockApp, TableView da toifalar qatorida Tashkilot qo'shish va Toifa tugmalari mavjudligi., Toifalar qatorida tashkilot va toifa qo'shish testlari., DataManager orqali yangi toifa qo'shish va saqlanishi., TestAddOrgPills

### Community 48 - "Any"
Cohesion: 0.15
Nodes (10): QPixmap, QR kod oynasi (Tel va vCard rejimlarida) to'g'ri yaratilishini tekshirish., pil_to_qpixmap(), Any, Image, QDialog, QRDialog, QR kod tasvirini joriy rejim bo'yicha qayta chizish. (+2 more)

### Community 49 - "is_service_account_available"
Cohesion: 0.22
Nodes (6): QTableWidgetItem, NumericTableWidgetItem, Sonlar, INN va litsenziya ko'rsatkichlarini to'g'ri raqamli tartiblash (sorting), 250ms Debounce bilan qidiruv., Qidiruv va toifa bo'yicha ma'lumotlarni filtrlab jadvalga chiqarish., Jadval qatorlarini professional, tartibli va rangli nishonlar bilan chizish.

### Community 50 - ".add_organization"
Cohesion: 0.13
Nodes (15): Comprehensive UI/UX Deep Testing & Verification Script Simulates loading all vie, get_stylesheet(), Belgilangan mavzu (Dark yoki Light) va shrift o'lchami bo'yicha     to'liq va mu, open_batch_import_dialog(), Any, ui_qt.views.import_dialog: Excel va CSV fayllardan ommaviy import qilish dialogi, copy_verification_quick(), open_verification_dialog() (+7 more)

### Community 52 - ".save_all_organizations"
Cohesion: 0.22
Nodes (7): QCompleter, get_completer_popup_style(), Auto-complete popapining Fluent UI uslubidagi stylesheeti., Senior darajadagi aqlli qidiruv takliflari (Auto-complete) klassi., Mavzuni yangilash (Dark / Light)., Takliflar ro'yxatini tezkor yangilash., SmartSearchCompleter

### Community 53 - ".send_welcome"
Cohesion: 0.19
Nodes (9): clean_inn(), INN (STIR) dan faqat raqamlarni ajratib olish., Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash., sanitize_text(), export_organizations_to_excel(), import_organizations_from_file(), Any, Excel (.xlsx, .xls) yoki CSV fayldan tashkilotlar ro'yxatini aqlli o'qish va val (+1 more)

### Community 54 - "setup_logger"
Cohesion: 0.09
Nodes (16): get_utility_path(), Yordamchi dastur fayli yo'lini topish (BASE_DIR yoki PyInstaller MEIPASS)., Pop Tuman Tashkilotlari va INN Tizimi Professional Aylanuvchi Log Tizimi va Glob, Aylanuvchi fayl log tizimini sozlash (5MB chegara va 5 ta arxiv nusxasi)., setup_logger(), Pop Tuman Tashkilotlari va INN Tizimi SQLite Tranzaksiyaviy Ma'lumotlar Bazasi D, Logger, Aqlli tokenli moslash: barcha so'zlar nishon ichida uchrashini tekshiradi. (+8 more)

### Community 55 - ".backup_data"
Cohesion: 0.13
Nodes (10): tests/test_qt_views.py: PyQt5 UI komponentlari va modellarining avtomatlashtiril, PyQt5 arxitekturasi, modellari va ko'rinishlarini sinash., TestQtArchitecture, PasswordPromptDialog, Any, QDialog, Parolni ko'rsatish yoki yashirish., Amal ('edit' yoki 'settings') uchun parolni so'rash.     Agar joriy sessiyada av (+2 more)

### Community 56 - ".get_organization_by_id"
Cohesion: 0.20
Nodes (5): CSV fayldan tashkilotlarni aniqlash va import qilish., Bo'sh faylni yuklashda ogohlantirish qaytarish., Noto'g'ri fayl formati xatosi., Excel va CSV fayllardan ommaviy import qilish testlari., TestImportService

### Community 57 - ".get_organization_by_inn"
Cohesion: 0.29
Nodes (3): QStyledItemDelegate, IzohDelegate, Izoh ustuni uchun maxsus zamonaviy inline muharrir (QLineEdit).

### Community 58 - ".get_recent_activity"
Cohesion: 0.22
Nodes (5): O'zbekiston STIR (INN) raqamini tekshirish.     STIR 9 ta raqamdan iborat bo'li, validate_inn(), Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish., Ma'lumotlarni validatsiya qilish va saqlash., Ma'lumotlarni validatsiya qilish va saqlash.

### Community 59 - "broadcast_service.py"
Cohesion: 0.33
Nodes (3): Task 1: SQLite delete_organization va delete_trash_item to'g'ri ishlashi., Task 2: QLockFile orqali ikkinchi instansiyani aniqlash va qulflash., TestFeatures12346

### Community 60 - ".send_help"
Cohesion: 0.22
Nodes (5): Any, Oqimni to'xtatish bayrog'ini o'rnatish., Ixtiyoriy og'ir funksiyani alohida fon oqimida bajaruvchi universal QThread., WorkerThread, QThread

### Community 61 - ".open_column_manager"
Cohesion: 0.16
Nodes (6): Any, QWidget, Senior-darajadagi muvozanatli 2x2 KPI statistika kartochkasi., Mavzuni Dark / Light rejimiga moslashtirish., Shartnomalar jadvaliga ustun qo'shish va boshqarish dialogi., Jadval ustunlari va sarlavhalarini baza + maxsus ustunlar bilan sozlash.

### Community 63 - ".on_table_double_clicked"
Cohesion: 0.20
Nodes (5): Tanlangan kataklarni Excel kabi Tab va Yangi qator bilan clipboardga nusxalash., Jadvalda klaviatura hodisalari: Enter (tahrir), Ctrl+C (nusxalash)., Saralash (sorting) hisobga olingan holda jadval qatoridagi elementni aniqlash., Jadvalda 2 marta bosilganda tahrirlash oynasini ochish., Tanlangan shartnoma ma'lumotini tahrirlash dialogi.

### Community 64 - ".load_data"
Cohesion: 0.33
Nodes (3): Bazada mavjud bo'lgan shartnoma ma'lumotlarini yuklash., KPI kartochkalaridagi umumiy sonlarni hisoblash., Yangi tashkilot / shartnoma ma'lumotini qo'shish dialogi.

### Community 65 - "extract_sheet_id"
Cohesion: 0.29
Nodes (4): extract_sheet_id(), is_service_account_available(), URL yoki matndan Google Sheet ID sini ajratib olish., Service account kalit fayli mavjud va to'g'ri ekanligini tekshirish.

## Knowledge Gaps
- **20 isolated node(s):** `graphify`, `Workflow: graphify`, `Enterprise Desktop Platformasi (v4.0 Pro)`, `📊 Asosiy Ko'rsatkichlar`, `🏢 1. Toifalar Qatorida Tezkor Tashkilot va Toifa Qo'shish (Quick Add Engine)` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DataManager` connect `export_organizations_to_excel` to `.__init__`, `DataManager`, `External Services (Excel, QR, GSheets)`, `UI Views Test Suite`, `MainWindow`, `TestDataManager`, `BroadcastView`, `setup_logger`, `clean_inn`, `sanitize_text`, `broadcast_service.py`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `TelegramBotService` connect `External Services (Excel, QR, GSheets)` to `CabinetDialog`, `OrgEditDialog`, `export_organizations_to_excel`, `Services Package Architecture`, `.add_organization`, `setup_logger`, `sanitize_text`, `broadcast_service.py`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `SQLiteManager` connect `DataManager` to `import_organizations_from_file`, `export_organizations_to_excel`, `TestDataManager`, `Organization`, `setup_logger`, `broadcast_service.py`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `MainWindow` (e.g. with `TestQtArchitecture` and `.test_view_imports()`) actually correct?**
  _`MainWindow` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `TableView` (e.g. with `MockApp` and `TestAddOrgPills`) actually correct?**
  _`TableView` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ContractsView` (e.g. with `MockApp` and `TestAddOrgPills`) actually correct?**
  _`ContractsView` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TelegramBotService` (e.g. with `DataManager` and `SearchService`) actually correct?**
  _`TelegramBotService` has 6 INFERRED edges - model-reasoned connections that need verification._