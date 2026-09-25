<div align="center">

# 🏢 Pop Tuman Tashkilotlari va INN Tizimi
### Enterprise Desktop Platformasi (v4.0 Pro)

Namangan viloyati Pop tumanidagi davlat idoralari, MFYlar, maktablar, bog'chalar va tibbiyot muassasalari ma'lumotlarini boshqarish, monitoring qilish va tahlil qilish uchun yagona korporativ tizim.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/GUI-PyQt5%20Fluent-0284c7?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/Storage-SQLite%20WAL-10b981?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite WAL">
  <img src="https://img.shields.io/badge/Tests-80%20Passed%20(100%25)-success?style=for-the-badge&logo=githubactions&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/OS-Windows%2010%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows 10/11">
</p>

</div>

---

## 📊 Asosiy Ko'rsatkichlar

| 🏢 Jami Tashkilotlar | 🏘 Mahalla Pasportlari | 📑 Shartnoma & Monitoring | ⚡ Ishlash Rejimi | 🛡 Ma'lumotlar Birligi |
| :---: | :---: | :---: | :---: | :---: |
| **680+ ta** | **74 ta MFY (Yettilik)** | **232 ta shartnoma** | **100% Offline-First** | **SQLite WAL + Dual JSON** |

---

## 🌟 Asosiy Imkoniyatlar

### ⚙️ 1. Professional Dinamik Ustunlar Menejeri (Column Manager)
* **Tashkilotlar va Shartnomalar jadvaliga erkin ustun qo'shish:**
  * **Tizim maydonlari:** Buxgalter tel, Apparat shtat soni, Ulangan apparatlar, Rahbar lavozimi, JSHSHIR, Pasport seriya kabi maydonlarni bitta bosishda yoqish/o'chirish.
  * **Maxsus yangi ustunlar:** Istalgan yangi ustun yaratish (nomi, kengligi va kalitini belgilagan holda, masalan: *Shartnoma sanasi*, *Manzil*, *Email*, *Qo'shimcha izoh*).
* **Avtomatik SQLite Sxema Migratsiyasi:** Yangi ustun qo'shilishi bilan SQLite bazasida `ALTER TABLE` orqali to'liq struktura yangilanadi va ma'lumotlar doimiy saqlanadi.
* **Inline Katak Tahrirlash (In-Place Edit):** Jadvaldagi yangi ustunlar yoki izoh ustuniga sichqoncha bilan ikki marta bosib to'g'ridan-to'g'ri o'zgartirish va `Enter` orqali saqlash.
* **Dinamik Excel Eksport:** Qo'shilgan barcha maxsus ustunlar avtomatik ravishda Excel hisobotiga qo'shiladi.

### 🔍 2. Aqlli Qidiruv va Mos Nomlar Taklifi (Smart Search Engine)
* **Lotin ⇄ Kirill Transliteratsiyasi:** Qidiruv maydonida so'z qaysi alifboda yozilishidan qat'i nazar (`maktab` yoki `мактаб`, `chorkesar` yoki `чоркесар`) tashkilot bir zumda topiladi.
* **Mustaqil Ko'p Tokenli Qidiruv:** So'zlar tartibi natijaga xalaqit qilmaydi (`"1 maktab"` = `"maktab 1"`).
* **Interaktiv Takliflar (`SmartSearchCompleter`):** Qidiruv kiritilishi bilan mos keluvchi nomlar, INNlar va telefonlar chiroyli Fluent popup menyusida oniy taklif etiladi.

### 📑 3. Shartnoma va Ulanishlar Monitoringi
* **Interaktiv Jadval & Dinamik Ustunlar:** `№`, `Tashkilot Nomi`, `INN`, `Toifasi`, `Apparat SHT`, `Ulangan`, `Rahbar Tel`, `Buxgalter Tel` + istalgan maxsus ustunlar.
* **Professional Raqamli Saralash:** Ustun bosilganda raqamlar matn emas, matematik qiymati bo'yicha to'g'ri tartiblanadi (`NumericTableWidgetItem`).
* **Kataklar Bo'yicha Erkin Nusxalash:** Istalgan kataklarni belgilab, `Ctrl+C` orqali to'g'ridan-to'g'ri nusxalash imkoniyati (`ExtendedSelection`).
* **Excel Eksport:** Barcha ma'lumotlarni (yangi qo'shilgan ustunlar bilan birga) bir bosishda `.xlsx` faylga saqlash.

### 🏘 4. Mahalla "Yettiligi" 360° Raqamli Pasporti
* Pop tumanining 74 ta MFYsi bo'yicha mas'ul rahbarlar: Rais, Hokim yordamchisi, Yoshlar yetakchisi, Xotin-qizlar faoli, Profilaktika inspektori, Soliqchi va Ijtimoiy xodim.
* Bir bosishda **"Verifikatsiya so'rovi"** va **"Kabinetga dostup"** rasmiy shablonlarini generatsiya qilish va Telegram orqali yuborish.

