# 🏢 Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5%20Fluent%20UI-0284c7.svg)](https://riverbankcomputing.com/software/pyqt/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20WAL%20(Dual--Storage)-10b981.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-75%20Passed%20(100%25)-success.svg)](https://github.com/Valijon21/pop-tuman-tizimi)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/Valijon21/pop-tuman-tizimi)

**Pop Tuman Tashkilotlari va INN Tizimi** — Pop tumanidagi barcha 680+ ta tashkilot, mahalla fuqarolar yig'inlari (MFY), maktablar, maktabgacha ta'lim tashkilotlari (MTT), tibbiyot muassasalari va boshqa davlat idoralari ma'lumotlarini markazlashtirilgan tarzda boshqarish, tahlil qilish hamda monitoring olib borish uchun maxsus ishlab chiqilgan yuqori tezlikdagi professional **Desktop dasturiy ta'minot**.

![Dashboard Screenshot](popdata.png)

---

## 🌟 Versiya 4.0 Pro Asosiy Imkoniyatlari

### 1. 🔍 Aqlli Qidiruv va Avto-taklif Tizimi (Smart Search & Auto-complete)
* **Lotin va Kirill transliteratsiyasi:** Qidiruv so'rovi istalgan alifboda kiritilganda birdek topadi (masalan: `maktab` ⇄ `мактаб`, `chorkesar` ⇄ `чоркесар`, `g'o'z` ⇄ `ғўз`).
* **Tartibga bog'liq bo'lmagan ko'p tokenli qidiruv:** So'zlarning joylashuv tartibidan qat'i nazar aniq moslikni aniqlash (masalan: `"1-maktab"` yoki `"maktab 1"` bir xil natija beradi).
* **Interaktiv Takliflar (`SmartSearchCompleter`):** Bosh jadval, shartnomalar va rotatsiya tarixi bo'limlarida harf kiritilishi bilan mos keluvchi tashkilot nomlari, INNlar va telefon raqamlari qulay popup menyuda taklif qilinadi.
* **Mavzuga moslashuvchan dizayn:** Dark va Light mavzulari uchun maxsus Fluent UI qidiruv dropdowni.

### 2. 📑 Shartnoma & Ulanishlar Monitoringi (Professional Tartiblangan Jadval)
* **9 ustunli to'liq ma'lumotlar jadvali:**
  `№`, `Tashkilot Nomi`, `INN`, `Toifasi`, `Apparat SHT`, `Ulangan`, `Litsenziya Holati`, `Rahbar Tel`, `Buxgalter Tel`.
* **Ustunlar bo'yicha interaktiv saralash (Interactive Sorting):**
  Raqamli (`NumericTableWidgetItem`) va matnli ustunlar boshini bosganda to'g'ri o'sish/kamayish tartibida saralanadi.
* **Avtomatik tartib raqamlarini yangilash:** Jadval saralanganda yoki filtrlanganda `№` ustuni avtomatik tarzda ketma-ket (1, 2, 3...) tekislanadi.
* **Litsenziya Holati Rangli Ko'rsatkichlari:**
  - `✅ To'liq ({ulangan}/{aparat})` — apparat va ulangan xodimlar to'liq mos kelganda.
  - `⚠️ Kamomad: -{diff}` — ulanishlar apparat shtatidan kam bo'lganda (saralashda yuqori ustuvorlik).
  - `🔷 Ortiqcha (+{diff})` — litsenziya me'yordan ortiq ulanganda.
  - `⚪ 0 / 0` yoki `⚪ Ma'lumotsiz` — ko'rsatkichlar kiritilmaganda.
* **Erkin katak tanlash va Ctrl+C:** Jadvaldan bir nechta katak yoki qatorlarni belgilab, to'g'ridan-to'g'ri nusxalash (`ExtendedSelection`).
* **9 ustunli professional Excel eksporti:** Barcha tahliliy ustunlarni to'g'ridan-to'g'ri `.xlsx` formatida yuklab olish.

