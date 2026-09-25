"""
core.security: Xavfsizlik, parollarni xeshlash va autentifikatsiya moduli.
PBKDF2-HMAC-SHA256, maxfiy Salt va Brute-force (Rate Limiting) himoyasi bilan boyitilgan.
"""
import hashlib
import hmac
import secrets
import time
from typing import Optional, Dict, Tuple, List

# Brute-force himoyasi sozlamalari
MAX_FAILED_ATTEMPTS: int = 5
LOCKOUT_DURATION_SEC: int = 60

# Xotiradagi urinishlar registri: {identifier: [timestamp1, timestamp2, ...]}
_FAILED_ATTEMPTS: Dict[str, List[float]] = {}


def generate_salt(length: int = 16) -> str:
    """Xavfsiz tasodifiy salt (tuz) heks-satrini yaratish."""
    return secrets.token_hex(length)


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Parolni xeshga aylantirish.
    Agar salt berilsa - PBKDF2-HMAC-SHA256 (100,000 iteratsiya) ishlatiladi.
    Agar salt berilmasa - standart SHA-256 qaytariladi (orqaga moslik uchun).
    """
    if not password:
        return ""
    if salt:
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        )
        return f"pbkdf2:sha256:100000:{salt}:{dk.hex()}"
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password_salted(password: str, salt: Optional[str] = None) -> str:
    """PBKDF2-HMAC-SHA256 yordamida parolni avtomatik salt bilan xeshlash."""
    s = salt or generate_salt(16)
    return hash_password(password, salt=s)


def verify_password(entered_password: str, stored_hash: str, fallback_plain: Optional[str] = None) -> bool:
    """
    Kiritilgan parolni saqlangan xesh bilan xavfsiz solishtirish (Timing Attack himoyasi bilan).
    PBKDF2 formatini ham, an'anaviy SHA-256 formatini ham avtomatik aniqlaydi.
    """
    if not entered_password or not stored_hash:
        return False

    # 1. PBKDF2 formati tekshiruvi (pbkdf2:sha256:iterations:salt:hash)
    if stored_hash.startswith("pbkdf2:sha256:"):
        parts = stored_hash.split(":")
        if len(parts) == 5:
            try:
                iterations = int(parts[2])
                salt = parts[3]
                expected_dk = parts[4]
                computed_dk = hashlib.pbkdf2_hmac(
                    "sha256",
                    entered_password.encode("utf-8"),
                    salt.encode("utf-8"),
                    iterations
                ).hex()
                return hmac.compare_digest(computed_dk, expected_dk)
            except Exception:
                return False

    # 2. Standart SHA-256 xesh tekshiruvi
    computed_sha = hashlib.sha256(entered_password.encode("utf-8")).hexdigest()
    if hmac.compare_digest(computed_sha, stored_hash):
        return True

    # 3. O'tish davri uchun ochiq matn (agar ko'rsatilgan bo'lsa)
    if fallback_plain and hmac.compare_digest(entered_password, fallback_plain):
        return True

    return False


def is_rate_limited(identifier: str = "global") -> Tuple[bool, int]:
    """
    Foydalanuvchi yoki IP bloklanganligini tekshirish.
    Qaytaradi: (bloklanganmi, qolgan_kutish_soniyasi)
    """
    now = time.time()
    attempts = _FAILED_ATTEMPTS.get(identifier, [])
    # Muddati o'tgan urinishlarni tozalash
    valid_attempts = [t for t in attempts if now - t < LOCKOUT_DURATION_SEC]
    _FAILED_ATTEMPTS[identifier] = valid_attempts

    if len(valid_attempts) >= MAX_FAILED_ATTEMPTS:
        oldest_valid = min(valid_attempts)
        remaining = int(LOCKOUT_DURATION_SEC - (now - oldest_valid))
        return True, max(1, remaining)
    return False, 0


def record_failed_attempt(identifier: str = "global") -> None:
    """Muvaffaqiyatsiz urinishni qayd etish."""
    now = time.time()
    if identifier not in _FAILED_ATTEMPTS:
        _FAILED_ATTEMPTS[identifier] = []
    _FAILED_ATTEMPTS[identifier].append(now)


def reset_failed_attempts(identifier: str = "global") -> None:
    """Muvaffaqiyatli kirishdan so'ng bloklash hisoblagichini tozalash."""
    _FAILED_ATTEMPTS.pop(identifier, None)


DEFAULT_PASSWORDS: Dict[str, str] = {
    "edit": "1234567",
    "settings": "773423321v",
    "admin": "773423321v",
    "operator": "1234567"
}


def authenticate_user(entered_password: str, passwords_dict: Dict[str, str], identifier: str = "global") -> Optional[str]:
    """
    Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash.
    Brute-force himoyasi mavjud: 5 ta xato urinishdan so'ng 60 soniyaga bloklanadi.
    """
    if not entered_password:
        return None

    # Brute-force tekshiruvi
    blocked, _ = is_rate_limited(identifier)
    if blocked:
        return None

    admin_hash = passwords_dict.get("admin") or passwords_dict.get("settings") or hash_password(DEFAULT_PASSWORDS["admin"])
    operator_hash = passwords_dict.get("operator") or passwords_dict.get("edit") or hash_password(DEFAULT_PASSWORDS["operator"])

    if verify_password(entered_password, admin_hash, fallback_plain=DEFAULT_PASSWORDS["admin"]) or (
        # Moslik uchun eski 123
        verify_password(entered_password, admin_hash, fallback_plain="123")
    ):
        reset_failed_attempts(identifier)
        return "admin"

    if verify_password(entered_password, operator_hash, fallback_plain=DEFAULT_PASSWORDS["operator"]) or (
        # Moslik uchun eski 1
        verify_password(entered_password, operator_hash, fallback_plain="1")
    ):
        reset_failed_attempts(identifier)
        return "operator"

    # Noto'g'ri parol bo'lsa urinishni qayd qilish
    record_failed_attempt(identifier)
    return None


def verify_action_password(
    action: str,
    entered_password: str,
    passwords_dict: Optional[Dict[str, str]] = None,
    identifier: str = "global"
) -> Tuple[bool, str]:
    """
    Muayyan amal ('edit' yoki 'settings') uchun parolni tekshirish.
    action='edit' uchun standart: '1234567'
    action='settings' uchun standart: '773423321v'
    Qaytaradi: (muvaffaqiyatlimi, xabar)
    """
    if not entered_password:
        return False, "Parol kiritilmadi!"

    # Brute-force tekshiruvi
    blocked, wait_sec = is_rate_limited(identifier)
    if blocked:
        return False, f"Ko'p xato urinish! Iltimos, {wait_sec} soniya kuting."

    p_dict = passwords_dict or {}
    expected_hash = p_dict.get(action)
    fallback = DEFAULT_PASSWORDS.get(action, "")

    if not expected_hash:
        if action == "edit":
            expected_hash = p_dict.get("operator")
        elif action == "settings":
            expected_hash = p_dict.get("admin")

    is_valid = False
    if expected_hash:
        is_valid = verify_password(entered_password, expected_hash, fallback_plain=fallback)
    else:
        is_valid = (entered_password == fallback)

    if is_valid:
        reset_failed_attempts(identifier)
        return True, "Parol to'g'ri tasdiqlandi."

    record_failed_attempt(identifier)
    blocked_now, remaining = is_rate_limited(identifier)
    if blocked_now:
        return False, f"Xavfsizlik: 5 ta xato urinish sababli {remaining} soniyaga bloklandingiz!"
    return False, "Noto'g'ri parol! Qayta urinib ko'ring."

