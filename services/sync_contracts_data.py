"""
services.sync_contracts_data: dataulan.xls faylidagi shartnomalar, apparat xodimlari soni,
tizimga ulanganlar va buxgalter kontaktlarini bazaga kiritish va sinxronlash xizmati.
"""
import os
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import xlrd

from core.logger import logger
from database.data_manager import DataManager

def format_phone_clean(val: Any) -> str:
    """Telefon raqamini 'XX XXX XX XX' yoki 'XX-XXX-XX-XX' dan toza formatga keltirish."""
    if not val:
        return ""
    digits = re.sub(r'\D', '', str(val))
    if digits.startswith('998') and len(digits) == 12:
        digits = digits[3:]
    if len(digits) == 9:
        return f"{digits[0:2]} {digits[2:5]} {digits[5:7]} {digits[7:9]}"
    return str(val).strip()

def parse_int_safe(val: Any) -> Optional[int]:
    """Raqamni xavfsiz butun songa o'tkazish."""
    if val is None or val == "":
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None

# dataulan.xls dagi maxsus INN tuzatishlari yoki bo'sh INN lar xaritasi
MANUAL_INN_MAP = {
    'поп туман 2-сон касб-ҳунар мактаби': '200088748',
    'поп туман 3-сон касб-ҳунар мактаби': '200088859',
    '7-сон болалар мусиқа ва санъат мактаби': '206986924',
    'pop tumani kelajak markaz': '207122161',
}

class ContractsSyncService:
    """Shartnoma va ulanishlar monitoring ma'lumotlarini yuklovchi servis."""

    def __init__(self, data_manager: Optional[DataManager] = None):
        self.dm = data_manager or DataManager()

    def sync_from_excel(self, excel_path: str = "dataulan.xls") -> Dict[str, Any]:
        """dataulan.xls faylini o'qib, bazadagi tashkilotlarni shartnoma ma'lumotlari bilan boyitish."""
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel fayli topilmadi: {excel_path}")

        logger.info(f"[CONTRACTS SYNC] Boshlanmoqda: {excel_path}")
        book = xlrd.open_workbook(excel_path)
        sheet = book.sheet_by_index(0)

        # Hozirgi bazadagi tashkilotlar
        current_data = self.dm.data
        db_by_inn = {}
        for item in current_data:
            inn = str(item.get("inn", "")).strip()
            if inn:
                if inn not in db_by_inn:
                    db_by_inn[inn] = []
                db_by_inn[inn].append(item)

        matched_count = 0
        added_count = 0
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        parsed_contracts = []

        for r in range(3, sheet.nrows):
            row_vals = sheet.row_values(r)
            nomi = str(row_vals[1]).strip()
            inn_raw = row_vals[2]
            inn = str(int(inn_raw)) if isinstance(inn_raw, float) and inn_raw > 0 else str(inn_raw).strip()

            # Qo'lda aniqlangan INN lar
            if not inn or inn == '206986824':
                nomi_clean = nomi.lower()
                if nomi_clean in MANUAL_INN_MAP:
                    inn = MANUAL_INN_MAP[nomi_clean]

            aparat = parse_int_safe(row_vals[3])
            ulangan = parse_int_safe(row_vals[4])
            raxbar_tel = format_phone_clean(row_vals[5])
            bux_tel = format_phone_clean(row_vals[6])

            parsed_contracts.append({
                "nomi": nomi,
                "inn": inn,
                "aparat_soni": aparat,
                "ulangan_soni": ulangan,
                "raxbar_tel": raxbar_tel,
                "bux_tel": bux_tel
            })

            # Bazadagi tashkilotlarga yangi maydonlarni biriktirish
            if inn and inn in db_by_inn:
                items = db_by_inn[inn]
                # Asosiy tashkilotni yangilash (agar bir nechta bo'lsa, 'Mahalla' yoki birinchisi)
                target_item = items[0]
                for it in items:
                    if it.get("s") in ("Mahalla", "Maktab", "Bog'cha", "Ta'lim", "Tibbiyot"):
                        target_item = it
                        break

                target_item["bux_tel"] = bux_tel
                target_item["aparat_soni"] = aparat
                target_item["ulangan_soni"] = ulangan
                if not target_item.get("t") and raxbar_tel:
                    target_item["t"] = raxbar_tel
                target_item["updated_at"] = now_str
                matched_count += 1
            else:
                # Yangi tashkilot sifatida qo'shish (masalan: Kelajak markaz)
                new_id = str(uuid.uuid4())
                new_org = {
                    "id": new_id,
                    "s": "Boshqa",
                    "m": nomi,
                    "f": "Rahbar",
                    "t": raxbar_tel,
                    "inn": inn,
                    "izoh": "Shartnoma asosida ulanish",
                    "bux_tel": bux_tel,
                    "aparat_soni": aparat,
                    "ulangan_soni": ulangan,
                    "jshr": "",
                    "seriya": "",
                    "updated_at": now_str
                }
                current_data.append(new_org)
                if inn:
                    db_by_inn[inn] = [new_org]
                added_count += 1

        # Bazani saqlash (Dual Sync)
        self.dm.data = current_data
        self.dm.save_data()

        summary = {
            "total_contract_rows": len(parsed_contracts),
            "matched_existing_orgs": matched_count,
            "newly_added_orgs": added_count,
            "total_orgs_in_db": len(self.dm.data)
        }

        logger.info(f"[CONTRACTS SYNC] Muvaffaqiyatli yakunlandi: {summary}")
        return summary

def run_contracts_sync():
    service = ContractsSyncService()
    res = service.sync_from_excel("dataulan.xls")
    print("Shartnomalar sinxronizatsiya natijasi:")
    for k, v in res.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    run_contracts_sync()
