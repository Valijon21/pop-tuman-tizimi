import hashlib
import time
from typing import Optional, Dict

def hash_password(password: str) -> str:
    """Parolni SHA-256 xeshga aylantirish."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(entered_password: str, stored_hash: str, fallback_plain: Optional[str] = None) -> bool:
    """Parolni xesh yoki o'tish davri uchun ochiq matn bilan tekshirish."""
    if not entered_password:
        return False
    if hash_password(entered_password) == stored_hash:
        return True
    if fallback_plain and entered_password == fallback_plain:
        return True
    return False

def authenticate_user(entered_password: str, passwords_dict: Dict[str, str]) -> Optional[str]:
    """Kiritilgan parol bo'yicha foydalanuvchi rolini (admin/operator) aniqlash."""
    if not entered_password:
        return None
        
    admin_hash = passwords_dict.get("admin", hash_password("123"))
    operator_hash = passwords_dict.get("operator", hash_password("1"))
    
    if verify_password(entered_password, admin_hash, fallback_plain="123"):
        return "admin"
    if verify_password(entered_password, operator_hash, fallback_plain="1"):
        return "operator"
        
    return None
