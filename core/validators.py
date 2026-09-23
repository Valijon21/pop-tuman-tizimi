"""
Pop Tuman Tashkilotlari va INN Tizimi
Ma'lumotlarni tekshirish va tozalash (Validation & Sanitization Layer)
"""
import re
from typing import Tuple

def sanitize_text(text: str, max_length: int = 500) -> str:
    """Matndagi ortiqcha bo'shliqlar va boshqaruv belgilarini tozalash."""
    if not text:
        return ""
    # Boshqaruv belgilarini olib tashlash (tab va newline-dan tashqari)
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(text))
    # Ortiqcha probellarni qisqartirish
    cleaned = " ".join(cleaned.strip().split())
    return cleaned[:max_length]

def clean_inn(inn: str) -> str:
    """INN (STIR) dan faqat raqamlarni ajratib olish."""
    if not inn:
        return ""
    return re.sub(r"\D", "", str(inn))

def validate_inn(inn: str, allow_empty: bool = True) -> Tuple[bool, str]:
    """
    O'zbekiston STIR (INN) raqamini tekshirish.
    STIR 9 ta raqamdan iborat bo'lishi shart.
    
    Qaytaradi: (to'g'riligi: bool, tozalangan_inn_yoki_xabar: str)
    """
    cleaned = clean_inn(inn)
    if not cleaned:
        if allow_empty:
            return True, ""
        return False, "INN (STIR) raqami kiritilmadi."
    
    if len(cleaned) != 9:
        return False, f"INN (STIR) 9 ta raqamdan iborat bo'lishi kerak. Kiritildi: {len(cleaned)} ta."
    
    return True, cleaned

def clean_phone(phone: str) -> str:
    """Telefon raqamidan faqat raqamlar va '+' belgisini ajratib olish."""
    if not phone:
        return ""
    raw_digits = re.sub(r"\D", "", str(phone))
    
    # Agar 998 bilan boshlansa
    if raw_digits.startswith("998") and len(raw_digits) == 12:
        return "+" + raw_digits
    # Agar 9 xonali bo'lsa (901234567)
    elif len(raw_digits) == 9:
        return "+998" + raw_digits
    elif raw_digits.startswith("8") and len(raw_digits) == 10: # Eski format 835...
        return "+998" + raw_digits[1:]
    
    return phone.strip()

def format_phone(phone: str) -> str:
    """Telefon raqamini +998 (XX) XXX-XX-XX formatiga keltirish."""
    cleaned = clean_phone(phone)
    digits = re.sub(r"\D", "", cleaned)
    
    if len(digits) == 12 and digits.startswith("998"):
        code = digits[3:5]
        p1 = digits[5:8]
        p2 = digits[8:10]
        p3 = digits[10:12]
        return f"+998 ({code}) {p1}-{p2}-{p3}"
    elif len(digits) == 9:
        code = digits[0:2]
        p1 = digits[2:5]
        p2 = digits[5:7]
        p3 = digits[7:9]
        return f"+998 ({code}) {p1}-{p2}-{p3}"
    
    return phone.strip()

def validate_phone(phone: str, allow_empty: bool = True) -> Tuple[bool, str]:
    """
    Telefon raqamini tekshirish.
    
    Qaytaradi: (to'g'riligi: bool, formatlangan_raqam_yoki_xabar: str)
    """
    if not phone or not str(phone).strip():
        if allow_empty:
            return True, ""
        return False, "Telefon raqami kiritilmadi."
    
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 9 or (len(digits) == 12 and digits.startswith("998")):
        return True, format_phone(phone)
    
    return False, "Telefon raqami noto'g'ri. 9 ta raqam kiritilishi kerak (masalan: 90 123-45-67)."
