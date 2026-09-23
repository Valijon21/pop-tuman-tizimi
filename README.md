# 🏢 Pop Tuman Tashkilotlari va INN Tizimi (PRO)

**Pop Tuman Tashkilotlari va INN Tizimi** — bu tashkilotlarni ro'yxatga olish, qidirish, tahrirlash va boshqarish uchun maxsus ishlab chiqilgan yuqori barqarorlikka ega **Desktop dastur**. 
Ushbu dastur orqali siz tashkilot rahbarlari, telefon raqamlari va INN ma'lumotlarini osonlik bilan boshqarishingiz, shuningdek, ma'lumotlarni real vaqt rejimida **Google Sheets** (Bulut) bilan xavfsiz sinxronizatsiya qilishingiz mumkin.

![Dashboard Screenshot](popdata.png) *Dastur ko'rinishi*

---

## 🚀 Versiya 3.0 (Production-Grade & Clean Architecture)

* 🏗 **Clean Architecture Modulli Tizim:** ~1900 qatorlik monolit kod `core/`, `database/`, `services/`, `ui/` qatlamlariga ajratildi. Kod o'qilishi va texnik xizmat ko'rsatish osonlashdi.
* 🧪 **To'liq Avtomatlashtirilgan Testlar:** Standart `unittest` asosida 20 ta test (100% PASS, 0.1s).
* 🛡 **Atomik Ma'lumot Saqlash:** JSON fayllar vaqtinchalik xotira orqali atomik yoziladi — kompyuter o'chib qolsa ham baza buzilmaydi.
* 🆔 **Unikal UUIDv4 Identifikator:** Har bir tashkilotga xalqaro standartdagi UUID berildi. INN bir xil yoki bo'sh bo'lganda ham tahrirlash va o'chirish 100% aniqlikda ishlaydi.
* ⚡ **Thread-Safe Fon Sinxronizatsiyasi:** Google Sheets bilan ma'lumot almashinuvida interfeys qotib qolmaydi va xavfsiz `after()` orqali yangilanadi.
* 🔑 **SHA-256 Parol Xavfsizligi:** Ochiq matndagi parollar o'rniga xesh qiymatlar saqlanadi va dastur ichidan parolni o'zgartirish oynasi mavjud.
* 🛡 **STIR/INN va Telefon Validatsiyasi:** O'zbekiston STIR (9 xonali) va telefon raqamlari qat'iy tekshiriladi va avto-formatlanadi.
* 🔔 **Zamonaviy Toast Xabarnomalar:** Bezovta qiluvchi modal popup'lar o'rniga silliq suzuvchi xabarlar.
* 📱 **RAM-da Tezkor QR Generatsiya:** Diskka ortiqcha `t.png` yozmasdan to'g'ridan-to'g'ri operativ xotirada QR-kod yaratiladi.
* 📦 **Mustaqil Windows .EXE Yig'ish:** Dasturni Python o'rnatilmagan kompyuterlarga ham tarqatish uchun `build_exe.py` skripti mavjud.
* 🔄 **100% Orqaga Moslik:** Ham yangi `python main.py`, ham avvalgi `python mahalrai_POP.py` orqali ishga tushirish mumkin.

---

## 📁 Loyiha Tuzilmasi