### 3. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)
* **Dark & Light Mavzular:** Tungi va kunduzgi rejimlar o'rtasida bir zumda almashtirish. Barcha modallar, oynalar, kartalar va inputlar yuqori kontrastli va ko'zga qulay.
* **0ms Kechikishsiz Navigatsiya (`_dirty_views` kesh):** Sahifalar o'rtasida o'tishda ma'lumotlar qayta yuklanmasdan oniy va silliq ochiladi.
* **Yuqori DPI Moslashuvchanlik:** Har qanday ekran o'lchamlari va masshtablarida (100%, 125%, 150%) elementlar va logolar tiniq va mutanosib ko'rinadi.
* **Yordamchi Dasturlar Paneli:** UzCrypto va AnyDesk uchun tezkor ishga tushirish, fayl joylashgan papkani ochish va faylni tizim buferiga nusxalash (`Ctrl+V` bilan istalgan joyga qo'yish).

### 4. 📇 Kontakt QR-kod Standartlari (RFC & MeCard)
* **Toza E.164 telefon formati:** Telefon skanerlari xato raqam terib qo'ymasligi uchun ortiqcha prefikslarsiz standart xalqaro `+998...` formatida generatsiya.
* **NTT DoCoMo MeCard & RFC 2426 vCard:** Android va iOS qurilmalari bilan 100% mos to'liq kontakt kartochkasi.

### 5. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti
* Pop tumanining barcha 74 ta MFYlari bo'yicha 7 ta asosiy mas'ul xodim (Rais, Hokim yordamchisi, Yoshlar yetakchisi, Xotin-qizlar faoli, Profilaktika inspektori, Soliq inspektori, Ijtimoiy xodim) profili.
* Bir bosishda **"Verifikatsiya so'rovi"** va **"Kabinetga dostup"** shablon matnlarini generatsiya qilish va Telegram orqali yuborish.

### 6. 💾 SQLite WAL Dual-Storage (ACID Kafolati)
* **Ikki tomonlama sinxronizatsiya:** Yuqori tezlikdagi SQLite (WAL rejimida) hamda inson o'qiy oladigan atomik `mahalla_bazasi.json`.
* Tizim to'satdan o'chib qolganda ham ma'lumotlar 100% buzilmasdan saqlanadi.
* Avtomatik zaxira nusxalash (`backups/` papkasida `.db` va `.json` formatida).

### 7. 📜 Kadrlar Almashinuvi va Rotatsiyasi Tarixi (Audit Log)
* Har qanday lavozim egasi o'zgarganda SQLite audit jadvalida vaqt, sana, eski xodim va yangi xodim nomi avtomatik saqlanib boriladi.
* Tarix oynasida ham tezkor aqlli qidiruv va mos nomlarni taklif qilish integratsiyalangan.

### 8. 📥 Excel & CSV Ommaviy Import / Eksport
* Tashqi Excel (`.xlsx`, `.xls`) va CSV fayllarni qisqa soniyalarda tizimga kiritish va tahlil qilish.
* Butun ma'lumotlar bazasini bitta tugma orqali Excel jadvaliga eksport qilish.

---

## 📁 Loyiha Arxitekturasi

```
pop-tuman-tizimi/
├── main.py                     # Asosiy kirish nuqtasi (PyQt5 Modern GUI)
├── main_qt.py                  # PyQt5 uchun qisqa ishga tushirish skripti
├── mahalrai_POP.py             # 100% orqaga moslik uchun adapter
├── requirements.txt            # Bog'liqliklar ro'yxati
├── run_tests.py                # Avtomatlashtirilgan test tizimi (75 ta test)
├── build_exe.py                # Windows .exe mustaqil dasturini yig'ish
│
├── core/                       # Yadro va biznes mantig'i
│   ├── config.py               # Konfiguratsiya, ranglar va doimiylar
│   ├── logger.py               # Log yuritish tizimi (RotatingFileHandler)
│   ├── security.py             # SHA-256 xeshlash va parollar xavfsizligi
│   └── validators.py           # INN, JSHSHIR, telefon va pasport seriya validatsiyasi
│
├── database/                   # Ma'lumotlar qatlami
│   ├── models.py               # Organization ma'lumotlar modeli va validatsiyasi
│   ├── data_manager.py         # Dual-storage boshqaruvchisi (SQLite + JSON)
│   └── sqlite_manager.py       # SQLite WAL mode, schema migratsiyasi, audit tarixi
│
├── services/                   # Yordamchi xizmatlar va integratsiyalar
│   ├── broadcast_service.py    # Ommaviy xabarnomalar xizmati
│   ├── cabinet_service.py      # Kabinet dostup shablon generatsiyasi
│   ├── excel_service.py        # Excel (.xlsx, .xls) va CSV import/export
│   ├── qr_service.py           # E.164, MeCard va vCard QR-kod generatsiyasi
│   ├── search_service.py       # Ko'p parametrli tezkor aqlli qidiruv (Lotin-Kirill)
│   ├── sync_contracts_data.py  # Shartnomalar va buxgalter kontaktlari sinxronizatori
│   ├── sync_excel_data.py      # Mahalla yettiligi va xodimlar sinxronizatori
│   ├── telegram_service.py     # Telegram Bot API integratsiyasi
│   └── verification_service.py # Xodim verifikatsiyasi shablon xizmati
│
├── ui_qt/                      # PyQt5 Zamonaviy Foydalanuvchi Interfeysi
│   ├── app_window.py           # Asosiy oyna (MainWindow, Sidebar, Navigation)
│   ├── styles.py               # Dark va Light mavzulari uchun Fluent QSS tizimi
│   ├── components/             # Qayta ishlatiluvchi grafik komponentlar
│   │   ├── charts.py           # Donut Chart, Horizontal Bar Chart, Legend
│   │   ├── smart_completer.py  # Aqlli qidiruv takliflari (SmartSearchCompleter)
│   │   └── table_model.py      # QAbstractTableModel (60fps tejamkor jadval)
│   └── views/                  # Ekranning alohida sahifalari va modallar
│       ├── dashboard_view.py   # Statistik tahlil paneli va grafiklar
│       ├── table_view.py       # Tashkilotlar bosh jadvali, aqlli qidiruv va filtrlar
│       ├── contracts_view.py   # Shartnoma & Ulanishlar monitoringi (9 ustunli)
│       ├── mahalla_passport_view.py # Mahalla "Yettiligi" 360° pasporti
│       ├── org_edit_dialog.py  # Tashkilot qo'shish / tahrirlash oynasi
│       ├── cabinet_dialog.py   # Kabinetga dostup tezkor dialogi
│       ├── verification_dialog.py # Verifikatsiya so'rovi dialogi
│       ├── broadcast_view.py   # Ommaviy xabarnoma yuborish dialogi
│       ├── history_view.py     # Kadrlar rotatsiyasi tarixi dialogi
│       ├── import_dialog.py    # Excel/CSV import dialogi
│       ├── settings_view.py    # Sozlamalar va zaxira nusxalar sahifasi
│       └── trash_view.py       # Chiqindi qutisi (Recycle Bin)
│
└── tests/                      # Avtomatlashtirilgan testlar to'plami (75 ta test)
    ├── test_qt_views.py        # PyQt5 ko'rinishlari, mavzulari va modellari testlari
    ├── test_ui_ux_deep.py      # Chuqur UI/UX, navigatsiya va render testlari
    ├── test_sqlite.py          # SQLite tranzaksiyalari va zaxiralar testlari
    ├── test_models.py          # Modellar va maydonlar testlari
    ├── test_services.py        # Tashqi xizmatlar, aqlli qidiruv va QR testlari
    ├── test_validators.py      # INN, JSHSHIR, telefon validatsiyasi testlari
    ├── test_security.py        # Xavfsizlik testlari
    └── test_import.py          # Import va eksport testlari
```

---

## 💻 O'rnatish va Ishga Tushirish

### 1. Repozitoriyni klonlash
```bash
git clone https://github.com/Valijon21/pop-tuman-tizimi.git
cd pop-tuman-tizimi
```

### 2. Virtual muhit yaratish va kutubxonalarni o'rnatish
```bash
python -m venv venv
# Windows uchun faollashtirish:
venv\Scripts\activate

# Kutubxonalarni o'rnatish:
pip install -r requirements.txt
```

### 3. Dasturni ishga tushirish
```bash
python main.py
```
*Yoki orqaga moslik buyrug'i:*
```bash
python mahalrai_POP.py
```

---

## 🧪 Avtomatlashtirilgan Testlar

Loyiha barqarorligini tekshirish uchun:
```bash
python run_tests.py
```
Natija:
```
Ran 75 tests in ~67s
OK - BARCHA TESTLAR MUVAFFAQIYATLI O'TDI! (75 ta test)
```


---

## 📦 Mustaqil Windows `.exe` Dasturini Yig'ish

Python o'rnatilmagan kompyuterlar uchun bitta mustaqil `.exe` yig'ish:
```bash
python build_exe.py
```
Yig'ilgan fayl `dist/PopTumanTizimi/PopTumanTizimi.exe` manzilida hosil bo'ladi.

---

## 🛡 Xavfsizlik va Ma'lumotlar Maxfiyligi

* Google Cloud kalitlari (`service_account.json`), lokal sozlamalar (`settings.json`) va shaxsiy loglar `.gitignore` orqali repozitoriyga kirmaydi.
* Namunaviy kalit fayli sifatida `service_account.json.example` taqdim etilgan.
* Barcha ma'lumotlar bazasi zaxiralari avtomatik ravishda `backups/` papkasiga saqlanadi.

---

## 📞 Muallif

* **Muallif:** Valijon
* **Versiya:** 4.0 Pro Enterprise Edition
* **Moslik:** Windows 10 / 11 (64-bit)
