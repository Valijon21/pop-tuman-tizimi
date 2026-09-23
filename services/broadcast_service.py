"""
Pop Tuman Tashkilotlari va INN Tizimi
Ommaviy Xabarnoma va Bildirishnoma Xizmati (Broadcast Notification Service)
Favqulodda yig'ilishlar, sayyor qabullar va topshiriqlarni SMS / Telegram orqali tarqatish dvigateli.
"""
from typing import List, Dict, Any, Optional
from core.logger import logger

DEFAULT_TEMPLATES = {
    "emergency": (
        "🚨 DIQQAT: Bugun soat 17:00 da tuman hokimligi majlislar zalida "
        "barcha mas'ullar ishtirokida favqulodda yig'ilish o'tkaziladi. "
        "Barcha xodimlar shaxsan ishtirok etishi shart!"
    ),
    "reception": (
        "🏛 DIQQAT: Ertaga soat 10:00 da tuman hokimligi va soha rahbarlari ishtirokida "
        "navbatdagi sayyor qabul bo'lib o'tadi. Fuqarolar murojaatlari bo'yicha tayyorgarlik ko'rilsin."
    ),
    "urgent_task": (
        "⚡ TEZKOR TOPSHIRIQ: Belgilangan reja-grafik asosida topshiriqlar ijrosini ta'minlab, "
        "bugun soat 18:00 ga qadar tuman shtabiga to'liq hisobot taqdim etishingiz so'raladi."
    ),
    "custom": ""
}

AUDIENCE_GROUPS = [
    ("Barchasi (Barcha tashkilotlar)", "all"),
    ("Mahalla raislari", "raislari"),
    ("Hokim yordamchilari", "hokim_yordamchilari"),
    ("Yoshlar yetakchilari", "yoshlar"),
    ("Xotin-qizlar faollari", "xotin_qizlar"),
    ("Ijtimoiy xodimlar", "ijtimoiy"),
    ("Profilaktika inspektorlari", "inspektor"),
    ("Maktab direktorlari", "maktab"),
    ("MTT mudiralari (Bog'chalar)", "bogcha"),
]

def filter_audience_recipients(
    data: List[Dict[str, Any]],
    group_key: str = "all",
    mahalla_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Belgilangan toifa va mahalla bo'yicha xabarnoma oluvchilar ro'yxatini shakllantirish."""
    results = []
    m_filter = (mahalla_query or "").strip().lower()

    for item in data:
        sec = str(item.get("s", "")).strip().lower()
        org_name = str(item.get("m", "")).strip()
        tel = str(item.get("t", "")).strip()

        # Mahalla filtri
        if m_filter and m_filter not in org_name.lower():
            continue

        matched = False
        if group_key == "all":
            matched = True
        elif group_key == "raislari" and ("mahalla" in sec or "mfy" in sec or "raisi" in sec):
            matched = True
        elif group_key == "hokim_yordamchilari" and "hokim yordamchi" in sec:
            matched = True
        elif group_key == "yoshlar" and "yoshlar" in sec:
            matched = True
        elif group_key == "xotin_qizlar" and "xotin" in sec:
            matched = True
        elif group_key == "ijtimoiy" and "ijtimoiy" in sec:
            matched = True
        elif group_key == "inspektor" and ("profilaktika" in sec or "inspektor" in sec or "ichki" in sec):
            matched = True
        elif group_key == "maktab" and "maktab" in sec:
            matched = True
        elif group_key == "bogcha" and ("bog'cha" in sec or "mtt" in sec):
            matched = True

        if matched:
            results.append(item)

    return results

def extract_clean_phone_list(recipients: List[Dict[str, Any]]) -> List[str]:
    """Qabul qiluvchilar ro'yxatidan faqat toza xalqaro formatdagi telefon raqamlarini ajratish."""
    from core.validators import clean_phone
    phones = []
    for r in recipients:
        raw_t = r.get("t", "")
        cleaned = clean_phone(raw_t)
        if cleaned and len(cleaned) == 13 and cleaned.startswith("+998"):
            if cleaned not in phones:
                phones.append(cleaned)
    return phones

def calculate_sms_segments(text: str) -> Dict[str, Any]:
    """SMS xabar belgilar soni va segmentlar (1 ta yoki 2 ta SMS) hisoblagichi."""
    length = len(text)
    is_ascii = all(ord(c) < 128 for c in text)
    
    if is_ascii:
        per_part = 160 if length <= 160 else 153
    else:
        per_part = 70 if length <= 70 else 67

    parts = max(1, (length + per_part - 1) // per_part) if length > 0 else 0
    return {
        "length": length,
        "is_ascii": is_ascii,
        "parts": parts,
        "encoding": "GSM-7 (Lotin)" if is_ascii else "Unicode (Kirill)"
    }

# Yuqori darajadagi API va shablonlar
SMS_TEMPLATES = {
    "Favqulodda yig'ilish": DEFAULT_TEMPLATES["emergency"],
    "Sayyor qabul": DEFAULT_TEMPLATES["reception"],
    "Tezkor topshiriq": DEFAULT_TEMPLATES["urgent_task"],
    "Erkin matn": ""
}

class BroadcastService:
    """Ommaviy xabarnomalar xizmatining yuqori darajadagi klassi."""

    @staticmethod
    def filter_recipients(data: List[Dict[str, Any]], group_key: str = "all", mahalla_query: Optional[str] = None) -> List[Dict[str, Any]]:
        return filter_audience_recipients(data, group_key=group_key, mahalla_query=mahalla_query)

    @staticmethod
    def extract_phones(recipients: List[Dict[str, Any]]) -> List[str]:
        return extract_clean_phone_list(recipients)

    @staticmethod
    def calculate_segments(text: str) -> Dict[str, Any]:
        return calculate_sms_segments(text)

    @staticmethod
    def send_broadcast(recipients: List[Dict[str, Any]], template: str, channels: Optional[Dict[str, bool]] = None, data_manager: Any = None) -> Dict[str, Any]:
        channels = channels or {"telegram": True, "sms": True}
        tg_sent = 0
        tg_total = 0
        if channels.get("telegram"):
            try:
                from services.telegram_bot import get_telegram_bot_service
                bot = get_telegram_bot_service(data_manager=data_manager)
                if bot.is_configured():
                    res = bot.broadcast_message(f"📢 <b>Ommaviy Xabarnoma:</b>\n\n{template}")
                    tg_sent = res.get("sent", 0)
                    tg_total = res.get("total", 0)
                    logger.info(f"[BROADCAST] Telegram orqali {tg_sent}/{tg_total} ta obunachiga yuborildi.")
                else:
                    logger.warning("[BROADCAST] Telegram bot tokeni sozlanmagan.")
            except Exception as e:
                logger.error(f"[BROADCAST] Telegram yuborishda xatolik: {e}")

        clean_phones = extract_clean_phone_list(recipients)
        return {
            "status": "ok",
            "recipients_count": len(recipients),
            "clean_phones_count": len(clean_phones),
            "telegram_sent": tg_sent,
            "telegram_subscribers": tg_total
        }


