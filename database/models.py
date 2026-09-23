import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple
from core.validators import sanitize_text, clean_inn, validate_inn, validate_phone

@dataclass
class Organization:
    """Tashkilot ma'lumotlar modeli va validatsiyasi."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    s: str = ""       # Turi / Kategoriya (Sector)
    m: str = ""       # Tashkilot nomi (Mahalla/Organization)
    f: str = ""       # Rahbar F.I.SH (Full name)
    t: str = ""       # Telefon raqami (Phone)
    inn: str = ""     # INN (Tax ID)
    izoh: str = ""    # Qo'shimcha izoh (Comment)
    deleted_at: Optional[str] = None # Chiqindiga tashlangan vaqt

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        """Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish."""
        item_id = str(data.get("id") or data.get("uuid") or uuid.uuid4())
        return cls(
            id=item_id,
            s=sanitize_text(data.get("s", "")),
            m=sanitize_text(data.get("m", "")),
            f=sanitize_text(data.get("f", "")),
            t=sanitize_text(data.get("t", "")),
            inn=clean_inn(data.get("inn", "")),
            izoh=sanitize_text(data.get("izoh", "")),
            deleted_at=data.get("deleted_at")
        )

    def to_dict(self) -> Dict[str, Any]:
        """Obyektni lug'atga aylantirish."""
        d = {
            "id": self.id,
            "s": self.s,
            "m": self.m,
            "f": self.f,
            "t": self.t,
            "inn": self.inn,
            "izoh": self.izoh
        }
        if self.deleted_at:
            d["deleted_at"] = self.deleted_at
        return d

    def validate(self) -> Tuple[bool, List[str]]:
        """Tashkilot ma'lumotlarini biznes qoidalari bo'yicha tekshirish."""
        errors: List[str] = []
        if not self.m or not self.m.strip():
            errors.append("Tashkilot nomi bo'sh bo'lishi mumkin emas.")
        
        if self.inn:
            is_valid, msg = validate_inn(self.inn, allow_empty=True)
            if not is_valid:
                errors.append(msg)
                
        if self.t:
            is_valid, msg = validate_phone(self.t, allow_empty=True)
            if not is_valid:
                errors.append(msg)
                
        return len(errors) == 0, errors
