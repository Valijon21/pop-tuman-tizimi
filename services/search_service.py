"""
Pop Tuman Tashkilotlari va INN Tizimi
Tezkor Qidiruv va Filtrlash Xizmati (Search & Filter Service)
"""
import re
from typing import List, Dict, Any, Optional

def normalize_text(text: str) -> str:
    """Qidiruv uchun matnni normallashtirish (lotin, kirill va tutuq belgilari)."""
    if not text:
        return ""
    text = str(text).lower()
    # Tutuq belgilarini bir xil ko'rinishga keltirish: ', `, ‘, ’
    text = re.sub(r"[`'‘ʼ’]", "'", text)
    return text.strip()

class SearchService:
    """Tashkilotlar bazasida tezkor qidiruv va filtrlash xizmati."""

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
        Maydonlar: Nomi, F.I.SH, INN, Izoh, Barchasi.
        """
        query_norm = normalize_text(query)
        digits_query = re.sub(r"\D", "", query_norm) if query_norm else ""
        results: List[Dict[str, Any]] = []

        for item in data:
            # 1. Toifa bo'yicha filtr
            if not SearchService.match_category(item.get("s", ""), category):
                continue

            # Qidiruv so'zi bo'lmasa, toifadagi barcha yozuvlar o'tadi
            if not query_norm:
                results.append(item)
                continue

            # 2. Maydonlar bo'yicha qidiruv
            m_norm = normalize_text(item.get("m", ""))
            f_norm = normalize_text(item.get("f", ""))
            izoh_norm = normalize_text(item.get("izoh", ""))
            inn_val = str(item.get("inn", "")).strip()
            phone_digits = re.sub(r"\D", "", str(item.get("t", "")))

            matched = False
            if field_type == "Nomi":
                matched = (query_norm in m_norm)
            elif field_type == "F.I.SH":
                matched = (query_norm in f_norm)
            elif field_type == "INN":
                matched = (digits_query in inn_val) if digits_query else (query_norm in inn_val)
            elif field_type == "Izoh":
                matched = (query_norm in izoh_norm)
            else:  # Barchasi
                if (query_norm in m_norm) or (query_norm in f_norm) or (query_norm in izoh_norm):
                    matched = True
                elif digits_query and ((digits_query in inn_val) or (digits_query in phone_digits)):
                    matched = True

            if matched:
                results.append(item)

        # 3. Saralash
        if sort_by:
            results.sort(key=lambda x: str(x.get(sort_by, "")).lower(), reverse=reverse)

        return results

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
