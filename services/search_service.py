"""
Pop Tuman Tashkilotlari va INN Tizimi
Tezkor Qidiruv va Filtrlash Xizmati (Search & Filter Service)
Lotin va Kirill alifbosini aqlli transliteratsiya qilish, ko'p so'zli token qidiruvi va auto-complete takliflari.
"""
import re
from typing import List, Dict, Any, Optional

CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
    'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh',
    'ъ': "'", 'ы': 'i', 'ь': "", 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'ғ': "g'", 'қ': 'q', 'ҳ': 'h', 'ў': "o'"
}

def transliterate_to_latin(text: str) -> str:
    """Kirill yozuvidagi o'zbek matnini lotin yozuviga o'girish."""
    if not text:
        return ""
    res = []
    for ch in str(text).lower():
        res.append(CYRILLIC_TO_LATIN.get(ch, ch))
    return "".join(res)

def normalize_text(text: str) -> str:
    """Qidiruv uchun matnni to'liq normallashtirish (tutuq belgilari, kirill-lotin, oraliqlar)."""
    if not text:
        return ""
    text = str(text).lower()
    # Tutuq belgilarini yagona ' ko'rinishga keltirish: ', `, ‘, ’, ʻ, ʼ
    text = re.sub(r"[`'‘ʼ’ʻ'´]", "'", text)
    # Kirill bo'lsa lotinga o'girish
    text = transliterate_to_latin(text)
    # Bo'shliqlarni ixchamlashtirish
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def smart_match_tokens(query_norm: str, target_norm: str) -> bool:
    """Aqlli tokenli moslash: barcha so'zlar nishon ichida uchrashini tekshiradi."""
    if not query_norm:
        return True
    if query_norm in target_norm:
        return True
    
    # Chiziqchalarni bo'shliqqa aylantirib ham tekshirish (masalan: 1-maktab <-> 1 maktab)
    t_clean = re.sub(r"[-_.,/]", " ", target_norm)
    if query_norm in t_clean:
        return True

    tokens = [t for t in query_norm.split() if t]
    if not tokens:
        return True
    
    return all((tok in target_norm or tok in t_clean) for tok in tokens)

class SearchService:
    """Tashkilotlar bazasida tezkor, aqlli qidiruv va filtrlash xizmati."""

    @staticmethod
    def match_category(item_cat: str, filter_cat: str) -> bool:
        """Toifalarni moslashtirish (shu jumladan qisqartmalar va sinonimlar)."""
        if not filter_cat or filter_cat == "Barchasi":
            return True
        item_cat = str(item_cat or "").strip()
        if item_cat == filter_cat:
            return True
        if filter_cat == "Mahalla (MFY)" and item_cat in ["Mahalla", "MFY"]:
            return True
        if filter_cat == "Maktab" and item_cat in ["Maktablar", "Maktab"]:
            return True
        if filter_cat == "Bog'cha (MTT)" and item_cat in ["MTT", "Bog'cha"]:
            return True
        if filter_cat == "Boshqa":
            known = [
                "Mahalla (MFY)", "Mahalla", "MFY",
                "Maktab", "Maktablar",
                "Bog'cha (MTT)", "MTT", "Bog'cha",
                "Hokim yordamchisi", "Yoshlar yetakchisi",
                "Ijtimoiy xodim", "Xotin qizlar"
            ]
            return (item_cat not in known) or (item_cat == "Boshqa")
        return False

    @staticmethod
    def search(
        data: List[Dict[str, Any]],
        query: str = "",
        category: str = "Barchasi",
        field_type: str = "Barchasi",
        sort_by: Optional[str] = None,
        reverse: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Ko'p maydonli aqlli qidiruv va filtrlash.
        Lotin/Kirill transliteratsiyasi, so'zlar tartibiga bog'liq bo'lmagan token qidiruvi.
        Maydonlar: Nomi, F.I.SH, INN, Izoh, Barchasi.
        """
        query_norm = normalize_text(query)
        digits_query = re.sub(r"\D", "", str(query or "")) if query else ""
        results: List[Dict[str, Any]] = []

        for item in data:
            # 1. Toifa bo'yicha filtr
            if not SearchService.match_category(item.get("s", ""), category):
                continue

            # Qidiruv so'zi bo'lmasa, toifadagi barcha yozuvlar o'tadi
            if not query_norm:
                results.append(item)
                continue

            # 2. Maydonlar bo'yicha aqlli qidiruv
            m_norm = normalize_text(item.get("m", ""))
            f_norm = normalize_text(item.get("f", ""))
            izoh_norm = normalize_text(item.get("izoh", ""))
            inn_val = str(item.get("inn", "")).strip()
            phone_digits = re.sub(r"\D", "", str(item.get("t", "")))
            bux_digits = re.sub(r"\D", "", str(item.get("bux_tel", "")))

            matched = False
            if field_type == "Nomi":
                matched = smart_match_tokens(query_norm, m_norm)
            elif field_type == "F.I.SH":
                matched = smart_match_tokens(query_norm, f_norm)
            elif field_type == "INN":
                matched = (digits_query in inn_val) if digits_query else (query_norm in inn_val)
            elif field_type == "Izoh":
                matched = smart_match_tokens(query_norm, izoh_norm)
            else:  # Barchasi
                combined_text = f"{m_norm} {inn_val} {f_norm} {izoh_norm} {phone_digits} {bux_digits}"
                if smart_match_tokens(query_norm, combined_text):
                    matched = True
                elif digits_query and len(digits_query) >= 3 and query_norm.replace(" ", "").isdigit():
                    if (digits_query in inn_val) or (digits_query in phone_digits) or (digits_query in bux_digits):
                        matched = True

            if matched:
                results.append(item)

        # 3. Saralash
        if sort_by:
            results.sort(key=lambda x: str(x.get(sort_by, "")).lower(), reverse=reverse)

        return results

    @staticmethod
    def get_search_dictionary(data: List[Dict[str, Any]]) -> List[str]:
        """Auto-complete takliflari uchun barcha unikal nomlar, INN va xodimlar ro'yxati."""
        suggestions: List[str] = []
        seen = set()

        # 1. Tashkilot nomlari
        for it in data:
            m = str(it.get("m", "")).strip()
            if m and m not in seen:
                seen.add(m)
                suggestions.append(m)

        # 2. INN — Tashkilot Nomi
        for it in data:
            inn = str(it.get("inn", "")).strip()
            m = str(it.get("m", "")).strip()
            if inn and inn not in seen:
                seen.add(inn)
                suggestions.append(f"{inn} — {m}" if m else inn)

        # 3. F.I.SH (Mas'ul xodimlar)
        for it in data:
            f = str(it.get("f", "")).strip()
            m = str(it.get("m", "")).strip()
            if f and f not in seen:
                seen.add(f)
                suggestions.append(f"{f} ({m})" if m else f)

        return suggestions

    @staticmethod
    def get_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tashkilotlar bo'yicha umumiy statistika hisoblash."""
        total = len(data)
        categories_count: Dict[str, int] = {}
        with_inn = 0
        with_phone = 0

        for item in data:
            cat = str(item.get("s", "Boshqa")).strip() or "Boshqa"
            categories_count[cat] = categories_count.get(cat, 0) + 1

            if item.get("inn") and str(item.get("inn")).strip():
                with_inn += 1
            if item.get("t") and str(item.get("t")).strip():
                with_phone += 1

        return {
            "total": total,
            "categories": categories_count,
            "with_inn": with_inn,
            "with_phone": with_phone
        }

