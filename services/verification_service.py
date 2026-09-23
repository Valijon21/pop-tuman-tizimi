"""
Pop Tuman Tashkilotlari va INN Tizimi
Verifikatsiya Xizmati (Verification Service)
Xodimlar va tashkilotlar uchun rasmiy verifikatsiya shablon matnini shakllantirish.
"""
import re
from typing import Dict, Any, Tuple, Optional

def extract_identifiers_from_text(text: str) -> Tuple[str, str]:
    """
    Matn yoki izoh ichidan JSHSHIR (14 xonali) va pasport seriyasini (masalan, AB1234567) ajratib olish.
    """
    if not text:
        return "", ""
    
    text_str = str(text).strip()
    
    # 14 xonali JSHSHIR qidirish
    jshr_match = re.search(r"\b([1-6]\d{13})\b", text_str)
    jshr = jshr_match.group(1) if jshr_match else ""
    
    # Pasport seriya va raqami (2 ta harf + 7 ta raqam, probelli yoki probelsiz)
    seriya_match = re.search(r"\b([A-Za-z]{2}\s*\d{7})\b", text_str)
    seriya = seriya_match.group(1).replace(" ", "").upper() if seriya_match else ""
    
    return jshr, seriya

def format_role(sector: str, organization_name: str) -> str:
    """
    Tashkilot turi va nomiga qarab xodimning lavozimini to'g'ri shakllantirish.
    """
    sector = str(sector or "").strip()
    organization_name = str(organization_name or "").strip()
    
    sec_lower = sector.lower()
    
    if "hokim yordamchi" in sec_lower:
        return f"{organization_name} hokim yordamchisi"
    elif "yoshlar yetakchi" in sec_lower:
        return f"{organization_name} yoshlar yetakchisi"
    elif "ijtimoiy xodim" in sec_lower:
        return f"{organization_name} ijtimoiy xodimi"
    elif "xotin qizlar" in sec_lower:
        return f"{organization_name} xotin-qizlar faoli"
    elif sec_lower in ["mahalla", "mahalla (mfy)", "mfy"]:
        return f"{organization_name} raisi"
    elif "maktab" in sec_lower:
        return f"{organization_name} direktori"
    elif "bog'cha" in sec_lower or "mtt" in sec_lower:
        return f"{organization_name} mudirasi"
    elif sector:
        return f"{organization_name} {sector}"
    return organization_name

def build_verification_text(
    item: Dict[str, Any],
    jshr: Optional[str] = None,
    seriya: Optional[str] = None,
    role: Optional[str] = None
) -> str:
    """
    Foydalanuvchi talabiga to'liq mos keluvchi verifikatsiya shablon matnini yaratish:
    
    Tashkilot nomi: Chorkesar MFY
    -INN:   203599806
    F.I.O:  Yondashev Xojiakbar Rustamali o‘g‘li
    JSHR : 30807995910027
    Seriya : AB4561091
    Lavozimi: Chorkesar MFY hokim yordamchi
    verfikatsiya bervoring.
    """
    org_name = str(item.get("m", "")).strip()
    inn_val = str(item.get("inn", "")).strip()
    fio_val = str(item.get("f", "")).strip()
    izoh_val = str(item.get("izoh", "")).strip()
    sector_val = str(item.get("s", "")).strip()
    
    # Agar JSHSHIR yoki seriya berilmagan bo'lsa, itemdan yoki izohdan qidiramiz
    auto_jshr, auto_seriya = extract_identifiers_from_text(izoh_val)
    
    final_jshr = jshr if jshr is not None and jshr != "" else (item.get("jshr") or auto_jshr or "")
    final_seriya = seriya if seriya is not None and seriya != "" else (item.get("seriya") or auto_seriya or "")
    
    if role is not None and role != "":
        final_role = role
    else:
        final_role = format_role(sector_val, org_name)
        
    return (
        f"Tashkilot nomi: {org_name}\n"
        f"-INN:   {inn_val}\n"
        f"F.I.O:  {fio_val}\n"
        f"JSHR : {final_jshr}\n"
        f"Seriya : {final_seriya}\n"
        f"Lavozimi: {final_role}\n"
        f"verfikatsiya bervoring."
    )
