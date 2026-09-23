"""
Pop Tuman Tashkilotlari va INN Tizimi
Kabinet Xizmati (Cabinet Access Service)
Xodimlar va tashkilotlar uchun shaxsiy kabinetga dostup so'rovi shablon matnini shakllantirish.
"""
from typing import Dict, Any, Optional

def build_cabinet_access_text(
    item: Dict[str, Any],
    action_text: Optional[str] = None
) -> str:
    """
    Foydalanuvchi talabiga to'liq mos keluvchi rasmiy 'Kabinetga dostup' shablon matnini shakllantirish:

    Tashkilot nomi: 22-Sonli Umumiy O'rta Ta'lim Maktabi
    INN:   206907205
    F.I.O:  Dehqanova Azimaxon Ortiqovna
    cabinetga dostup
    """
    org_name = str(item.get("m", "")).strip()
    inn_val = str(item.get("inn", "")).strip()
    fio_val = str(item.get("f", "")).strip()
    action = (action_text.strip() if action_text and action_text.strip() else "cabinetga dostup")

    return (
        f"Tashkilot nomi: {org_name}\n"
        f"INN:   {inn_val}\n"
        f"F.I.O:  {fio_val}\n"
        f"{action}"
    )

def get_cabinet_portal_url(sector: str) -> str:
    """Tashkilot toifasiga qarab tegishli davlat portali havolasini qaytarish."""
    sec = str(sector or "").lower()
    if "maktab" in sec:
        return "https://e-maktab.uz"
    elif "bog'cha" in sec or "mtt" in sec:
        return "https://my.gov.uz"
    elif "mahalla" in sec or "hokim" in sec:
        return "https://online-mahalla.uz"
    return "https://my.soliq.uz"
