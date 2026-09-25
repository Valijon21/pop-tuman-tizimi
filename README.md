# 🏢 Pop Tuman Tashkilotlari va INN Tizimi (Enterprise Desktop Edition)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyQt5 Fluent UI](https://img.shields.io/badge/GUI-PyQt5%20Fluent%20Desktop-0284c7.svg)](https://riverbankcomputing.com/software/pyqt/)
[![SQLite WAL](https://img.shields.io/badge/Storage-SQLite%20WAL%20Dual--Sync-10b981.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-75%20Passed%20(100%25)-success.svg)](https://github.com/Valijon21/pop-tuman-tizimi)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Layered%20Offline--First-8b5cf6.svg)](https://github.com/Valijon21/pop-tuman-tizimi)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/Valijon21/pop-tuman-tizimi)

---

## 📌 Loyiha Haqida Umumiy Ma'lumot (Executive Summary)

**Pop Tuman Tashkilotlari va INN Tizimi** — Namangan viloyati Pop tumanidagi barcha davlat idoralari, Mahalla fuqarolar yig'inlari (74 ta MFY), umumta'lim maktablari, maktabgacha ta'lim tashkilotlari (MTT), tibbiyot muassasalari hamda korxona va tashkilotlar (jami **680+ ta tashkilot**) ma'lumotlarini markazlashtirilgan tarzda yuritish, shartnomalar va litsenziyalar kvotalari monitoringini olib borish, kadrlar rotatsiyasi tarixini qayd etish hamda tezkor tahlillarni amalga oshirish uchun ishlab chiqilgan **Senior-darajadagi korporativ Desktop dasturiy platformasi**.

Tizim to'liq **Offline-First** konsepsiyasida barpo etilgan bo'lib, internet aloqasi mavjud bo'lmagan sharoitda ham 100% quvvatda ishlaydi. Ma'lumotlar yaxlitligi (Data Integrity) yuqori tezlikdagi **SQLite (WAL rejimida)** va inson o'qiy oladigan atomik **JSON** formatidagi ikki tomonlama sinxronizatsiya qatlami orqali kafolatlanadi.

---

## 🏛 Tizim Arxitekturasi va Muhandislik Tamoyillari

Loyiha arxitekturasi **Domain-Driven Design (DDD)** va **Clean Architecture** tamoyillari asosida modulli qatlamlarga ajratilgan:

```
┌─────────────────────────────────────────────────────────────────┐
│               PRESENTATION LAYER (PyQt5 GUI)                    │
│  MainWindow | TableView | ContractsView | MahallaPassportView   │
│  SmartSearchCompleter | Fluent Stylesheet Generator (Dark/Light)│
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│               SERVICES & BUSINESS LOGIC LAYER                   │
│  SearchService (Cyrillic/Latin) | QRService (RFC/MeCard)        │
│  ExcelService | VerificationService | CabinetService            │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│             DATA ACCESS & REPOSITORY LAYER                      │
│  DataManager (Dual-Storage Coordinator)                         │
│  SQLiteManager (WAL Mode, Migration, Staff Audit History)       │
│  Data Models & Input Validators (INN, JSHSHIR, Phone, Passport) │
└────────────────────────────────┬────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                PERSISTENT PHYSICAL STORAGE                      │
│  mahalla_tizimi.db (SQLite)  │  mahalla_bazasi.json (Atomic)    │
│  backups/ (Rolling Daily Snapshot Archives)                     │
└─────────────────────────────────────────────────────────────────┘
```

### Arxitekturaning Asosiy Afzalliklari:
1. **0ms Kechikishsiz Navigatsiya (`_dirty_views` kesh tizimi):**
   Sahifalar o'rtasida o'tishda ma'lumotlar har safar noldan qayta o'qilmaydi. Faqat ma'lumotlar bazasida haqiqiy o'zgarish sodir bo'lgandagina tegishli sahifalar "ifloslangan" deb belgilanadi va yengil yangilanadi.
2. **ACID Kafolati va Dual-Storage Sinxronizatsiyasi:**
   Har bir CRUD amali bir vaqtning o'zida ham SQLite tranzaksiyasiga, ham atomik JSON fayliga yoziladi. To'satdan elektr ta'minoti uzilganda ham ma'lumotlarning yo'qolish xavfi nolga teng.
3. **Avtomatik Rolling Zaxiralash (Auto-Backup):**
   Dastur har 30 daqiqada va har safar xavfsiz yopilganda SQLite (`.db`) va JSON (`.json`) formatlaridagi to'liq zaxira nusxalarini `backups/` papkasiga arxivlaydi (oxirgi 20 ta nusxa avtomat nazorat qilinadi).

---

## ⚡ Asosiy Funksional Modullar

### 1. 🔍 Aqlli Ko'p Tokenli Qidiruv va Mos Nomlar Taklifi (Smart Search Engine)
* **Lotin ⇄ Kirill Ikki Tomonlama Transliteratsiyasi:**
  Foydalanuvchi qidiruv satriga `мактаб`, `чоркесар`, `ғўз` yoki `maktab`, `chorkesar`, `g'o'z` deb yozishidan qat'i nazar, tizim fonetik normalizatsiya orqali tashkilotlarni bir zumda topadi.
* **Mustaqil Token Qidiruvi (Order-Invariant Token Matching):**
  So'zlarning ketma-ketlik tartibi natijaga ta'sir qilmaydi (masalan: `"1 maktab"` va `"maktab 1"` bir xil yuqori aniqlikda filtrlanadi).
* **Oniy Interaktiv Takliflar (`SmartSearchCompleter`):**
  Bosh jadval, shartnomalar monitoringi va rotatsiya tarixi oynalaridagi har bir qidiruv maydoni aqlli lug'at bilan boyitilgan. 1-2 harf kiritilishi bilanoq mos tashkilot nomlari, INN raqamlari va mas'ul shaxslar qulay Fluent dropdown popup shaklida taklif qilinadi.
* **Raqamli Matn Ajratmasi:**
  Nom ichidagi raqamlar (masalan: `"15-sonli bog'cha"`) telefon raqamlari bilan adashib ketmasligi uchun aqlli parametrlar ajratilgan.

### 2. 📑 Shartnoma va Ulanishlar Monitoringi (Professional Matritsa)
* **9 Ustunli To'liq Analitik Jadval:**
  `№` | `Tashkilot Nomi` | `INN` | `Toifasi` | `Apparat SHT` | `Ulangan` | `Litsenziya Holati` | `Rahbar Tel` | `Buxgalter Tel`
* **Interaktiv Raqamli va Matnli Saralash (`NumericTableWidgetItem`):**
  Ustun sarlavhasini bosganda sonlar satr ko'rinishida emas, matematik qiymati bo'yicha to'g'ri o'sish/kamayish tartibida saralanadi (masalan: `2 < 10 < 100`).
* **Avtomatik Qator Raqamlash (№):**
  Jadval saralanganda yoki filtrlanganda qator tartib raqamlari 1 dan boshlab avtomatik ravishda qayta tekislanadi.
* **Litsenziyalar Kvotasi Holat Nishonlari:**
  - `✅ To'liq ({ulangan}/{aparat})` — apparat shtati va ulangan litsenziyalar soni to'liq teng (yashil nishon).
  - `⚠️ Kamomad: -{diff}` — litsenziya soni apparat shtatiga yetmayotgan tashkilotlar (saralashda yuqori ustuvorlik, to'q sariq ogohlantirish).
  - `🔷 Ortiqcha (+{diff})` — me'yordan ortiq ulangan tashkilotlar (binafsharang).
  - `⚪ 0 / 0` yoki `⚪ Ma'lumotsiz` — ko'rsatkich kiritilmagan yozuvlar.
* **Erkin Katak Tanlash va Nusxalash:**
  `SelectItems` va `ExtendedSelection` arxitekturasi orqali jadvaldan istalgan kataklar blokini sichqoncha bilan belgilab, `Ctrl+C` yordamida to'g'ridan-to'g'ri Excel yoki matnli hujjatlarga nusxalash imkoniyati.
* **9 Ustunli Professional Excel Eksporti:**
  Monitoring natijalarini to'liq ko'rsatkichlari bilan bir zumda `.xlsx` formatida yuklab olish.

### 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti
* Pop tumanining barcha 74 ta MFYlari bo'yicha 7 ta asosiy mas'ul xodim profili:
  `Rais`, `Hokim yordamchisi`, `Yoshlar yetakchisi`, `Xotin-qizlar faoli`, `Profilaktika inspektori`, `Soliq inspektori`, `Ijtimoiy xodim`.
* Har bir xodim uchun shaxsiy telefon, passport/JSHSHIR va lavozim ma'lumotlari.
* **Avtomatlashtirilgan Shablon Generatori:**
  Bir bosishda **"Verifikatsiya so'rovi"** va **"Kabinetga dostup"** rasmiy shablon matnlarini generatsiya qilish va Telegram orqali yuborish.

### 4. 📇 Kontakt QR-kod Standartlari (Xalqaro Muvofiqlik)
* **Toza E.164 Telefon Formati:**
  Skanerlar va telefon apparatlari raqamni noto'g'ri terishini (masalan, ortiqcha ichki kodlar qo'shilib qolishini) oldini oluvchi toza `+998XXXXXXXXX` standarti.
* **NTT DoCoMo MeCard & RFC 2426 vCard 3.0:**
  Har qanday Android va iOS qurilmalari skan qilganda to'g'ridan-to'g'ri "Kontaktga saqlash" oynasini ochuvchi universal QR generatori.

### 5. 📜 Kadrlar Rotatsiyasi Tarixi (Audit Trail)
* Tashkilot yoki mahallada mas'ul xodim o'zgarganda tizim orqa fonda avtomatik audit yozuvini yaratadi:
  - O'zgarish sanasi va aniq vaqti
  - Tashkilot / Mahalla nomi
  - Lavozim turi
  - Eski xodim F.I.SH. va telefon raqami
  - Yangi xodim F.I.SH. va telefon raqami
* Rotatsiya tarixida tezkor qidiruv, takliflar va hisobotlarni ko'rish oynasi.

### 6. 🛠 Yordamchi Dasturlar va Tizim Integratsiyasi (Tools Panel)
* Tashkilotlar bilan ishlashda kerak bo'ladigan tashqi yordamchi dasturlar:
  - **UzCrypto** (E-Imzo va soliq sertifikatlari)
  - **AnyDesk** (Tezkor masofaviy yordam)
* Bitta tugma orqali dastur papkasini ochish yoki dasturni tizim almashish buferiga (clipboard) nusxalash (`Ctrl+V` orqali istalgan joyga joylash).

---

## 🎨 UI/UX Dizayn Tizimi (PyQt5 Modern Fluent UI)

* **Adaptiv QSS Stil Tizimi:** [ui_qt/styles.py](file:///d:/programming/tashkilotlar%20INN%20tizim/ui_qt/styles.py) dagi ranglar palitrasi orqali boshqariladi.
* **Tungi (Dark) va Kunduzgi (Light) Rejimlar:** Ko'zga qulay kontrast, zamonaviy fon ranglari (`#0f172a` va `#f8fafc`), nozik chegaralar va kartalar soyalari.
* **Shrift Masshtablash (Accessibility):** Dastur interfeysi 11px dan 16px gacha bo'lgan o'lchamlarda matn buzilmasdan erkin masshtablanadi.
* **Yuqori DPI (High-DPI Scaling):** 2K/4K monitorlar hamda noutbuk ekranlarida (100%, 125%, 150%) barcha tugmalar, piktogrammalar va logotiplar ravshan aks etadi.

---

## 📂 Loyiha Katalog Tuzilishi

```
pop-tuman-tizimi/
├── main.py                     # Asosiy kirish nuqtasi (PyQt5 GUI bootstrap)
├── main_qt.py                  # PyQt5 uchun tezkor ishga tushirish moduli
├── mahalrai_POP.py             # 100% orqaga moslik integratsiya adapteri
├── requirements.txt            # Python tashqi bog'liqliklari
├── run_tests.py                # Avtomatlashtirilgan regressiya testlari (75 ta test)
├── build_exe.py                # Standalone Windows .exe yig'uvchi skript
├── mahalla_tizimi.db           # SQLite asosiy ma'lumotlar bazasi (WAL)
├── mahalla_bazasi.json         # Atomik JSON sinxronizatsiya ma'lumotlar bazasi
│
├── core/                       # Yadro tizim moduli
│   ├── config.py               # Ranglar, toifalar va doimiy parametrlar
│   ├── logger.py               # Loglarni faylga va konsolga yozish tizimi
│   ├── security.py             # SHA-256 xesh va parollar xavfsizligi
│   └── validators.py           # INN (9 xonali), JSHSHIR, telefon va pasport tekshiruvi
│
├── database/                   # Ma'lumotlar boshqaruvi qatlami
│   ├── models.py               # Organization obyekti modeli va tipizatsiyasi
│   ├── data_manager.py         # Dual-storage boshqaruvchisi va kesh koordinatori
│   └── sqlite_manager.py       # SQLite WAL mode, schema migratsiyalari va audit jadvallari
│
├── services/                   # Tashqi va analitik xizmatlar
│   ├── search_service.py       # Lotin-Kirill transliteratsiyasi va ko'p tokenli aqlli qidiruv
│   ├── qr_service.py           # E.164, MeCard va RFC 2426 vCard QR generatori
│   ├── excel_service.py        # 9 ustunli Excel (.xlsx, .xls) va CSV import/export
│   ├── sync_contracts_data.py  # Shartnomalar va buxgalterlar ma'lumotlarini birlashtirish
│   ├── sync_excel_data.py      # MFY yettiligi ma'lumotlarini sinxronlash
│   ├── broadcast_service.py    # Ommaviy xabarnomalar xizmati
│   ├── telegram_service.py     # Telegram Bot API xabarnoma integratsiyasi
│   ├── verification_service.py # Verifikatsiya so'rovi shablon generatori
│   └── cabinet_service.py      # Kabinetga dostup rasmiy shablon generatori
│
├── ui_qt/                      # Foydalanuvchi grafik interfeysi (PyQt5)
│   ├── app_window.py           # Asosiy oyna (MainWindow, navigatsiya, xavfsiz yopilish)
│   ├── styles.py               # Dynamic Fluent Dark/Light QSS generatori
│   ├── components/             # Qayta ishlatiluvchi komponentlar
│   │   ├── smart_completer.py  # Aqlli qidiruv avto-takliflar komponenti
│   │   ├── table_model.py      # Yuqori tezlikdagi QAbstractTableModel
│   │   └── charts.py           # Donut Chart va Horizontal Bar Chart
│   └── views/                  # Ko'rinishlar (Views) va Modallar
│       ├── dashboard_view.py   # Analitik KPI paneli va interaktiv diagrammalar
│       ├── table_view.py       # Tashkilotlar bosh jadvali va filtrlar
│       ├── contracts_view.py   # Shartnoma va ulanishlar 9 ustunli monitoringi
│       ├── mahalla_passport_view.py # Mahalla "Yettiligi" 360° profili
│       ├── org_edit_dialog.py  # Tashkilot qo'shish va tahrirlash oynasi
│       ├── history_view.py     # Kadrlar rotatsiyasi tarixi dialogi
│       ├── settings_view.py    # Sozlamalar va zaxira nusxalar paneli
│       ├── trash_view.py       # Chiqindi qutisi (Recycle Bin - qayta tiklash bilan)
│       └── import_dialog.py    # Excel/CSV ommaviy import dialogi
│
└── tests/                      # Keng qamrovli testlar to'plami (75 ta test)
    ├── test_services.py        # Aqlli qidiruv, QR standartlari va xizmatlar testlari
    ├── test_validators.py      # INN, telefon va kiritish tekshiruvlari testlari
    ├── test_models.py          # Organization modeli testlari
    ├── test_sqlite.py          # SQLite WAL, tranzaksiyalar va audit log testlari
    ├── test_security.py        # Parollar va xavfsizlik testlari
    ├── test_import.py          # Excel va CSV import/export testlari
    ├── test_qt_views.py        # PyQt5 ko'rinishlari va komponentlar testlari
    └── test_ui_ux_deep.py      # Chuqur UI/UX, navigatsiya va hodisalar testlari
```

---

## 🚀 O'rnatish va Ishga Tushirish

### 1. Tizim talablari
* **Operatsion tizim:** Windows 10 yoki Windows 11 (64-bit)
* **Python versiyasi:** Python 3.10 yoki undan yuqori

### 2. Repozitoriyni yuklab olish
```bash
git clone https://github.com/Valijon21/pop-tuman-tizimi.git
cd pop-tuman-tizimi
```

### 3. Virtual muhitni yoqish va bog'liqliklarni o'rnatish
```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Dasturni ishga tushirish
```bash
python main.py
```
*(Eski skriptlar bilan moslik uchun `python mahalrai_POP.py` ham to'liq quvvatda ishlaydi).*

---

## 🧪 Avtomatlashtirilgan Sifat Nazorati (Testing)

Loyiha barqarorligi va regressiya xatolarining oldini olish uchun 75 ta avtomatlashtirilgan test ishlab chiqilgan:

```bash
python run_tests.py
```

Test hisoboti:
```text
Ran 75 tests in ~67s
OK - BARCHA TESTLAR MUVAFFAQIYATLI O'TDI! (75 ta test)
```

Qamrov sohalari:
* **Validation & Security:** INN, JSHSHIR, telefon, xeshlar va rate limiting.
* **Database & ACID:** SQLite WAL tranzaksiyalari, sxema migratsiyasi, audit tarixi va zaxiralar.
* **Services & Algorithms:** Lotin-Kirill transliteratsiyasi, ko'p tokenli qidiruv, E.164 va vCard 3.0 QR generatsiyasi.
* **PyQt5 UI/UX:** Barcha oynalar inisializatsiyasi, mavzular almashtirilishi, shrift masshtabi va hodisalar uzatilishi.

---

## 🔒 Xavfsizlik va Maxfiylik

1. **Maxfiy Kalitlar Izolyatsiyasi:**
   Barcha shaxsiy sozlamalar (`settings.json`), bulut kalitlari (`service_account.json`) va tizim loglari `.gitignore` orqali repozitoriyga chiqib ketishdan himoyalangan.
2. **Kadrlar Audit Tizimi:**
   Har qanday kadr o'zgarishi qayd qilinib boriladi, hech bir ma'lumot izsiz o'chirilmaydi (Soft-delete orqali chiqindi qutisiga tushadi va xohlagan vaqtda qayta tiklanishi mumkin).

---

## 👨‍💻 Muallif va Texnik Qo'llab-quvvatlash

* **Muallif va Ishlab chiquvchi:** Valijon
* **Versiya:** 4.0 Pro Enterprise Edition
* **Platforma:** Windows Desktop (PyQt5 + SQLite WAL)
* **Hudud:** Namangan viloyati, Pop tumani
