# 🏢 Pop Tuman Tashkilotlari va INN Tizimi

**Pop Tuman Tashkilotlari va INN Tizimi** — bu tashkilotlarni ro'yxatga olish, qidirish va boshqarish uchun maxsus ishlab chiqilgan **Desktop dastur**. 
Ushbu dastur orqali siz tashkilot rahbarlari, telefon raqamlari va INN ma'lumotlarini osonlik bilan boshqarishingiz, shuningdek, ma'lumotlarni real vaqt rejimida **Google Sheets** (Bulut) bilan sinxronizatsiya qilishingiz mumkin.

![Dashboard Screenshot](popdat.png) *Dastur ko'rinishi*

---

## 🚀 Yangiliklar (v2.1)

*   **QR Kod Tizimi:** Telefon raqamli QR kodlar endi "835" kabi ortiqcha kodlarsiz, toza va aniq ishlaydi. Skaner qilganda to'g'ridan-to'g'ri qo'ng'iroq qilish imkoniyati.
*   **Avto-Format:** Telefon raqam kiritishda avtomatik `+998 (XX) XXX-XX-XX` andozasi qo'shildi.
*   **O'zbekcha Kod:** Dastur kodi to'liq o'zbek tilida izohlandi (O'zbek dasturchilari uchun qulaylik).
*   **Ma'lumotlar Xavfsizligi:** Yangi qo'shilgan ma'lumotlar avtomatik tarzda bazaning oxiriga qo'shiladi va eskilariga zarar yetkazmaydi.

---

## 🛠 Asosiy Imkoniyatlar

### 📋 Ma'lumotlarni Boshqarish
*   **Qo'shish / Tahrirlash / O'chirish:** Tashkilotlarni oson boshqarish.
*   **Qidiruv:** INN, Tashkilot nomi yoki rahbari bo'yicha tezkor qidiruv.
*   **Filter:** Mahallalar, Maktablar va Bog'chalarni alohida saralash.

### ☁️ Google Sheet Integratsiyasi (Real-vaqt)
*   **Avtomatik Sinxronizatsiya:** Dasturdagi har bir o'zgarish (qo'shish, o'chirish) avtomatik ravishda Google Jadvalga tushadi.
*   **Ma'lumotlarni Olish (Restore):** Kompyuter o'zgarganda ma'lumotlarni bulutdan qayta yuklab olish imkoniyati.
*   **100% Xavfsiz:** Google Service Account orqali himoyalangan ulanish.

### 📊 Statistika va Monitoring
*   **Dashboard:** Jami tashkilotlar, maktablar va bog'chalar sonini grafik ko'rinishida kuzatish.
*   **Log Tizimi:** Dasturdagi barcha xatoliklar va harakatlar `app.log` faylida saqlab boriladi.

### 📱 Qo'shimcha Qulayliklar
*   **QR Kod:** Telefon raqamlar uchun avtomatik QR kod yaratish (skanerlash uchun).
*   **Excel Export:** Ma'lumotlarni Excel formatida yuklab olish.
*   **User Roles:** Admin (123) va Operator (1) rejimlarida ishlash.
*   **Dark Mode:** Tungi va kunduzgi rejimlar.

---

## 💻 O'rnatish va Ishga Tushirish

Ushbu dasturni ishga tushirish uchun kompyuteringizda **Python** o'rnatilgan bo'lishi kerak.

### 1-qadam. Loyihani yuklab olish
```bash
git clone https://github.com/Valijon21/pop-tuman-tizimi.git
cd pop-tuman-tizimi
```

### 2-qadam. Kerakli kutubxonalarni o'rnatish
Windows terminalida quyidagi buyruqni bering:
```bash
pip install -r requirements.txt
```
*(Agar `requirements.txt` bo'lmasa, quyidagilarni o'rnating: `customtkinter`, `gspread`, `oauth2client`, `openpyxl`, `qrcode`, `pillow`)*

### 3-qadam. Dasturni ochish
```bash
python mahalrai_POP.py
```

---

## 🔑 Kalit Fayllar va Sozlamalar

Dastur to'g'ri ishlashi uchun quyidagi fayllar kerak:

1.  **`service_account.json`**: Google Cloud Console-dan olingan maxsus kalit fayl (Google Sheet bilan ishlash uchun).
2.  **`popdat.png`**: Dastur logotipi.
3.  **`sync_config.json`**: Googla Sheet linki saqlanadigan fayl (Avtomatik yaratiladi).

---

## 🛡 Xavfsizlik va Rollar

*   **Admin Paroli:** `123` (Barcha huquqlar: O'chirish, Tiklash, Sozlamalar).
*   **Operator Paroli:** `1` (Faqat ko'rish va qo'shish).

> **Eslatma:** Ma'lumot o'chirilganda u butunlay o'chib ketmaydi, balki "Chiqindi qutisi" (Trash) ga tushadi. Uni faqat Admin qaytara oladi.

---

## 📞 Aloqa va Yordam
Dastur bo'yicha savollar yoki takliflar bo'lsa, dasturchi bilan bog'laning.

**Muallif:** Valijon
**Versiya:** 2.1 (QR Fix & Uzbek Comments)
**Oxirgi yangilanish:** 2026-yil Fevral
