# 🏢 Pop Tuman Tashkilotlari va INN Tizimi (v4.0 Pro Enterprise)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5%20Fluent%20UI-0284c7.svg)](https://riverbankcomputing.com/software/pyqt/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20WAL%20(Dual--Storage)-10b981.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-73%20Passed%20(100%25)-success.svg)](https://github.com/Valijon21/pop-tuman-tizimi)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](https://github.com/Valijon21/pop-tuman-tizimi)

**Pop Tuman Tashkilotlari va INN Tizimi** — Pop tumanidagi barcha 680+ ta tashkilot, mahalla fuqarolar yig'inlari (MFY), maktablar, maktabgacha ta'lim tashkilotlari (MTT), tibbiyot muassasalari va boshqa davlat idoralari ma'lumotlarini markazlashtirilgan tarzda boshqarish, tahlil qilish hamda monitoring olib borish uchun maxsus ishlab chiqilgan yuqori tezlikdagi professional **Desktop dasturiy ta'minot**.

![Dashboard Screenshot](popdata.png)

---

## 🌟 Versiya 4.0 Pro Asosiy Imkoniyatlari

### 1. 🖥 PyQt5 Modern Fluent UI (Senior Desktop Edition)
* **Dark & Light Mavzular:** Tungi va kunduzgi rejimlar o'rtasida bir zumda almashtirish. Barcha modallar, oynalar, kartalar va inputlar kontrastli va ko'zga qulay qilib ishlangan.
* **0ms Kechikishsiz Navigatsiya (`_dirty_views` kesh):** Sahifalar o'rtasida o'tishda ma'lumotlar qayta yuklanmasdan oniy va silliq ochiladi.
* **Yuqori DPI Moslashuvchanlik:** Har qanday ekran o'lchamlari va masshtablarida (100%, 125%, 150%) elementlar tiniq va ixcham ko'rinadi.

### 2. 📑 Shartnoma & Ulanishlar Monitoringi (Yangi)
* **232 ta tashkilot shartnomasi:** Shartnoma raqamlari, apparat xodimlari soni, litsenziyalar / ulangan xodimlar kvotasi.
* **218+ ta Buxgalter aloqa bazasi:** Har bir tashkilotning buxgalter telefon raqami ro'yxati va bir bosishda nusxalash amallari.
* **Interaktiv KPI Kartalari:** Shartnomalar soni, apparat shtati, ulangan xodimlar va mavjud buxgalter kontaktlari bo'yicha dinamik tahlil.

### 3. 🏘 Mahalla "Yettiligi" 360° Raqamli Pasporti
* Pop tumanining barcha 74 ta MFYlari bo'yicha 7 ta asosiy mas'ul xodim (Rais, Hokim yordamchisi, Yoshlar yetakchisi, Xotin-qizlar faoli, Profilaktika inspektori, Soliq inspektori, Ijtimoiy xodim) profili.
* Bir bosishda **"Verifikatsiya so'rovi"** va **"Kabinetga dostup"** shablon matnlarini generatsiya qilish va Telegram orqali yuborish.

### 4. 💾 SQLite WAL Dual-Storage (ACID Kafolati)
* **Ikki tomonlama sinxronizatsiya:** Yuqori tezlikdagi SQLite (WAL rejimida) hamda inson o'qiy oladigan atomik `mahalla_bazasi.json`.
* Tizim to'satdan o'chib qolganda ham ma'lumotlar 100% buzilmasdan saqlanadi.
* Avtomatik zaxira nusxalash (`backups/` papkasida `.db` va `.json` formatida).

### 5. 📢 Ommaviy Xabarnoma Tarqatish Tizimi
* Tanlangan toifalar (Barcha mahallalar, faqat raislar, hokim yordamchilari, maktablar) bo'yicha tezkor xabar tarqatish.
* Telegram Bot API va SMS integratsiyasi.

### 6. 📜 Kadrlar Almashinuvi va Rotatsiyasi Tarixi (Audit Log)
* Har qanday lavozim egasi o'zgarganda SQLite audit jadvalida vaqt, sana, eski xodim va yangi xodim nomi avtomatik saqlanib boriladi.

### 7. 📥 Excel & CSV Ommaviy Import / Eksport
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
├── run_tests.py                # Avtomatlashtirilgan test tizimi (56 ta test)
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
│   ├── qr_service.py           # Operativ xotirada QR-kod generatsiyasi
│   ├── search_service.py       # Ko'p parametrli tezkor qidiruv xizmati
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
│   │   └── table_model.py      # QAbstractTableModel (60fps tejamkor jadval)
│   └── views/                  # Ekranning alohida sahifalari va modallar
│       ├── dashboard_view.py   # Statistik tahlil paneli va grafiklar
│       ├── table_view.py       # Tashkilotlar bosh jadvali va filtrlar
│       ├── contracts_view.py   # Shartnoma & Ulanishlar monitoringi
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
└── tests/                      # Avtomatlashtirilgan testlar to'plami
    ├── test_qt_views.py        # PyQt5 ko'rinishlari, mavzulari va modellari testlari
    ├── test_sqlite.py          # SQLite tranzaksiyalari va zaxiralar testlari
    ├── test_models.py          # Modellar va maydonlar testlari
    ├── test_services.py        # Tashqi xizmatlar testlari
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
Ran 56 tests in ~7s
OK - BARCHA TESTLAR MUVAFFAQIYATLI O'TDI! (56 ta test)
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