```
pop-tuman-tizimi/
├── main.py                     # Asosiy kirish nuqtasi (Modern Entry point)
├── mahalrai_POP.py             # 100% orqaga moslik uchun adapter
├── requirements.txt            # Loyiha kutubxonalari
├── run_tests.py                # Avtomatlashtirilgan test runner
├── build_exe.py                # Windows .exe dasturini yig'uvchi skript
│
├── core/                       # Yadro va konfiguratsiya
│   ├── config.py               # Doimiy parametrlar, yo'llar, ranglar
│   ├── logger.py               # Log tizimi (RotatingFileHandler)
│   ├── security.py             # SHA-256 xeshlash va parollar
│   └── validators.py           # INN, telefon va matn validatsiyasi
│
├── database/                   # Ma'lumotlar ombori
│   ├── models.py               # Organization ma'lumotlar modeli va validatsiyasi
│   └── data_manager.py         # Atomik saqlash, UUID, zaxira va audit log
│
├── services/                   # Tashqi servislar
│   ├── qr_service.py           # RAM-da QR-kod yaratish
│   ├── excel_service.py        # Excelga eksport qilish
│   ├── gsheet_service.py       # Google Sheets bilan aloqa
│   └── search_service.py       # Tezkor qidiruv va filtrlash xizmati
│
├── ui/                         # Foydalanuvchi interfeysi (CustomTkinter)
│   ├── style.py                # Mavzular va vizual stillar
│   ├── toast.py                # Suzuvchi zamonaviy xabarnomalar
│   ├── app.py                  # Asosiy oyna va boshqaruvchi (MainWindow)
│   └── views/                  # Ko'rinishlar (Views)
│       ├── dashboard_view.py   # Statistika sahifasi
│       ├── table_view.py       # Tashkilotlar jadvali va qidiruv
│       ├── trash_view.py       # Chiqindi qutisi
│       └── settings_view.py    # Sozlamalar va integratsiyalar
│
└── tests/                      # Avtomatlashtirilgan testlar to'plami
    ├── test_validators.py      # Validatsiya testlari
    ├── test_security.py        # Xavfsizlik testlari
    ├── test_models.py          # Model testlari
    ├── test_data_manager.py    # Ombor testlari
    └── test_services.py        # Servislar testlari
```

---

## 💻 O'rnatish va Ishga Tushirish

### 1-qadam. Loyihani yuklab olish
```bash
git clone https://github.com/Valijon21/pop-tuman-tizimi.git
cd pop-tuman-tizimi
```

### 2-qadam. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3-qadam. Dasturni ishga tushirish
Tavsiya etilgan zamonaviy buyruq:
```bash
python main.py
```
Yoki avvalgi buyruq orqali:
```bash
python mahalrai_POP.py
```

---

## 🧪 Avtomatlashtirilgan Testlarni Ishga Tushirish

Loyiha sifatini va barcha modullar to'g'ri ishlayotganini tekshirish uchun:
```bash
python run_tests.py
```
*Barcha 20 ta unit-test avtomatik ishga tushib, natijalarni ko'rsatadi.*

---

## 📦 Mustaqil Windows `.exe` Dasturini Yig'ish

Python o'rnatilmagan kompyuterlar uchun `.exe` yaratish:
```bash
python build_exe.py
```
*Yig'ilgan fayl `dist/PopTumanTizimi/PopTumanTizimi.exe` manzilida tayyor bo'ladi.*

---

## 🔑 Kalit Fayllar va Sozlamalar

Dastur to'g'ri ishlashi uchun quyidagi fayllar kerak:

1. **`service_account.json`**: Google Cloud Console-dan olingan kalit fayl (Google Sheets sinxronizatsiyasi uchun).
2. **`sync_config.json`**: Google Sheets jadval ID va sozlamalari (Dastur ichidan avtomatik sozlanadi).
3. **`settings.json`**: Dastur xavfsizlik sozlamalari va parollari.

---

## 🛡 Xavfsizlik va Rollar

* **Admin:** Barcha huquqlar (Tashkilot qo'shish, tahrirlash, o'chirish, trashdan tiklash, parollarni o'zgartirish, Google Sheets sozlash). Boshlang'ich parol: `123`
* **Operator:** Faqat ko'rish va ma'lumot kiritish huquqlari. Boshlang'ich parol: `1`

> 💡 **Tavsiya:** Dasturni birinchi marta ishga tushirgandan so'ng, "Sozlamalar" -> "Asboblar" -> "Parolni o'zgartirish" bo'limidan boshlang'ich parollarni shaxsiy xavfsiz parolingizga almashtiring.

---

## 📞 Muallif va Ruxsatnoma

* **Muallif:** Valijon
* **Versiya:** 3.0 (Production-Grade & Clean Architecture)
* **Tizim:** Windows 10/11 moslashuvchan Desktop ilova