### 📇 5. Xalqaro Aloqa va QR Standartlari
* **Toza E.164 Formati:** Raqamlarda xato prefikslar qo'shilishining oldini oluvchi toza `+998...` standarti.
* **Universal QR-kodlar:** Android va iOS qurilmalari bilan to'liq mos NTT DoCoMo MeCard va RFC 2426 vCard 3.0 kontakt kartochkalari.

### 💾 6. Dual-Storage & Avtomatik Zaxiralash
* **ACID Kafolati:** Har bir amal SQLite (WAL rejimida) hamda atomik JSON fayliga birdek yoziladi.
* **Avto-zaxira (Rolling Backups):** Har 30 daqiqada va dastur yopilganda SQLite (`.db`) va JSON (`.json`) nusxalari avtomatik arxivlanadi.

### 🛠 7. Yordamchi Dasturlar (Tools)
* **UzCrypto va AnyDesk:** Bitta tugma orqali dastur papkasini ochish yoki dasturni tizim almashish buferiga (clipboard) nusxalash (`Ctrl+V` orqali xohlagan joyga joylash).

---

## ⌨️ Tezkor Tugmalar (Hotkeys)

| Tugma | Amal | Tavsif |
| :--- | :--- | :--- |
| `Ctrl + F` | Tezkor Qidiruv | Qidiruv satriga fokus qaratish |
| `Ctrl + C` | Nusxalash | Jadvaldagi belgilangan kataklar yoki matnni nusxalash |
| `Ctrl + N` | Yangi Qo'shish | Yangi tashkilot qo'shish dialogini ochish |
| `Enter` | Saqlash | Dialog oynalarida o'zgarishlarni tasdiqlash |
| `Double Click` | Tahrirlash | Jadval qatoriga 2 marta bosib to'g'ridan-to'g'ri tahrirlash |
| `Esc` | Yopish | Faol modal dialog oynasini yopish |

---

## 🧱 Texnologiyalar Steki

| Qatlam | Texnologiya | Tavsif |
| :--- | :--- | :--- |
| **Foydalanuvchi Interfeysi** | **PyQt5 (Python Qt)** | Modern Fluent Design, Dark/Light mavzular, HiDPI masshtablash |
| **Ma'lumotlar Bazasi** | **SQLite 3 (WAL Mode)** | Yuqori tezlikdagi tranzaksiyalar, migratsiya va audit logi |
| **Faylli Sinxronizatsiya** | **Atomic JSON Engine** | Inson o'qiy oladigan ma'lumotlar bazasi zaxirasi |
| **Qidiruv Tizimi** | **Bilingual Phonetic Engine** | Lotin-Kirill transliteratsiyasi va mustaqil token qidiruvi |
| **Hisobotlar** | **openpyxl / pandas** | Excel (`.xlsx`, `.xls`) va CSV formatlarida import/export |
| **Aloqa Integratsiyasi** | **Requests / Telegram Bot API** | Xabarnomalar va bot orqali tezkor ma'lumot uzatish |

---

## 📁 Katalog Tuzilishi

```text
pop-tuman-tizimi/
├── main.py                     # Asosiy kirish nuqtasi (PyQt5 GUI)
├── run_tests.py                # Avtomatlashtirilgan test tizimi (80 ta test)
├── build_exe.py                # Standalone Windows .exe yig'uvchi
├── mahalla_tizimi.db           # SQLite asosiy bazasi (WAL)
├── mahalla_bazasi.json         # Atomik JSON sinxronizatsiya bazasi
│
├── core/                       # Yadro parametrlari, validatsiyalar va logger
├── database/                   # Ma'lumotlar modeli va SQLite/JSON menejerlari
├── services/                   # Aqlli qidiruv, QR, Excel va Telegram servislar
├── ui_qt/                      # Fluent interfeys, ko'rinishlar va dialoglar
│   ├── components/             # SmartCompleter, jadvallar va diagrammalar
│   └── views/                  # Dashboard, Jadval, Shartnomalar, MFY pasporti
└── tests/                      # 80 ta to'liq qamrovli avtotestlar to'plami
```

---

## 🚀 Ishga Tushirish

### 1. Repozitoriyni klonlash
```bash
git clone https://github.com/Valijon21/pop-tuman-tizimi.git
cd pop-tuman-tizimi
```

### 2. Bog'liqliklarni o'rnatish
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Dasturni ishga tushirish
```powershell
python main.py
```

---

## 🧪 Sifat Nazorati va Testlar

Loyiha barqarorligi va ishonchliligi 75 ta avtomatlashtirilgan test bilan himoyalangan:

```powershell
python run_tests.py
```

```text
Ran 75 tests in ~67s
OK - BARCHA TESTLAR MUVAFFAQIYATLI O'TDI! (75 ta test)
```

---

## 👨‍💻 Muallif

* **Dastur muallifi:** Valijon
* **Versiya:** 4.0 Pro Enterprise Edition
* **Qo'llab-quvvatlanadi:** Windows 10 / Windows 11 (64-bit)
* **Hudud:** Namangan viloyati, Pop tumani
