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
    jshr: str = ""    # JSHSHIR (14 xonali PINFL)
    seriya: str = ""  # Pasport seriya va raqami (masalan, AB1234567)
    lavozim: str = "" # Xodim lavozimi (masalan, Rais, Yoshlar yetakchisi)
    bux_tel: str = "" # Buxgalter telefoni
    aparat_soni: Optional[int] = None # Apparat xodimlari soni
    ulangan_soni: Optional[int] = None # Ulangan xodimlar / litsenziyalar
    updated_at: str = "" # So'nggi yangilanish vaqti
    deleted_at: Optional[str] = None # Chiqindiga tashlangan vaqt

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        """Lug'at (dict) dan tozalangan va xavfsiz obyekt yaratish."""
        item_id = str(data.get("id") or data.get("uuid") or uuid.uuid4())
        aparat = data.get("aparat_soni")
        ulangan = data.get("ulangan_soni")
        return cls(
            id=item_id,
            s=sanitize_text(data.get("s", "")),
            m=sanitize_text(data.get("m", "")),
            f=sanitize_text(data.get("f", "")),
            t=sanitize_text(data.get("t", "")),
            inn=clean_inn(data.get("inn", "")),
            izoh=sanitize_text(data.get("izoh", "")),
            jshr=sanitize_text(data.get("jshr", "")),
            seriya=sanitize_text(data.get("seriya", "")),
            lavozim=sanitize_text(data.get("lavozim", "")),
            bux_tel=sanitize_text(data.get("bux_tel", "")),
            aparat_soni=int(aparat) if aparat not in (None, "") else None,
            ulangan_soni=int(ulangan) if ulangan not in (None, "") else None,
            updated_at=str(data.get("updated_at", "")),
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
        if self.jshr:
            d["jshr"] = self.jshr
        if self.seriya:
            d["seriya"] = self.seriya
        if self.lavozim:
            d["lavozim"] = self.lavozim
        if self.bux_tel:
            d["bux_tel"] = self.bux_tel
        if self.aparat_soni is not None:
            d["aparat_soni"] = self.aparat_soni
        if self.ulangan_soni is not None:
            d["ulangan_soni"] = self.ulangan_soni
        if self.updated_at:
            d["updated_at"] = self.updated_at
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
